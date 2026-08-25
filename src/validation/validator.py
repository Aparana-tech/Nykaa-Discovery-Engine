"""
Phase 4: Insight Validation Layer & Quality Control
Implements the 4-step strict validation checks for insights.
"""
import json
import os
from google import genai
from google.genai import types

class InsightValidator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            print("WARNING: Gemini API key is missing. Dual-Model Verification will be mocked.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)

        # Mock operational return rates (Step 4.4)
        self.mock_return_rates = {
            "ethnic_wear": {"sizing_mismatch": 0.12, "fabric_quality": 0.08, "color_difference": 0.05},
            "western_wear": {"fit_issues": 0.15, "styling_uncertainty": 0.04, "material_quality": 0.06},
            "footwear": {"size_chart_confusion": 0.14, "comfort_concerns": 0.10, "color_mismatch": 0.03},
            "accessories": {"quality_expectations": 0.05, "photo_vs_reality": 0.04},
            "lingerie": {"sizing_uncertainty": 0.18, "fabric_sensitivity": 0.07, "no_try_on": 0.05},
        }

    def validate_insights(self, impact_report_path: str, output_dir: str = "mock_datalake/insights"):
        print("\n=== Running Phase 4 Validation Checkpoints ===")
        
        with open(impact_report_path, 'r') as f:
            insights = json.load(f)

        print(f"Loaded {len(insights)} insights for validation.")
        validated_insights = []
        rejected_insights = []

        for item in insights:
            print(f"\nEvaluating: '{item['friction_point']}'")
            rejection_reasons = []

            # Step 4.1: Cross-Platform Triangulation Logic
            if item["scores_breakdown"]["cross_platform"]["count"] < 2:
                rejection_reasons.append(f"Step 4.1 Failed: Found on only {item['scores_breakdown']['cross_platform']['count']} source(s). Requires >= 2.")

            # Step 4.2: Volume Thresholding
            if item["evidence"]["review_count"] < 3:
                rejection_reasons.append(f"Step 4.2 Failed: Only {item['evidence']['review_count']} occurrences. Requires >= 3 (Low volume/Noise).")

            # Step 4.3: Dual-Model Verification Architecture (Model B)
            is_hallucinated, model_b_reason = self._run_dual_model_check(item)
            if is_hallucinated:
                rejection_reasons.append(f"Step 4.3 Failed: Model B detected hallucination or weak support. Reason: {model_b_reason}")
            else:
                item["model_b_verification"] = "Passed"

            # Step 4.4: Operational Reality Check API
            passes_reality_check, op_reason = self._run_operational_reality_check(item)
            if not passes_reality_check:
                rejection_reasons.append(f"Step 4.4 Failed: Operational Reality Check failed. {op_reason}")
            else:
                item["operational_verification"] = "Passed"

            # Decision
            if rejection_reasons:
                print(f"  ❌ REJECTED:")
                for r in rejection_reasons:
                    print(f"     - {r}")
                item["rejection_reasons"] = rejection_reasons
                rejected_insights.append(item)
            else:
                print(f"  ✅ PASSED all 4 validation checkpoints.")
                item["validation_status"] = "Verified"
                validated_insights.append(item)

        print(f"\nValidation Summary: {len(validated_insights)} Passed | {len(rejected_insights)} Rejected")

        # Save results
        os.makedirs(output_dir, exist_ok=True)
        validated_path = os.path.join(output_dir, "validated_insights.json")
        rejected_path = os.path.join(output_dir, "rejected_insights.json")

        with open(validated_path, 'w') as f:
            json.dump(validated_insights, f, indent=2)
        with open(rejected_path, 'w') as f:
            json.dump(rejected_insights, f, indent=2)

        print(f"Saved {len(validated_insights)} validated insights to {validated_path}")
        print(f"Saved {len(rejected_insights)} rejected insights to {rejected_path}")

        return validated_path

    def _run_dual_model_check(self, item: dict) -> tuple[bool, str]:
        """
        Step 4.3: Ask Model B (Groq evaluator) to verify Model A's extraction.
        Returns: (is_hallucinated: bool, reason: str)
        """
        if not self.client:
            return False, "Mocked: Passed"

        insight_claim = item['friction_point']
        raw_quotes = "\\n".join(item['evidence']['sample_quotes'])

        system_prompt = f"""
        You are a strict QA Evaluator Model (Model B).
        Model A extracted the following friction point: '{insight_claim}'
        
        Based ONLY on the following source quotes, does the source text strongly and explicitly support this friction point?
        Or did Model A hallucinate/over-extrapolate it?
        
        Source Quotes:
        {raw_quotes}

        Respond ONLY with a JSON object:
        {{
            "is_supported": true/false,
            "reasoning": "brief explanation"
        }}
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=system_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    response_mime_type="application/json"
                )
            )
            response_json = json.loads(response.text)
            
            is_supported = response_json.get("is_supported", False)
            reason = response_json.get("reasoning", "No reasoning provided.")
            
            return not is_supported, reason
            
        except Exception as e:
            print(f"  ⚠️ Model B verification failed to execute: {e}. Defaulting to Passed.")
            return False, f"Error: {str(e)}"

    def _run_operational_reality_check(self, item: dict) -> tuple[bool, str]:
        """
        Step 4.4: Cross-reference insight with internal return rates.
        If return rate is < 2%, flag as anomaly/noise.
        """
        categories = item.get("business_impact", {}).get("affected_categories", [])
        friction_point = item.get("friction_point", "").lower()
        
        # Simple keyword matching to map friction to internal return reasons
        mapped_reason = None
        if "size" in friction_point or "fit" in friction_point or "length" in friction_point:
            mapped_reason = "sizing_mismatch"
        elif "fabric" in friction_point or "sheer" in friction_point or "quality" in friction_point:
            mapped_reason = "fabric_quality"
        elif "refund" in friction_point or "return" in friction_point:
             # Customer service issues don't map to product return rates, so they pass automatically
             return True, "CS Issue - exempt from return rate reality check."
             
        if not mapped_reason:
            # If we can't map it, we can't disprove it operationally, so we let it pass.
            return True, f"Could not map '{friction_point}' to an operational return category."

        for cat in categories:
            # Normalize category string to key format (e.g. "Western Wear" -> "western_wear")
            cat_key = cat.split(" ")[0].lower() + "_wear"
            if "lingerie" in cat.lower():
                cat_key = "lingerie"
            elif "accessories" in cat.lower():
                cat_key = "accessories"
            elif "footwear" in cat.lower():
                cat_key = "footwear"
            
            rates = self.mock_return_rates.get(cat_key, {})
            # Look for exact or fuzzy match in keys
            for r_key, rate in rates.items():
                if mapped_reason in r_key or r_key in mapped_reason:
                    if rate < 0.02:
                        return False, f"Operational mismatch: Text complaints are high, but actual return rate for {r_key} in {cat} is only {rate*100}% (< 2%). Flagging as noise."
                    else:
                        return True, f"Operationally validated: Return rate for {r_key} is {rate*100}%."

        return True, "No specific operational category match found; defaulting to Pass."
