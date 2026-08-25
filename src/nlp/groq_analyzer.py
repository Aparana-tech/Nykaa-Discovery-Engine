import os
import json
from groq import Groq

class GroqFashionAnalyzer:
    def __init__(self, api_key: str = None, model: str = "qwen/qwen3.6-27b"):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.model = model
        
        if not self.api_key or "your_groq_api_key_here" in self.api_key:
            print("WARNING: Groq API key is missing or invalid. Analysis will be mocked.")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)
            
        self.system_prompt = """
        You are an expert AI fashion analyst for Nykaa Fashion. Your job is to extract highly structured insights from user reviews.
        You will receive a user review. You must output a JSON object exactly matching this schema, with no markdown formatting or conversational text outside the JSON:
        {
            "aspects": [
                {
                    "feature": "string (e.g. fabric, zipper, length)",
                    "sentiment": "positive|negative|neutral",
                    "quote": "string (the exact words referencing this)"
                }
            ],
            "named_entities": {
                "sizing_mentioned": ["string"],
                "fabric_mentioned": ["string"]
            },
            "barrier_classification": "Fit/Fabric Uncertainty | Choice Paralysis | Styling Ambiguity | Taxonomy Disconnect | None"
        }
        """

    def analyze_text(self, text: str) -> dict:
        """
        Sends a single text string to the Groq API and returns the structured JSON response.
        """
        if not self.client:
            return self._mock_analysis(text)
            
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt,
                    },
                    {
                        "role": "user",
                        "content": f"Review text: '{text}'",
                    }
                ],
                model=self.model,
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            
            response_text = chat_completion.choices[0].message.content
            return json.loads(response_text)
            
        except Exception as e:
            print(f"Error during Groq API call: {e}")
            return {"error": str(e)}

    def process_batch(self, data_records: list) -> list:
        """
        Takes a list of preprocessed records, runs them through Groq, and appends the 'analysis' field.
        """
        analyzed_data = []
        for record in data_records:
            print(f"Analyzing record ID {record.get('id')}...")
            analyzed_record = record.copy()
            
            # Use the cleaned text for analysis
            text_to_analyze = analyzed_record.get('text', '')
            analysis_result = self.analyze_text(text_to_analyze)
            
            analyzed_record['groq_analysis'] = analysis_result
            analyzed_data.append(analyzed_record)
            
        return analyzed_data
        
    def _mock_analysis(self, text: str) -> dict:
        """Returns a mock structured analysis if no API key is present."""
        return {
            "aspects": [
                {
                    "feature": "mock_fabric",
                    "sentiment": "negative",
                    "quote": "fabric is terribly tight"
                }
            ],
            "named_entities": {
                "sizing_mentioned": ["tight fit"],
                "fabric_mentioned": []
            },
            "barrier_classification": "Fit/Fabric Uncertainty"
        }
