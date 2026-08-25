import os
import json
import shutil

def export_data_to_frontend():
    print("=== Exporting Data to Frontend ===")
    
    src_dir = "mock_datalake/insights"
    dest_dir = "frontend/src/data"
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    # Files to copy
    files_to_copy = [
        "validated_insights.json",
        "prioritization_matrix.json"
    ]
    
    for filename in files_to_copy:
        src_path = os.path.join(src_dir, filename)
        dest_path = os.path.join(dest_dir, filename)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Copied {filename} to frontend/src/data/")
        else:
            print(f"Warning: {filename} not found in {src_dir}")
            
    print("Export complete.")

if __name__ == "__main__":
    export_data_to_frontend()
