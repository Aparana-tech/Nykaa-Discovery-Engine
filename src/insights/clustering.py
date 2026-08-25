"""
Step 3.1: Hesitation Clustering
Groups similar user complaints/doubts using embeddings + HDBSCAN clustering.
"""
import json
import os
import glob
import numpy as np
from collections import Counter


class HesitationClusterer:
    """
    Loads analyzed review data, generates text embeddings, and clusters 
    similar user hesitations together using HDBSCAN.
    """

    def __init__(self, analyzed_data_path: str = "mock_datalake/analyzed"):
        self.analyzed_data_path = analyzed_data_path
        self.records = []
        self.embeddings = None
        self.cluster_labels = None
        self.clusters = {}

    def load_analyzed_data(self):
        """Load all analyzed JSON files from the data lake."""
        print("Loading all analyzed data...")
        all_files = glob.glob(os.path.join(self.analyzed_data_path, "**/*.json"), recursive=True)

        seen_ids = set()
        for filepath in all_files:
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                for record in data:
                    record_id = record.get('id')
                    # Deduplicate records (multiple pipeline runs may have duplicates)
                    if record_id and record_id not in seen_ids:
                        # Only include records with valid groq_analysis
                        analysis = record.get('groq_analysis', {})
                        if 'error' not in analysis and 'aspects' in analysis:
                            seen_ids.add(record_id)
                            self.records.append(record)
            except Exception as e:
                print(f"  Skipping file {filepath}: {e}")

        print(f"Loaded {len(self.records)} unique analyzed records from {len(all_files)} files.")
        return self.records

    def generate_embeddings(self):
        """Generate sentence embeddings for all review texts."""
        if not self.records:
            print("No records loaded. Call load_analyzed_data() first.")
            return

        print(f"Generating embeddings for {len(self.records)} records...")

        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')

            texts = [r.get('text', '') or r.get('original_text', '') for r in self.records]
            self.embeddings = model.encode(texts, show_progress_bar=True)
            print(f"Generated embeddings with shape: {self.embeddings.shape}")

        except ImportError:
            print("WARNING: sentence-transformers not installed. Using TF-IDF fallback.")
            self._tfidf_fallback()

    def _tfidf_fallback(self):
        """Fallback: Use TF-IDF vectors if sentence-transformers is unavailable."""
        from sklearn.feature_extraction.text import TfidfVectorizer

        texts = [r.get('text', '') or r.get('original_text', '') for r in self.records]
        vectorizer = TfidfVectorizer(max_features=256, stop_words='english')
        self.embeddings = vectorizer.fit_transform(texts).toarray()
        print(f"Generated TF-IDF embeddings with shape: {self.embeddings.shape}")

    def cluster(self, min_cluster_size: int = 2):
        """Run HDBSCAN clustering on the embeddings."""
        if self.embeddings is None:
            print("No embeddings generated. Call generate_embeddings() first.")
            return

        print(f"Running HDBSCAN clustering (min_cluster_size={min_cluster_size})...")

        try:
            import hdbscan
            clusterer = hdbscan.HDBSCAN(
                min_cluster_size=min_cluster_size,
                min_samples=1,
                metric='euclidean',
                cluster_selection_method='eom'
            )
            self.cluster_labels = clusterer.fit_predict(self.embeddings)
        except ImportError:
            print("WARNING: hdbscan not installed. Using sklearn DBSCAN fallback.")
            from sklearn.cluster import DBSCAN
            clusterer = DBSCAN(eps=0.5, min_samples=min_cluster_size)
            self.cluster_labels = clusterer.fit_predict(self.embeddings)

        n_clusters = len(set(self.cluster_labels)) - (1 if -1 in self.cluster_labels else 0)
        n_noise = list(self.cluster_labels).count(-1)
        print(f"Found {n_clusters} clusters and {n_noise} noise points.")

        return self._build_cluster_output()

    def _build_cluster_output(self):
        """Build structured cluster output with labels and summaries."""
        self.clusters = {}

        for i, label in enumerate(self.cluster_labels):
            label_str = str(label)
            if label_str not in self.clusters:
                self.clusters[label_str] = {
                    "cluster_id": int(label),
                    "is_noise": label == -1,
                    "records": [],
                    "aspects": [],
                    "barriers": [],
                    "sources": set(),
                }

            record = self.records[i]
            analysis = record.get('groq_analysis', {})

            self.clusters[label_str]["records"].append({
                "id": record.get("id"),
                "text": record.get("original_text", record.get("text", "")),
                "source": record.get("source", "unknown"),
                "score": record.get("score"),
            })

            # Collect aspects
            for aspect in analysis.get("aspects", []):
                self.clusters[label_str]["aspects"].append(aspect)

            # Collect barriers
            barrier = analysis.get("barrier_classification", "None")
            if barrier and barrier != "None":
                self.clusters[label_str]["barriers"].append(barrier)

            # Collect sources
            source = record.get("source", "unknown")
            self.clusters[label_str]["sources"].add(source.split("_")[0])

        # Label each cluster and convert sets to lists
        for label_str, cluster in self.clusters.items():
            cluster["size"] = len(cluster["records"])
            cluster["sources"] = list(cluster["sources"])
            cluster["source_count"] = len(cluster["sources"])

            # Determine dominant barrier
            if cluster["barriers"]:
                barrier_counts = Counter(cluster["barriers"])
                cluster["dominant_barrier"] = barrier_counts.most_common(1)[0][0]
            else:
                cluster["dominant_barrier"] = "None"

            # Determine dominant aspect
            if cluster["aspects"]:
                feature_counts = Counter(a.get("feature", "") for a in cluster["aspects"])
                cluster["dominant_feature"] = feature_counts.most_common(1)[0][0]

                sentiments = [a.get("sentiment", "neutral") for a in cluster["aspects"]]
                sentiment_counts = Counter(sentiments)
                cluster["dominant_sentiment"] = sentiment_counts.most_common(1)[0][0]
            else:
                cluster["dominant_feature"] = "general"
                cluster["dominant_sentiment"] = "neutral"

            # Generate a human-readable label
            cluster["label"] = f"{cluster['dominant_feature']} ({cluster['dominant_sentiment']})"

        return self.clusters

    def save_clusters(self, output_dir: str = "mock_datalake/insights"):
        """Save cluster results to a JSON file."""
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "clusters.json")

        # Create a serializable copy (remove raw aspect lists for cleaner output)
        output = {}
        for label, cluster in self.clusters.items():
            output[label] = {
                "cluster_id": int(cluster["cluster_id"]),
                "label": cluster["label"],
                "is_noise": bool(cluster["is_noise"]),
                "size": cluster["size"],
                "dominant_barrier": cluster["dominant_barrier"],
                "dominant_feature": cluster["dominant_feature"],
                "dominant_sentiment": cluster["dominant_sentiment"],
                "sources": cluster["sources"],
                "source_count": cluster["source_count"],
                "sample_quotes": [r["text"][:150] for r in cluster["records"][:3]],
                "records": cluster["records"],
            }

        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"Saved {len(output)} clusters to {output_path}")
        return output
