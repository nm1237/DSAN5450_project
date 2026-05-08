import requests
from bs4 import BeautifulSoup
import os
import re

POLICIES = {
    "meta":     "https://www.facebook.com/privacy/policy/",
    "tiktok":   "https://www.tiktok.com/legal/page/us/privacy-policy/en",
    "youtube":  "https://policies.google.com/privacy",
    "x":        "https://x.com/en/privacy",
    "snapchat": "https://values.snap.com/privacy/privacy-policy",
}

os.makedirs("data/raw", exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

for name, url in POLICIES.items():
    print(f"Fetching {name}...")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "lxml")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) < 500:
            print(f"  WARNING: {name} returned very little text ({len(text)} chars) — likely JS-rendered. Manual copy needed.")
        else:
            with open(f"data/raw/{name}.txt", "w", encoding="utf-8") as f:
                f.write(text)
            print(f"  Saved {name}: {len(text):,} chars")
    except Exception as e:
        print(f"  ERROR fetching {name}: {e}")

print("\nDone. Check data/raw/ for results.")
print("Any platform showing a WARNING needs to be manually copied — see README for instructions.")
