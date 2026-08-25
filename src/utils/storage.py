import os
import json
from datetime import datetime

class DataLakeManager:
    """
    A mock storage manager that simulates saving to cloud storage (e.g., AWS S3).
    It saves files to a local 'mock_datalake' directory.
    """
    def __init__(self, base_path: str = "mock_datalake"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save_raw_data(self, source_name: str, data: list):
        """Saves raw ingested data to the datalake."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{source_name}_raw_{timestamp}.json"
        
        # Create source-specific directory
        source_dir = os.path.join(self.base_path, "raw", source_name)
        os.makedirs(source_dir, exist_ok=True)
        
        file_path = os.path.join(source_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Saved {len(data)} raw records to {file_path}")
        return file_path

    def save_processed_data(self, source_name: str, data: list):
        """Saves preprocessed data to the datalake."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{source_name}_processed_{timestamp}.json"
        
        # Create source-specific directory
        source_dir = os.path.join(self.base_path, "processed", source_name)
        os.makedirs(source_dir, exist_ok=True)
        
        file_path = os.path.join(source_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Saved {len(data)} processed records to {file_path}")
        return file_path

    def save_analyzed_data(self, source_name: str, data: list):
        """Saves Groq analyzed data to the datalake."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{source_name}_analyzed_{timestamp}.json"
        
        source_dir = os.path.join(self.base_path, "analyzed", source_name)
        os.makedirs(source_dir, exist_ok=True)
        
        file_path = os.path.join(source_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Saved {len(data)} AI-analyzed records to {file_path}")
        return file_path
