from googleapiclient.discovery import build
import os
import time

class YouTubeScraper:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("YOUTUBE_API_KEY")
        self.use_mock = not self.api_key
        
        if not self.use_mock:
            self.youtube = build("youtube", "v3", developerKey=self.api_key)
        else:
            print("WARNING: YouTube API key missing. Using mock data mode.")

    def search_videos(self, query: str, max_results: int = 2) -> list:
        """
        Searches YouTube for videos matching the query and returns a list of Video IDs.
        """
        if self.use_mock:
            print(f"Mock search for: {query}")
            return ['mock_video_id_123']
            
        print(f"Searching YouTube for: '{query}'...")
        try:
            request = self.youtube.search().list(
                part="id",
                q=query,
                type="video",
                maxResults=max_results
            )
            response = request.execute()
            
            video_ids = []
            for item in response.get("items", []):
                video_ids.append(item["id"]["videoId"])
                
            print(f"Found {len(video_ids)} videos: {video_ids}")
            return video_ids
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return []

    def fetch_comments(self, video_ids: list, max_results: int = 50):
        """
        Fetches top comments from a list of YouTube video IDs.
        Falls back to mock data if no API keys are provided.
        """
        if self.use_mock:
            return self._generate_mock_data(video_ids, max_results)
            
        formatted_data = []
        for video_id in video_ids:
            print(f"Fetching comments for YouTube Video ID: {video_id}...")
            try:
                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=max_results,
                    textFormat="plainText"
                )
                response = request.execute()

                for item in response.get("items", []):
                    comment = item["snippet"]["topLevelComment"]["snippet"]
                    formatted_data.append({
                        "id": item["id"],
                        "source": f"youtube_{video_id}",
                        "text": comment["textDisplay"],
                        "score": comment["likeCount"],
                        "timestamp": comment["publishedAt"],
                        "author": comment["authorDisplayName"]
                    })
                time.sleep(1) # Rate limit protection
            except Exception as e:
                print(f"Error fetching from YouTube Video {video_id}: {e}")
                
        return formatted_data

    def _generate_mock_data(self, video_ids, limit):
        print("Generating mock YouTube data...")
        data = []
        for i in range(min(3, limit)):
            data.append({
                "id": f"mock_yt_{i}",
                "source": "youtube_mock_video",
                "text": "The try-on haul looks great, but what size did she actually wear? I can't tell if it has stretch.",
                "score": 45,
                "timestamp": "2023-10-01T12:00:00Z",
                "author": "mock_yt_viewer"
            })
            data.append({
                "id": f"mock_yt_{i+1}_b",
                "source": "youtube_mock_video",
                "text": "I bought this same top and the lining is totally missing. Don't buy it!",
                "score": 12,
                "timestamp": "2023-10-02T14:30:00Z",
                "author": "mock_yt_reviewer2"
            })
        return data
