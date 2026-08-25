# Nykaa Fashion Discovery Engine: Problem Statement

## 1. Context & Strategic Anchor
Nykaa Fashion has established itself as India's premier destination for curated style, designer edits, and premium apparel. Millions of fashion-forward shoppers browse the platform daily, actively discovering products, curating aspirational wardrobes, and adding high-affinity merchandise to their wishlists. A wishlist represents one of the strongest explicit signals of user interest on the platform—far outperforming passive catalog browsing in commercial intent.

However, despite this high accumulation of saved items, user behavior frequently encounters an intent freeze. Shoppers curate dozens—or even hundreds—of items that remain permanently dormant in their wishlist "graveyard," with only a small fraction converting into an order within 30 days. This cognitive stalling degrades conversion velocity, ties up high-intent platform demand, and dampens Customer Lifetime Value (LTV).

To unlock organic Gross Merchandise Value (GMV) growth without escalating Customer Acquisition Costs (CAC), Nykaa Fashion's Growth Team must increase the percentage of users who purchase at least one item from their wishlist within 30 days. Under a strict strategic constraint of zero monetary incentives (no flash discounts, coupons, or cashback), conversion must be unlocked entirely by deeply understanding residual doubts and uncovering actionable intelligence.

## 2. The Core Problem Statement
> "How might we analyze unstructured customer feedback and off-platform fashion discourse at scale to uncover the cognitive, physical, and psychological uncertainties preventing wishlist hoards from converting into purchases within 30 days?"

## 3. Objectives of the AI Engine
The proposed AI Engine will ingest vast streams of unstructured text across App/Play Store reviews, Reddit communities (r/IndianFashionAddicts, r/IndianBeautyDeals), YouTube try-on haul comments, and verified Product Display Page (PDP) Q&As. The AI engine must go beyond simply summarizing reviews or performing basic sentiment analysis. It is designed to identify, quantify where possible, and compare potential opportunity areas that could positively influence the target business metric across four foundational pillars:

- **The Fit, Fabric & Drape Uncertainty Barrier:** Uncover the residual physical doubts that persist after viewing studio-lit PDPs. Do users hesitate because model photos fail to reflect diverse Indian body proportions (height < 5'4", bust/waist ratios)? Is there fear regarding fabric opacity, stretch, or color distortion under daylight?
- **The Choice Paralysis & Comparison Friction:** Map why shortlisted items decay into inactive bookmarks. When a user wishlists 5 near-identical tops across different brands, what cognitive friction prevents selection? Does the app lack side-by-side spec evaluation tools (fabric blend, lining, wash care)?
- **Styling Ambiguity & Asynchronous Validation:** Identify why standalone items are postponed. Does the user lack styling confidence ("what shoes/bag do I pair this with?") or drop off after screenshotting items to solicit slow opinions from friends on WhatsApp?
- **Taxonomy & Segment Intent Disconnect:** Differentiate active, time-sensitive intent (upcoming wedding/event) from passive aesthetic mood-boarding across distinct cohorts (e.g., Gen-Z Trend Hunters vs. Premium Occasion Shoppers).

## 4. Data Architecture & Processing Blueprint
The AI Engine operationalizes raw text into strategic intelligence by routing data through four distinct, automated processing layers:

1. **DATA INGESTION:** App/Play Store Reviews, Reddit (r/IFA), YouTube Hauls, PDP Verified Q&A
2. **NLP & PROCESSING:** Aspect-Based Sentiment, Barrier Classification, Sizing & Fabric NER
3. **INSIGHT GENERATION:** Hesitation Clustering, Drop-off Root Cause, Intent vs Bookmark Scoring
4. **OPPORTUNITY QUANTIFICATION:** Impact Sizing of Friction Points, Intervention Comparison, Strategic Export

## 5. Expected Output & Business Impact
The output of this AI engine serves as a dynamic intelligence layer feeding directly into Nykaa Fashion’s growth roadmap. Instead of building specific app features, the engine provides the foundational data required to prioritize behavioral solutions:

- **Friction Point Identification:** Pinpointing exactly why users hesitate at the final step (e.g., fit anxiety, fabric uncertainty, styling doubts) rather than just logging negative sentiment.
- **Opportunity Sizing & Quantification:** Assigning statistical weight and volume to each identified barrier, allowing product teams to prioritize fixes based on potential conversion impact.
- **Comparative Analysis:** Benchmarking different user segments and product categories to uncover where interventions will yield the highest GMV return.
- **Target Business Metric Alignment:** Uncovering actionable intelligence designed specifically to increase the percentage of users who convert ≥1 item from their wishlist within 30 days of addition by +15% to +20%, driving repeat purchase frequency without margin-eroding discounts.

## 6. Insight Validation Layer (Quality Control)
To guarantee that the discovery engine generates high-confidence, statistically sound product opportunities rather than over-indexing on edge cases or AI hallucinations, it implements four strict verification checkpoints:

- **Cross-Platform Triangulation:** An insight is only classified as high-confidence if validated across at least two independent data streams (e.g., sizing complaints on Reddit matching Play Store return commentary).
- **The 1.5% Volume Threshold:** One-off complaints are filtered out. A specific friction point must account for at least 1.5% of total categorized feedback within a product category to be designated as an actionable product opportunity.
- **Dual-Model Verification:** The engine utilizes a two-tier LLM verification architecture where an extractive model captures raw quotes/attributes and a secondary evaluator validates that synthesis introduces no external hallucinations.
- **Operational Reality Check:** Qualitative hesitation trends are cross-referenced with internal platform metrics (e.g., pairing user doubts about fabric sheer/fit with actual category-level return and exchange rates) to decouple perception from catalog reality.
