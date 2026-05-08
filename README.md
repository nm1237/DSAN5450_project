# Consenting to the Algorithm
## How Social Media Privacy Policies Obscure Algorithmic Data Use and What Policymakers Should Do About It

**Course:** DSAN 5450 — Data Ethics and Policy, Georgetown University  
**Author:** Noelle Martell  
**Live site:** https://nm1237.github.io/DSAN5450_project/

---

## Project Structure

```
5450 Final Project/
├── data/
│   └── raw/                      # Scraped .txt files and Meta PDF (one per platform)
├── outputs/                      # Figures, CSVs, and extracted sentence files
├── index.qmd                     # Quarto source document (full paper)
├── index.html                    # Rendered HTML (self-contained)
├── references.bib                # BibTeX citations
├── collect_policies.py           # Phase 1 — Data collection
├── readability_analysis.py       # Phase 2 — Readability scoring
├── topic_modeling.py             # Phase 3 — NMF topic modeling
├── keyword_analysis.py           # Phase 4 — Keyword density analysis
├── operationalization_table.py   # Phase 4 — Manual disclosure indicators
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
python operationalization_table.py
```

## Platforms Analyzed
- Meta (Facebook/Instagram)
- TikTok
- YouTube (Google)
- X (formerly Twitter)
- Snapchat
