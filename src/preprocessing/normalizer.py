import re
import html

class TextNormalizer:
    def __init__(self):
        # Basic Regex patterns for PII removal
        self.email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
        self.phone_pattern = re.compile(r'\+?\d{10,13}')
        
        # Regex to match emojis and non-ascii characters (basic)
        # Note: In a production system, use the `emoji` package for better parsing
        self.emoji_pattern = re.compile(r'[^\w\s.,!?\'"-]')

    def clean_text(self, text: str) -> str:
        """
        Runs the full normalization pipeline on a string of text.
        """
        if not text or not isinstance(text, str):
            return ""
            
        # 1. Unescape HTML entities (e.g., &amp; -> &)
        text = html.unescape(text)
        
        # 2. Strip PII
        text = self.email_pattern.sub('[EMAIL_REMOVED]', text)
        text = self.phone_pattern.sub('[PHONE_REMOVED]', text)
        
        # 3. Remove Emojis / Weird Characters (optional based on downstream model, 
        # but often good for basic NLP if not using specific emoji sentiment models)
        text = self.emoji_pattern.sub('', text)
        
        # 4. Standardize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 5. Lowercase for consistency
        text = text.lower()
        
        return text

    def process_batch(self, data_records: list) -> list:
        """
        Processes a batch of dictionary records, cleaning the 'text' field.
        """
        processed_data = []
        for record in data_records:
            cleaned_record = record.copy()
            
            # Keep original text for debugging/auditing if needed
            cleaned_record['original_text'] = cleaned_record.get('text', '')
            cleaned_record['text'] = self.clean_text(cleaned_record.get('text', ''))
            
            processed_data.append(cleaned_record)
            
        return processed_data
