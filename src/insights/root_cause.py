"""
Step 3.2: Drop-off Root Cause Analysis
Correlates hesitation clusters with wishlist-to-checkout drop-off telemetry.
"""
import json
import os


class DropOffAnalyzer:
    """
    Maps hesitation clusters to product categories and correlates them with 
    simulated wishlist-to-checkout drop-off data to identify root causes.
    """

    def __init__(self):
        # Simulated internal telemetry: drop-off rates by product category
        # In production, this would pull from a real data warehouse
        self.dropoff_telemetry = {
            "ethnic_wear": {
                "category": "Ethnic Wear (Sarees, Kurtas, Lehengas)",
                "wishlist_adds_monthly": 125000,
                "checkout_completions": 31250,
                "dropoff_rate": 0.75,
                "avg_cart_value": 2400,
                "top_return_reasons": ["sizing_mismatch", "fabric_quality", "color_difference"],
            },
            "western_wear": {
                "category": "Western Wear (Dresses, Tops, Jeans)",
                "wishlist_adds_monthly": 98000,
                "checkout_completions": 29400,
                "dropoff_rate": 0.70,
                "avg_cart_value": 1800,
                "top_return_reasons": ["fit_issues", "styling_uncertainty", "material_quality"],
            },
            "footwear": {
                "category": "Footwear (Heels, Flats, Sneakers)",
                "wishlist_adds_monthly": 67000,
                "checkout_completions": 23450,
                "dropoff_rate": 0.65,
                "avg_cart_value": 1500,
                "top_return_reasons": ["size_chart_confusion", "comfort_concerns", "color_mismatch"],
            },
            "accessories": {
                "category": "Accessories (Bags, Jewelry, Watches)",
                "wishlist_adds_monthly": 45000,
                "checkout_completions": 18000,
                "dropoff_rate": 0.60,
                "avg_cart_value": 1200,
                "top_return_reasons": ["quality_expectations", "photo_vs_reality"],
            },
            "lingerie": {
                "category": "Lingerie & Innerwear",
                "wishlist_adds_monthly": 38000,
                "checkout_completions": 9500,
                "dropoff_rate": 0.75,
                "avg_cart_value": 900,
                "top_return_reasons": ["sizing_uncertainty", "fabric_sensitivity", "no_try_on"],
            },
        }

        # Mapping keywords in review aspects to product categories
        self.category_keywords = {
            "ethnic_wear": ["saree", "kurta", "lehenga", "ethnic", "dupatta", "salwar", "anarkali", "choli"],
            "western_wear": ["dress", "top", "jeans", "shirt", "skirt", "western", "tshirt", "jacket", "blazer"],
            "footwear": ["shoe", "heel", "flat", "sneaker", "sandal", "footwear", "slipper", "boot"],
            "accessories": ["bag", "jewelry", "watch", "earring", "necklace", "ring", "bracelet", "clutch"],
            "lingerie": ["bra", "lingerie", "innerwear", "panty", "underwear", "nightwear"],
        }

        # Mapping barrier types to their funnel impact
        self.barrier_funnel_impact = {
            "Fit/Fabric Uncertainty": {
                "funnel_stage": "Pre-Purchase Decision",
                "impact_description": "Users cannot confidently choose a size or trust fabric quality, causing them to abandon at checkout.",
                "affected_categories": ["ethnic_wear", "western_wear", "lingerie"],
                "estimated_dropoff_contribution": 0.35,
            },
            "Choice Paralysis": {
                "funnel_stage": "Product Discovery",
                "impact_description": "Users are overwhelmed by too many options without clear differentiation, causing analysis paralysis.",
                "affected_categories": ["ethnic_wear", "western_wear", "accessories"],
                "estimated_dropoff_contribution": 0.20,
            },
            "Styling Ambiguity": {
                "funnel_stage": "Consideration",
                "impact_description": "Users don't know how to style the product or what it pairs with, reducing purchase confidence.",
                "affected_categories": ["ethnic_wear", "western_wear", "footwear"],
                "estimated_dropoff_contribution": 0.15,
            },
            "Taxonomy Disconnect": {
                "funnel_stage": "Search & Navigation",
                "impact_description": "Users can't find what they're looking for because platform categories don't match how they think about fashion.",
                "affected_categories": ["ethnic_wear", "accessories"],
                "estimated_dropoff_contribution": 0.10,
            },
        }

    def analyze(self, clusters: dict) -> dict:
        """
        Correlate hesitation clusters with drop-off telemetry data.
        Returns a root cause analysis mapping.
        """
        print("\n--- Running Drop-off Root Cause Analysis ---")

        root_causes = []

        for cluster_id, cluster in clusters.items():
            if cluster.get("is_noise", False):
                continue

            barrier = cluster.get("dominant_barrier", "None")
            feature = cluster.get("dominant_feature", "general")

            # Map cluster to product categories
            matched_categories = self._map_to_categories(cluster)

            # Get barrier funnel impact
            funnel_data = self.barrier_funnel_impact.get(barrier, {})

            # Calculate estimated revenue at risk
            revenue_at_risk = 0
            category_details = []
            for cat_key in matched_categories:
                telemetry = self.dropoff_telemetry.get(cat_key, {})
                if telemetry:
                    dropoff_contribution = funnel_data.get("estimated_dropoff_contribution", 0.05)
                    monthly_lost = telemetry["wishlist_adds_monthly"] * telemetry["dropoff_rate"] * dropoff_contribution
                    revenue_lost = monthly_lost * telemetry["avg_cart_value"]
                    revenue_at_risk += revenue_lost

                    category_details.append({
                        "category": telemetry["category"],
                        "dropoff_rate": telemetry["dropoff_rate"],
                        "monthly_abandoned_due_to_this": int(monthly_lost),
                        "estimated_revenue_loss_monthly": round(revenue_lost, 2),
                    })

            root_cause = {
                "cluster_id": cluster.get("cluster_id"),
                "cluster_label": cluster.get("label"),
                "barrier_type": barrier,
                "dominant_feature": feature,
                "cluster_size": cluster.get("size", 0),
                "funnel_stage": funnel_data.get("funnel_stage", "Unknown"),
                "impact_description": funnel_data.get("impact_description", "Unclassified friction point."),
                "matched_categories": [self.dropoff_telemetry.get(c, {}).get("category", c) for c in matched_categories],
                "category_details": category_details,
                "total_estimated_revenue_at_risk_monthly": round(revenue_at_risk, 2),
                "source_platforms": cluster.get("sources", []),
                "cross_platform_validated": cluster.get("source_count", 0) >= 2,
            }

            root_causes.append(root_cause)
            print(f"  Cluster '{cluster.get('label')}': Barrier={barrier}, Revenue at risk=₹{revenue_at_risk:,.0f}/mo")

        # Sort by revenue at risk
        root_causes.sort(key=lambda x: x["total_estimated_revenue_at_risk_monthly"], reverse=True)

        print(f"Completed root cause analysis for {len(root_causes)} clusters.")
        return {"root_causes": root_causes, "telemetry_source": "simulated_internal_data"}

    def _map_to_categories(self, cluster: dict) -> list:
        """Map a cluster to product categories based on keyword matching."""
        matched = set()

        # Check review texts for category keywords
        for record in cluster.get("records", []):
            text = record.get("text", "").lower()
            for cat_key, keywords in self.category_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        matched.add(cat_key)

        # Check aspect features
        for aspect in cluster.get("aspects", []):
            feature = aspect.get("feature", "").lower()
            for cat_key, keywords in self.category_keywords.items():
                for keyword in keywords:
                    if keyword in feature:
                        matched.add(cat_key)

        # If no category matched, use barrier-based defaults
        if not matched:
            barrier = cluster.get("dominant_barrier", "None")
            funnel_data = self.barrier_funnel_impact.get(barrier, {})
            matched = set(funnel_data.get("affected_categories", ["western_wear"]))

        return list(matched)

    def save_analysis(self, analysis: dict, output_dir: str = "mock_datalake/insights"):
        """Save root cause analysis to JSON."""
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "root_cause_analysis.json")

        with open(output_path, 'w') as f:
            json.dump(analysis, f, indent=2)

        print(f"Saved root cause analysis to {output_path}")
        return output_path
