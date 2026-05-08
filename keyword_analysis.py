import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PLATFORMS = ["meta", "tiktok", "youtube", "x", "snapchat"]

ALGO_TERMS = [
    # Original terms
    "algorithm", "recommend", "personali", "behavioral",
    "infer", "predict", "amplif", "engagement", "content ranking",
    "machine learning", "automated decision", "profil",
    # Added via vocabulary audit: platform-specific synonyms found in policy text
    "tailor",            # YouTube: "tailored to how you use our services"
    "customiz",          # YouTube: "customized search results", "customize our services"
    "for you",           # TikTok: "For You" feed — primary algorithmic product
    "targeted",          # Snapchat/TikTok: "targeted advertising", "target...ads"
    "automated system",  # YouTube: "automated systems that analyze your content"
    "automated process", # Meta: "automated processing" (not "automated decision")
    "curate",            # Meta: "curating" content
    "artificial intelligence",  # X/Snapchat: "AI models", "AI features"
    "ranking",           # general content ranking language
    "content moderation",# TikTok: "content moderation" via algorithmic systems
]

DATA_TERMS = [
    "collect", "data", "information", "store", "retain",
    "process", "share", "third party", "cookie", "device"
]

os.makedirs("outputs", exist_ok=True)

results = []
for p in PLATFORMS:
    path = f"data/raw/{p}.txt"
    if not os.path.exists(path):
        print(f"MISSING: {path} — skipping {p}")
        continue
    with open(path, encoding="utf-8") as f:
        text = f.read().lower()

    words = text.split()
    total_words = len(words)

    algo_hits = sum(text.count(t) for t in ALGO_TERMS)
    data_hits = sum(text.count(t) for t in DATA_TERMS)

    sentences = re.split(r"[.!?]", text)
    algo_sentences = [
        s.strip() for s in sentences
        if any(t in s for t in ALGO_TERMS) and len(s.split()) > 5
    ]

    results.append({
        "platform":            p,
        "total_words":         total_words,
        "algo_hits":           algo_hits,
        "data_hits":           data_hits,
        "algo_density":        round(algo_hits / total_words * 1000, 2),
        "data_density":        round(data_hits / total_words * 1000, 2),
        "algo_sentences_count": len(algo_sentences),
    })

    with open(f"outputs/algo_sentences_{p}.txt", "w", encoding="utf-8") as f:
        f.write(f"=== {p.upper()} — Sentences containing algorithmic language ===\n\n")
        for i, s in enumerate(algo_sentences, 1):
            f.write(f"{i}. {s}\n\n")

df = pd.DataFrame(results)
df.to_csv("outputs/keyword_analysis.csv", index=False)
print(df[["platform", "algo_hits", "data_hits", "algo_density", "data_density"]].to_string(index=False))

# Side-by-side density comparison
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.barplot(data=df, x="platform", y="algo_density", palette="Reds_d", ax=axes[0])
axes[0].set_title("Algorithmic Term Density\n(hits per 1,000 words)")
axes[0].set_xlabel("")
axes[0].set_ylabel("Density")

sns.barplot(data=df, x="platform", y="data_density", palette="Blues_d", ax=axes[1])
axes[1].set_title("General Data Term Density\n(hits per 1,000 words)")
axes[1].set_xlabel("")
axes[1].set_ylabel("")

plt.suptitle("Algorithmic vs. Data Language Density Across Platforms", fontsize=12, y=1.01)
plt.tight_layout()
plt.savefig("outputs/keyword_density_comparison.png", dpi=150, bbox_inches="tight")
plt.close()

print("\nSaved: outputs/keyword_analysis.csv")
print("Saved: outputs/keyword_density_comparison.png")
print("Saved: outputs/algo_sentences_{platform}.txt for each platform")
