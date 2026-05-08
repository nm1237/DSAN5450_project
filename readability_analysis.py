import textstat
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PLATFORMS = ["meta", "tiktok", "youtube", "x", "snapchat"]

os.makedirs("outputs", exist_ok=True)

results = []
for p in PLATFORMS:
    path = f"data/raw/{p}.txt"
    if not os.path.exists(path):
        print(f"MISSING: {path} — skipping {p}")
        continue
    with open(path, encoding="utf-8") as f:
        text = f.read()
    results.append({
        "platform": p,
        "flesch_ease":      textstat.flesch_reading_ease(text),
        "fk_grade":         textstat.flesch_kincaid_grade(text),
        "fog_index":        textstat.gunning_fog(text),
        "smog":             textstat.smog_index(text),
        "dale_chall":       textstat.dale_chall_readability_score(text),
        "word_count":       textstat.lexicon_count(text),
        "avg_sentence_len": textstat.avg_sentence_length(text),
    })

df = pd.DataFrame(results)
df.to_csv("outputs/readability_scores.csv", index=False)
print(df.to_string(index=False))

# Bar chart — FK Grade Level
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=df, x="platform", y="fk_grade", palette="Blues_d", ax=ax)
ax.axhline(8, color="red", linestyle="--", label="8th grade benchmark")
ax.axhline(12, color="orange", linestyle="--", label="12th grade benchmark")
ax.set_title("Flesch-Kincaid Grade Level by Platform")
ax.set_ylabel("Grade Level")
ax.set_xlabel("")
ax.legend()
plt.tight_layout()
plt.savefig("outputs/readability_fk_grade.png", dpi=150)
plt.close()
print("\nSaved: outputs/readability_scores.csv")
print("Saved: outputs/readability_fk_grade.png")
