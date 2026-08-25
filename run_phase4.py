import os
import sys

# Ensure src/ is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from dotenv import load_dotenv
load_dotenv()

from validation.validator import InsightValidator

def run_phase4():
    print("=== Starting Phase 4: Insight Validation Layer & Quality Control ===")
    
    impact_report_path = "mock_datalake/insights/impact_report.json"
    
    if not os.path.exists(impact_report_path):
        print(f"Error: Could not find Phase 3 output at {impact_report_path}")
        print("Please run Phase 3 first.")
        return
        
    validator = InsightValidator()
    validator.validate_insights(impact_report_path)

if __name__ == "__main__":
    run_phase4()
