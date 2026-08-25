import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from insights.clustering import HesitationClusterer
from insights.root_cause import DropOffAnalyzer
from insights.impact_scorer import ImpactScorer

print("=== Starting Phase 3: Analytics & Impact Sizing ===")

# Step 3.1: Hesitation Clustering
clusterer = HesitationClusterer()
clusterer.load_analyzed_data()
clusterer.generate_embeddings()
clusters = clusterer.cluster()
clusterer.save_clusters()

# Step 3.2: Drop-off Root Cause Analysis
root_cause_analyzer = DropOffAnalyzer()
rc_analysis = root_cause_analyzer.analyze(clusters)
root_cause_analyzer.save_analysis(rc_analysis)

# Step 3.3: Impact Sizing Model
impact_scorer = ImpactScorer()
impact_scorer.score(clusters, rc_analysis)
impact_scorer.save_report()

print("\n=== Phase 3 Completed Successfully! ===")
