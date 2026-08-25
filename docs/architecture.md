# Nykaa Fashion Discovery Engine: System Architecture

## 1. High-Level Architecture Overview

The Nykaa Fashion Discovery Engine is designed as a multi-stage data processing pipeline. It ingests unstructured text from diverse fashion communities and customer feedback channels, processes it using advanced NLP, and outputs quantified, validated strategic insights.

```mermaid
graph TD
    %% Data Sources
    subgraph Data Sources
        A1[App/Play Store Reviews]
        A2[Reddit Communities r/IFA]
        A3[YouTube Haul Comments]
        A4[PDP Verified Q&A]
    end

    %% Ingestion Layer
    subgraph 1. Data Ingestion Layer
        B1[Data Connectors & Scrapers]
        B2[Data Normalization & Cleaning]
        B3[Raw Text Storage Data Lake]
    end

    %% NLP Processing Layer
    subgraph 2. NLP & Processing Layer
        C1[Aspect-Based Sentiment]
        C2[Barrier Classification Engine]
        C3[Sizing & Fabric NER]
    end

    %% Insight Generation Layer
    subgraph 3. Insight Generation & Quantification
        D1[Hesitation Clustering]
        D2[Drop-off Root Cause Analysis]
        D3[Impact Sizing & Volume Scoring]
    end

    %% Validation Layer
    subgraph 4. Insight Validation Layer
        E1[Cross-Platform Triangulation]
        E2[1.5% Volume Threshold Filter]
        E3[Dual-Model Verification]
        E4[Operational Reality Check]
    end

    %% Output
    subgraph 5. Strategic Export
        F1[Friction Point Identification]
        F2[Opportunity Sizing Dashboard]
        F3[Comparative Analysis Reports]
    end

    %% Connections
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    
    B1 --> B2 --> B3
    
    B3 --> C1
    B3 --> C2
    B3 --> C3
    
    C1 --> D1
    C2 --> D1
    C3 --> D1
    
    D1 --> D2 --> D3
    
    D3 --> E1
    D3 --> E2
    D3 --> E3
    D3 --> E4
    
    E1 --> F1
    E2 --> F1
    E3 --> F2
    E4 --> F3
```

## 2. Component Breakdown

### 2.1 Data Ingestion Layer
This layer is responsible for gathering unstructured data from multiple off-platform and on-platform sources.
- **Connectors & APIs:** Automated pipelines pulling data from App Store, Google Play Store, Reddit (e.g., `r/IndianFashionAddicts`, `r/IndianBeautyDeals`), and YouTube APIs.
- **Normalization:** Cleansing raw text (removing emojis, correcting spelling, standardizing fashion terminology).
- **Storage:** Storing raw and pre-processed text in a scalable Data Lake for batch processing.

### 2.2 NLP & Processing Layer
The core AI processing layer that transforms raw text into structured attributes.
- **Aspect-Based Sentiment Analysis (ABSA):** Identifies specific product aspects (e.g., "fabric", "zipper", "length") and assigns sentiment scores to each, going beyond generic review sentiment.
- **Barrier Classification:** Categorizes identified issues into core barrier types:
    - Fit, Fabric & Drape Uncertainty
    - Choice Paralysis & Comparison Friction
    - Styling Ambiguity
    - Taxonomy & Segment Intent Disconnect
- **Sizing & Fabric NER:** Uses Named Entity Recognition to extract specific physical attributes mentioned by users (e.g., "5'4 height", "bust size", "cotton blend").

### 2.3 Insight Generation & Opportunity Quantification
This layer aggregates processed data to find meaningful patterns and sizes their business impact.
- **Hesitation Clustering:** Groups similar complaints and doubts using embedding-based clustering to identify emerging trends.
- **Root Cause Analysis:** Maps clustered hesitations to specific points in the user journey (e.g., dropping off at the wishlist stage vs. checkout).
- **Opportunity Sizing:** Assigns a statistical weight to each barrier based on occurrence volume, allowing product teams to prioritize fixes based on potential GMV impact.

### 2.4 Insight Validation Layer (Quality Control)
To prevent AI hallucinations and ensure statistical significance, all insights must pass through four strict checkpoints:
1. **Cross-Platform Triangulation:** Insights must be validated across at least two independent data streams (e.g., a Reddit complaint must also appear in Play Store reviews).
2. **The 1.5% Volume Threshold:** Filtering out edge cases; a friction point must represent at least 1.5% of total categorized feedback to be flagged.
3. **Dual-Model Verification:** A two-tier Large Language Model (LLM) architecture. An *extractive* model pulls raw quotes, while a *secondary evaluator* model checks the synthesis to ensure no external hallucinations were introduced.
4. **Operational Reality Check:** Cross-referencing qualitative text insights with internal Nykaa platform metrics (e.g., mapping user doubts about "fabric sheer" to actual return/exchange rates for that category).

## 3. Output & Export (Strategic Intelligence)
The final stage exports the validated data into actionable formats for the product and growth teams:
- **Friction Point Dashboards:** Clear visualization of why users are hesitating.
- **Prioritization Matrices:** Opportunities ranked by their quantified impact on the 30-day wishlist conversion metric.
- **Segment Benchmarking:** Comparative analysis across different user cohorts (e.g., Gen-Z Trend Hunters vs. Premium Occasion Shoppers).
