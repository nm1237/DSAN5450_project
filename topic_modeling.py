import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

PLATFORMS = ["meta", "tiktok", "youtube", "x", "snapchat"]

docs = []
available = []
for p in PLATFORMS:
    path = f"data/raw/{p}.txt"
    if not os.path.exists(path):
        print(f"MISSING: {path} — skipping {p}")
        continue
    with open(path, encoding="utf-8") as f:
        docs.append(f.read())
    available.append(p)

os.makedirs("outputs", exist_ok=True)

# TF-IDF vectorize
vectorizer = TfidfVectorizer(
    max_df=0.95,
    min_df=1,
    stop_words="english",
    max_features=2000
)
tfidf = vectorizer.fit_transform(docs)

# NMF with 8 topics
n_topics = 8
nmf = NMF(n_components=n_topics, random_state=42, max_iter=500)
W = nmf.fit_transform(tfidf)
H = nmf.components_

feature_names = vectorizer.get_feature_names_out()

# Print and save top words per topic
topic_data = []
print("=== NMF Topics ===\n")
for i, topic in enumerate(H):
    top_words = [feature_names[j] for j in topic.argsort()[-12:][::-1]]
    print(f"Topic {i+1}: {', '.join(top_words)}")
    topic_data.append({"topic": i + 1, "top_words": ", ".join(top_words)})

pd.DataFrame(topic_data).to_csv("outputs/nmf_topics.csv", index=False)

# Heatmap of platform-topic weights
W_df = pd.DataFrame(W, index=available, columns=[f"T{i+1}" for i in range(n_topics)])
fig, ax = plt.subplots(figsize=(10, 4))
sns.heatmap(W_df, annot=True, fmt=".2f", cmap="Blues", ax=ax)
ax.set_title("Platform-Topic Weight Matrix (NMF)")
plt.tight_layout()
plt.savefig("outputs/nmf_heatmap.png", dpi=150)
plt.close()

print("\nSaved: outputs/nmf_topics.csv")
print("Saved: outputs/nmf_heatmap.png")
