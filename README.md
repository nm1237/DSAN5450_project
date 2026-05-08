# Consenting to the Algorithm
## How Social Media Privacy Policies Obscure Algorithmic Data Use and What Policymakers Should Do About It

**Course:** DSAN 5450 — Data Ethics and Policy, Georgetown University  
**Student:** Noelle M.

---

## Project Structure

```
5450 Final Project/
├── data/
│   ├── raw/          # Scraped .txt files (one per platform)
│   └── processed/    # Cleaned/tokenized versions if needed
├── outputs/          # All figures, CSVs, and sentence files
├── paper/
│   └── draft.md      # Written paper
├── collect_policies.py     # Phase 1 — Data Collection
├── readability_analysis.py # Phase 2 — Readability Analysis
├── topic_modeling.py       # Phase 3 — NMF Topic Modeling
├── keyword_analysis.py     # Phase 4 — Keyword/Clause Analysis
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

## Running the Pipeline

```bash
python collect_policies.py
python readability_analysis.py
python topic_modeling.py
python keyword_analysis.py
```

## Platforms Analyzed
- Meta (Facebook/Instagram)
- TikTok
- YouTube (Google)
- X (Twitter)
- Snapchat
