"""
Step 3.3: Impact Sizing Model
Scores each friction point by business impact and generates a prioritization matrix.
"""
import json
import os
from datetime import datetime


class ImpactScorer:
    """
    Calculates a composite Impact Score for each friction point based on:
    - Volume (40%): How many reviews mention this issue
    - Severity (30%): Average negative sentiment intensity
    - Cross-Platform Presence (20%): How many distinct sources report this
    - Drop-off Correlation (10%): How strongly this maps to checkout abandonment
    """

    # Weight configuration
    WEIGHT_VOLUME = 0.40
    WEIGHT_SEVERITY = 0.30
    WEIGHT_CROSS_PLATFORM = 0.20
    WEIGHT_DROPOFF = 0.10

    # Max expected values for normalization
    MAX_VOLUME = 50  # Scale: a cluster with 50+ reviews gets max score
    MAX_SOURCES = 4  # We have 4 data sources (play_store, app_store, youtube, pdp_internal)

    def __init__(self):
        self.scored_items = []
        self.prioritization_matrix = {}
        self.total_analyzed_records = 0

    def score(self, clusters: dict, root_cause_analysis: dict, total_analyzed_records: int = 0) -> list:
        """
        Score each cluster by composite business impact.
        """
        print("\n--- Running Impact Sizing Model ---")
        self.total_analyzed_records = total_analyzed_records

        # Build a lookup from cluster_id to root cause data
        rc_lookup = {}
        for rc in root_cause_analysis.get("root_causes", []):
            rc_lookup[rc["cluster_id"]] = rc

        self.scored_items = []

        for cluster_id, cluster in clusters.items():
            if cluster.get("is_noise", False):
                continue

            cid = cluster.get("cluster_id")
            root_cause = rc_lookup.get(cid, {})

            # --- 1. Volume Score (0-1) ---
            volume = cluster.get("size", 0)
            volume_score = min(volume / self.MAX_VOLUME, 1.0)

            # --- 2. Severity Score (0-1) ---
            severity_score = self._calculate_severity(cluster)

            # --- 3. Cross-Platform Score (0-1) ---
            source_count = cluster.get("source_count", 1)
            cross_platform_score = min(source_count / self.MAX_SOURCES, 1.0)

            # --- 4. Drop-off Correlation Score (0-1) ---
            revenue_at_risk = root_cause.get("total_estimated_revenue_at_risk_monthly", 0)
            # Normalize: ₹10Cr+/month = max score
            dropoff_score = min(revenue_at_risk / 100_000_000, 1.0)

            # --- Composite Score ---
            composite_score = (
                self.WEIGHT_VOLUME * volume_score +
                self.WEIGHT_SEVERITY * severity_score +
                self.WEIGHT_CROSS_PLATFORM * cross_platform_score +
                self.WEIGHT_DROPOFF * dropoff_score
            )

            # Estimate conversion uplift if resolved
            estimated_uplift = self._estimate_conversion_uplift(
                revenue_at_risk, composite_score
            )

            item = {
                "rank": 0,  # Will be set after sorting
                "cluster_id": cid,
                "friction_point": cluster.get("label", "Unknown"),
                "barrier_type": cluster.get("dominant_barrier", "None"),
                "composite_score": round(composite_score, 4),
                "priority": self._priority_label(composite_score),
                "scores_breakdown": {
                    "volume": {"raw": volume, "normalized": round(volume_score, 3)},
                    "severity": {"raw_sentiment": cluster.get("dominant_sentiment", "neutral"), "normalized": round(severity_score, 3)},
                    "cross_platform": {"sources": cluster.get("sources", []), "count": source_count, "normalized": round(cross_platform_score, 3)},
                    "dropoff_correlation": {"revenue_at_risk_monthly": revenue_at_risk, "normalized": round(dropoff_score, 3)},
                },
                "business_impact": {
                    "estimated_monthly_revenue_at_risk": revenue_at_risk,
                    "estimated_annual_revenue_at_risk": revenue_at_risk * 12,
                    "estimated_conversion_uplift_if_fixed": estimated_uplift,
                    "funnel_stage": root_cause.get("funnel_stage", "Unknown"),
                    "affected_categories": root_cause.get("matched_categories", []),
                },
                "evidence": {
                    "review_count": volume,
                    "sample_quotes": [r["text"][:150] for r in cluster.get("records", [])[:3]],
                    "platforms": cluster.get("sources", []),
                    "cross_platform_validated": source_count >= 2,
                },
            }

            self.scored_items.append(item)

        # Sort by composite score descending and assign ranks
        self.scored_items.sort(key=lambda x: x["composite_score"], reverse=True)
        for i, item in enumerate(self.scored_items):
            item["rank"] = i + 1

        self._build_prioritization_matrix()
        self._print_summary()

        return self.scored_items

    def _calculate_severity(self, cluster: dict) -> float:
        """Calculate severity score based on sentiment distribution in the cluster."""
        aspects = cluster.get("aspects", [])
        if not aspects:
            return 0.3  # Default moderate severity if no aspects

        sentiment_map = {"negative": 1.0, "neutral": 0.3, "positive": 0.0}
        scores = [sentiment_map.get(a.get("sentiment", "neutral"), 0.3) for a in aspects]

        return sum(scores) / len(scores) if scores else 0.3

    def _priority_label(self, score: float) -> str:
        """Assign a priority label based on composite score."""
        if score >= 0.7:
            return "🔴 CRITICAL"
        elif score >= 0.5:
            return "🟠 HIGH"
        elif score >= 0.3:
            return "🟡 MEDIUM"
        else:
            return "🟢 LOW"

    def _estimate_conversion_uplift(self, revenue_at_risk: float, composite_score: float) -> str:
        """Estimate the potential conversion uplift if the friction point is resolved."""
        # Assume we can recover 30-60% of the revenue at risk depending on score
        recovery_rate = 0.3 + (composite_score * 0.3)
        potential_recovery_monthly = revenue_at_risk * recovery_rate
        potential_recovery_annual = potential_recovery_monthly * 12

        if potential_recovery_annual >= 10_000_000:
            return f"₹{potential_recovery_annual / 10_000_000:.1f}Cr+ annual recovery potential"
        elif potential_recovery_annual >= 100_000:
            return f"₹{potential_recovery_annual / 100_000:.1f}L annual recovery potential"
        else:
            return f"₹{potential_recovery_annual:,.0f} annual recovery potential"

    def _build_prioritization_matrix(self):
        """Build a summary prioritization matrix."""
        self.prioritization_matrix = {
            "generated_at": datetime.now().isoformat(),
            "total_analyzed_reviews": self.total_analyzed_records,
            "total_friction_points": len(self.scored_items),
            "critical_count": sum(1 for i in self.scored_items if "CRITICAL" in i["priority"]),
            "high_count": sum(1 for i in self.scored_items if "HIGH" in i["priority"]),
            "medium_count": sum(1 for i in self.scored_items if "MEDIUM" in i["priority"]),
            "low_count": sum(1 for i in self.scored_items if "LOW" in i["priority"]),
            "total_monthly_revenue_at_risk": sum(
                i["business_impact"]["estimated_monthly_revenue_at_risk"] for i in self.scored_items
            ),
            "top_3_actions": [
                {
                    "rank": item["rank"],
                    "action": f"Fix '{item['friction_point']}' in {item['barrier_type']}",
                    "impact": item["business_impact"]["estimated_conversion_uplift_if_fixed"],
                    "priority": item["priority"],
                }
                for item in self.scored_items[:3]
            ],
        }

    def _print_summary(self):
        """Print a human-readable summary of the impact analysis."""
        print("\n" + "=" * 70)
        print("  FRICTION POINT PRIORITIZATION MATRIX")
        print("=" * 70)

        for item in self.scored_items:
            print(f"\n  #{item['rank']} {item['priority']}")
            print(f"     Friction: {item['friction_point']}")
            print(f"     Barrier:  {item['barrier_type']}")
            print(f"     Score:    {item['composite_score']:.3f}")
            print(f"     Volume:   {item['evidence']['review_count']} reviews across {item['scores_breakdown']['cross_platform']['count']} platforms")
            rev = item['business_impact']['estimated_monthly_revenue_at_risk']
            if rev > 0:
                print(f"     Revenue:  ₹{rev:,.0f}/month at risk")
            print(f"     Uplift:   {item['business_impact']['estimated_conversion_uplift_if_fixed']}")

        total_rev = self.prioritization_matrix.get("total_monthly_revenue_at_risk", 0)
        print(f"\n{'=' * 70}")
        print(f"  TOTAL MONTHLY REVENUE AT RISK: ₹{total_rev:,.0f}")
        print(f"  Critical: {self.prioritization_matrix['critical_count']} | High: {self.prioritization_matrix['high_count']} | Medium: {self.prioritization_matrix['medium_count']} | Low: {self.prioritization_matrix['low_count']}")
        print(f"{'=' * 70}\n")

    def save_report(self, output_dir: str = "mock_datalake/insights"):
        """Save impact report and prioritization matrix."""
        os.makedirs(output_dir, exist_ok=True)

        # Save full report
        report_path = os.path.join(output_dir, "impact_report.json")
        with open(report_path, 'w') as f:
            json.dump(self.scored_items, f, indent=2, default=str)
        print(f"Saved impact report to {report_path}")

        # Save prioritization matrix
        matrix_path = os.path.join(output_dir, "prioritization_matrix.json")
        with open(matrix_path, 'w') as f:
            json.dump(self.prioritization_matrix, f, indent=2, default=str)
        print(f"Saved prioritization matrix to {matrix_path}")

        return report_path, matrix_path
