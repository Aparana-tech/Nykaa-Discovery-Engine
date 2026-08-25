import requests
import os
import time

class RedditScraper:
    def __init__(self, user_agent="NykaaDiscoveryEngine/1.0 (Contact: admin@example.com)"):
        self.user_agent = user_agent
        self.headers = {'User-Agent': self.user_agent}

    def fetch_discussions(self, subreddits: list, limit: int = 50):
        """
        Fetches top discussions and comments from a list of subreddits using the public JSON API.
        No API keys required.
        """
        formatted_data = []
        for sub in subreddits:
            print(f"Fetching {limit} posts from r/{sub} using public JSON API...")
            try:
                url = f"https://www.reddit.com/r/{sub}/top.json?t=month&limit={limit}"
                response = requests.get(url, headers=self.headers)
                
                if response.status_code != 200:
                    print(f"Error fetching from r/{sub}: HTTP {response.status_code}")
                    continue
                    
                data = response.json()
                posts = data.get('data', {}).get('children', [])
                
                for post_child in posts:
                    post = post_child['data']
                    # Add main post
                    formatted_data.append({
                        "id": post.get('id', ''),
                        "source": f"reddit_r/{sub}",
                        "text": f"{post.get('title', '')} {post.get('selftext', '')}",
                        "score": post.get('score', 0),
                        "timestamp": str(post.get('created_utc', '')),
                        "author": post.get('author', 'anonymous')
                    })
                    
                    # We can fetch comments by hitting the specific post's JSON endpoint,
                    # but to avoid aggressive rate-limiting on the public API, we'll just pull the post bodies for now.
                    
                time.sleep(1.5) # Rate limit protection (Reddit asks for 1 req/sec max for unauthenticated)
            except Exception as e:
                print(f"Error fetching from r/{sub}: {e}")
                
        return formatted_data

    def _generate_mock_data(self, subreddits, limit):
        print("Generating mock Reddit data...")
        data = []
        for i in range(min(5, limit)):
            data.append({
                "id": f"mock_r_{i}",
                "source": "reddit_r/IndianFashionAddicts",
                "text": "I ordered this dress from Nykaa, the fabric is nice but the fit is terribly tight around the bust.",
                "score": 150,
                "timestamp": str(time.time()),
                "author": "mock_user1"
            })
            data.append({
                "id": f"mock_r_{i+1}_b",
                "source": "reddit_r/IndianBeautyDeals",
                "text": "Got a great deal, but it looks completely different from the PDP images. The color is washed out.",
                "score": 89,
                "timestamp": str(time.time()),
                "author": "mock_user2"
            })
        return data
