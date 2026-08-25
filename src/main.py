import os
import sys

# Add src to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.storage import DataLakeManager
from ingestion.play_store import PlayStoreScraper
from ingestion.app_store import AppStoreScraper
from ingestion.reddit_api import RedditScraper
from ingestion.youtube_api import YouTubeScraper
from ingestion.pdp_internal import InternalPDPConnector
from preprocessing.normalizer import TextNormalizer
from dotenv import load_dotenv
from nlp.gemini_analyzer import GeminiFashionAnalyzer
from insights.clustering import HesitationClusterer
from insights.root_cause import DropOffAnalyzer
from insights.impact_scorer import ImpactScorer
from validation.validator import InsightValidator

def run_phase1_pipeline():
    # Local macOS SSL Fix for Play/App Store scrapers
    import ssl
    import urllib.request
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    # Load environment variables from .env file if it exists
    load_dotenv()
    
    print("=== Starting Nykaa Fashion Discovery Engine: Pipeline ===\n")
    
    # Initialize Storage and Normalizer
    datalake = DataLakeManager()
    normalizer = TextNormalizer()
    gemini_analyzer = GeminiFashionAnalyzer()
    
    # ---------------------------------------------------------
    # 1. App/Play Store Pipeline
    # ---------------------------------------------------------
    print("--- 1. App/Play Store Pipeline ---")
    
    # Android (Play Store)
    nykaa_play_store = PlayStoreScraper(app_id='com.fsn.nykaa')
    play_store_data = nykaa_play_store.fetch_reviews(count=750)
    
    if play_store_data:
        datalake.save_raw_data("play_store", play_store_data)
        processed_play_store = normalizer.process_batch(play_store_data)
        datalake.save_processed_data("play_store", processed_play_store)
        
        analyzed_play_store = gemini_analyzer.process_batch(processed_play_store)
        datalake.save_analyzed_data("play_store", analyzed_play_store)
        
    # iOS (App Store via SerpApi)
    print("\nFetching reviews from Apple App Store (via SerpApi)...")
    nykaa_app_store = AppStoreScraper(app_name='nykaa-fashion-shopping', app_id='1439872423', country='in')
    app_store_data = nykaa_app_store.fetch_reviews(count=300)
    
    if app_store_data:
        datalake.save_raw_data("app_store", app_store_data)
        processed_app_store = normalizer.process_batch(app_store_data)
        datalake.save_processed_data("app_store", processed_app_store)
        
        analyzed_app_store = gemini_analyzer.process_batch(processed_app_store)
        datalake.save_analyzed_data("app_store", analyzed_app_store)
        
    # ---------------------------------------------------------
    # 2. Reddit Ingestion
    # ---------------------------------------------------------
    print("\n--- 2. Reddit API Ingestion ---")
    reddit_scraper = RedditScraper() # Will use mock data if keys are absent
    reddit_data = reddit_scraper.fetch_discussions(
        subreddits=['IndianFashionAddicts', 'IndianBeautyDeals'], 
        limit=200
    )
    
    if reddit_data:
        datalake.save_raw_data("reddit", reddit_data)
        processed_reddit = normalizer.process_batch(reddit_data)
        datalake.save_processed_data("reddit", processed_reddit)
        
        analyzed_reddit = gemini_analyzer.process_batch(processed_reddit)
        datalake.save_analyzed_data("reddit", analyzed_reddit)
        
    # ---------------------------------------------------------
    # 3. YouTube Ingestion
    # ---------------------------------------------------------
    print("\n--- 3. YouTube API Ingestion ---")
    youtube_scraper = YouTubeScraper() # Will use mock data if keys are absent
    
    # Dynamically search for videos instead of hardcoding
    discovered_videos = youtube_scraper.search_videos(
        query="Nykaa fashion try on haul", 
        max_results=3
    )
    
    if discovered_videos:
        youtube_data = youtube_scraper.fetch_comments(
            video_ids=discovered_videos, 
            max_results=100
        )
        
        if youtube_data:
            datalake.save_raw_data("youtube", youtube_data)
            processed_youtube = normalizer.process_batch(youtube_data)
            datalake.save_processed_data("youtube", processed_youtube)
            
            analyzed_youtube = gemini_analyzer.process_batch(processed_youtube)
            datalake.save_analyzed_data("youtube", analyzed_youtube)
    else:
        print("No YouTube videos found.")
        
    # ---------------------------------------------------------
    # 4. Internal PDP Ingestion
    # ---------------------------------------------------------
    print("\n--- 4. Internal PDP Q&A Ingestion ---")
    pdp_connector = InternalPDPConnector(db_connection_string="mock://nykaa_internal_db")
    pdp_data = pdp_connector.fetch_verified_qa(
        product_ids=['PID_89324', 'PID_10923']
    )
    
    if pdp_data:
        datalake.save_raw_data("pdp_internal", pdp_data)
        processed_pdp = normalizer.process_batch(pdp_data)
        datalake.save_processed_data("pdp_internal", processed_pdp)
        
        analyzed_pdp = gemini_analyzer.process_batch(processed_pdp)
        datalake.save_analyzed_data("pdp_internal", analyzed_pdp)
        
    print("\n=== Phases 1 & 2 Completed! ===\n")
    
    # ---------------------------------------------------------
    # Phase 3: Insight Generation & Quantification
    # ---------------------------------------------------------
    print("=== Starting Phase 3: Analytics & Impact Sizing ===")
    
    # Step 3.1: Hesitation Clustering
    clusterer = HesitationClusterer()
    clusterer.load_analyzed_data()
    clusterer.generate_embeddings()
    clusters = clusterer.cluster()
    clusterer.save_clusters()
    
    # Step 3.2: Drop-off Root Cause Analysis
    root_cause_analyzer = DropOffAnalyzer()
    rc_analysis = root_cause_analyzer.analyze(clusters)
    root_cause_analyzer.save_analysis(rc_analysis)
    
    # Step 3.3: Impact Sizing Model
    impact_scorer = ImpactScorer()
    impact_scorer.score(clusters, rc_analysis, total_analyzed_records=len(clusterer.records))
    report_path, _ = impact_scorer.save_report()
    
    # ---------------------------------------------------------
    # Phase 4: Insight Validation Layer & Quality Control
    # ---------------------------------------------------------
    print("\n=== Starting Phase 4: Insight Validation Layer ===")
    validator = InsightValidator()
    validator.validate_insights(report_path)
    
    print("\n=== Full Pipeline Completed Successfully! ===")

if __name__ == "__main__":
    run_phase1_pipeline()
