# Nykaa Fashion Discovery Engine: Edge Cases & Mitigations

This document outlines potential edge cases, system vulnerabilities, and data anomalies that could disrupt the Nykaa Fashion Discovery Engine, along with specific engineering and architectural mitigations designed to handle them.

---

## 1. Data Ingestion & Preprocessing (Phase 1)

### 1.1 Code-Switching and "Hinglish"
**Edge Case:** A significant portion of the Indian user base writes reviews mixing Hindi and English (e.g., *"Fabric bahut achha hai but fit thoda tight hai"*). Standard Western NLP models will fail to parse this accurately.
**Mitigation:** The Text Normalization Engine (Step 1.4) must incorporate an Indic NLP transliteration layer. Furthermore, the base LLM used for extraction should be explicitly fine-tuned on a localized Hinglish corpus rather than relying solely on standard English models.

### 1.2 Sarcasm and Nuanced Slang
**Edge Case:** Users employing sarcasm to express dissatisfaction (e.g., *"Wow, great job Nykaa making a dress that fits absolutely no one"*). Standard sentiment analysis might misclassify "great job" as positive.
**Mitigation:** The Aspect-Based Sentiment Analysis (ABSA) model (Step 2.1) must be trained on datasets containing sarcastic fashion discourse. The Dual-Model Verification layer (Step 4.3) will act as a secondary net to catch contextual discrepancies.

### 1.3 Bot Attacks & Fake Review Spam
**Edge Case:** Competitors or malicious actors deploying bots to flood a product with fake negative or positive reviews, skewing the overall data pool.
**Mitigation:** Introduce a pre-processing anomaly detection filter before the NLP layer. This filter will flag and quarantine text bursts that exhibit sudden, high-velocity identical sentiment, repetitive phrasing, or come from unverified accounts.

---

## 2. NLP & ML Processing (Phase 2)

### 2.1 Ambiguous Coreference Resolution
**Edge Case:** A user reviews a multi-item purchase or a co-ord set but uses ambiguous pronouns (e.g., *"I bought the top and the skirt. It was way too sheer."*). The engine cannot determine which item is sheer.
**Mitigation:** The NLP pipeline must include a robust coreference resolution step to trace pronouns back to the correct Named Entity. If the ambiguity cannot be mathematically resolved with high confidence, the data point should be dropped rather than guessed.

### 2.2 Highly Conflicting Sentiments on the Same Product
**Edge Case:** For a specific dress, 50% of reviews claim it "runs large," while the other 50% claim it "runs small." A naive engine might average this out to "true to size," completely missing the problem.
**Mitigation:** The Insight Generation layer (Step 3.1) must not average opposing sentiments. Instead, it must recognize high-variance bi-modal distributions and cluster this as a new specific barrier: **"Inconsistent Sizing / Manufacturing Variance."**

---

## 3. Insight Generation & Validation (Phases 3 & 4)

### 3.1 The 1.5% Threshold & High-Risk Blind Spots
**Edge Case:** The engine filters out any friction point that doesn't meet the 1.5% volume threshold (Step 4.2). However, what if a rare issue is highly critical (e.g., a toxic dye causing skin rashes, or a zipper causing injury)? 
**Mitigation:** Implement a **Severity Override Bypass**. A predefined dictionary of high-risk keywords (*"rash"*, *"allergy"*, *"cut"*, *"bleeding color"*) will automatically bypass the volume threshold and be immediately escalated to the Strategic Dashboard as a high-priority alert.

### 3.2 AI Hallucinations in Summary Generation
**Edge Case:** The generative AI model summarizes a cluster of complaints by hallucinating a feature request. For example, reading *"I wish this had pockets like my other dress,"* and summarizing it as *"Users are reporting the pockets are broken."*
**Mitigation:** The Dual-Model Verification architecture (Step 4.3) handles this. The secondary Evaluator LLM is strictly prompted to verify if the claims made in the synthesized summary exist in the raw extractive quotes. If it detects a hallucination, the insight is regenerated.

### 3.3 Perception vs. Reality Disconnect (Metrics Mismatch)
**Edge Case:** The text analysis strongly indicates that users hate the fabric of a specific top, yet the internal return rates for that top are incredibly low. 
**Mitigation:** The Operational Reality Check (Step 4.4) is designed exactly for this. Instead of discarding the text insight, the dashboard will flag a **"Perception vs. Reality Gap."** This indicates users are keeping the item (perhaps due to hassle or low price) but are unsatisfied—which silently destroys Customer Lifetime Value (LTV). This requires a different product intervention than high-return items.

### 3.4 Seasonal Skewing
**Edge Case:** A massive spike in complaints about "fabric being too thick and unbreathable" during May (peak Indian summer) might heavily skew the yearly prioritization matrix, de-prioritizing other valid issues.
**Mitigation:** The Impact Sizing Model (Step 3.3) must apply temporal normalization. Insights should be weighted against the current season, and the dashboard should tag insights as either *Evergreen* or *Seasonally Dependent*.
