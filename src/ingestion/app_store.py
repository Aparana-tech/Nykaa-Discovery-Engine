import requests
import os
import time

class AppStoreScraper:
    """
    Fetches Apple App Store reviews using SerpApi's Apple App Store API.
    Falls back to mock data if no SERPAPI_KEY is provided.
    """
    def __init__(self, app_name: str = 'nykaa-fashion-shopping', app_id: str = '1439872423', country: str = 'in'):
        self.app_name = app_name
        self.app_id = app_id
        self.country = country
        self.api_key = os.environ.get("SERPAPI_KEY")
        self.use_mock = not self.api_key or self.api_key == '"your_serpapi_key_here"'

        if self.use_mock:
            print("WARNING: SERPAPI_KEY missing. Using mock data for App Store.")

    def fetch_reviews(self, count: int = 100):
        """
        Fetches reviews from the Apple App Store via SerpApi.
        Falls back to mock data if no API key is provided.
        """
        if self.use_mock:
            return self._generate_mock_data(count)

        print(f"Fetching {count} reviews for {self.app_name} from App Store (via SerpApi)...")

        try:
            params = {
                "engine": "apple_reviews",
                "product_id": self.app_id,
                "country": self.country,
                "sort": "mostrecent",
                "page": "1",
                "api_key": self.api_key,
            }

            response = requests.get("https://serpapi.com/search.json", params=params)
            response.raise_for_status()
            data = response.json()

            reviews = data.get("reviews", [])

            formatted_data = []
            for item in reviews:
                # Extract author name from nested dict
                author = item.get("author", {})
                author_name = author.get("name", "anonymous") if isinstance(author, dict) else str(author)

                formatted_data.append({
                    "id": str(item.get("id", time.time())),
                    "source": "app_store",
                    "text": item.get("text", ""),
                    "score": item.get("rating"),
                    "timestamp": str(item.get("review_date", "")),
                    "author": author_name,
                    "title": item.get("title", ""),
                })

            print(f"Fetched {len(formatted_data)} App Store reviews via SerpApi.")
            time.sleep(1)  # Rate limit protection
            return formatted_data[:count]

        except Exception as e:
            print(f"Error fetching App Store reviews via SerpApi: {e}")
            return []

    def _generate_mock_data(self, limit):
        """Generate mock App Store review data for testing."""
        print("Generating mock App Store data...")
        data = []
        mock_reviews = [
            {
                "text": "Love the Nykaa Fashion app! Great collection of ethnic wear. Delivery was quick too.",
                "score": 5,
                "author": "FashionLover_IN",
                "title": "Amazing collection!",
            },
            {
                "text": "App crashes frequently when I try to filter by size. Please fix this bug.",
                "score": 2,
                "author": "ShopperGirl23",
                "title": "Too many crashes",
            },
            {
                "text": "Good variety but the return process is very confusing. Took 2 weeks to get my refund.",
                "score": 3,
                "author": "ReturnNightmare",
                "title": "Returns need improvement",
            },
        ]
        for i, review in enumerate(mock_reviews[:limit]):
            data.append({
                "id": f"mock_appstore_{i}",
                "source": "app_store",
                "text": review["text"],
                "score": review["score"],
                "timestamp": "2024-01-15T10:30:00Z",
                "author": review["author"],
                "title": review["title"],
            })
        return data
