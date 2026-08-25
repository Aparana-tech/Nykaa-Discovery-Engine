from google_play_scraper import Sort, reviews
import time

class PlayStoreScraper:
    def __init__(self, app_id: str, lang: str = 'en', country: str = 'in'):
        self.app_id = app_id
        self.lang = lang
        self.country = country

    def fetch_reviews(self, count: int = 100):
        """
        Fetches the most relevant reviews from the Google Play Store.
        Uses a mocked sleep to simulate rate-limiting considerations.
        """
        print(f"Fetching {count} reviews for {self.app_id} from Play Store...")
        
        try:
            result, continuation_token = reviews(
                self.app_id,
                lang=self.lang,
                country=self.country,
                sort=Sort.NEWEST,
                count=count
            )
            
            # Format the data for consistency across pipelines
            formatted_data = []
            for item in result:
                formatted_data.append({
                    "id": item.get('reviewId'),
                    "source": "play_store",
                    "text": item.get('content', ""),
                    "score": item.get('score'),
                    "timestamp": str(item.get('at')),
                    "author": item.get('userName', 'anonymous')
                })
                
            time.sleep(1) # Be nice to the API
            return formatted_data
            
        except Exception as e:
            print(f"Error fetching Play Store reviews: {e}")
            return []
