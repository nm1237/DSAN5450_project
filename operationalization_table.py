import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Manual coding based on close reading of each policy's algo_sentences output.
# Indicators assess how explicitly each policy discloses algorithmic data practices.
# Coding scale: "Yes" = explicit disclosure, "Partial" = vague/implied, "No" = absent.

INDICATORS = [
    "Names specific algorithmic feature(s)",
    "States what data inputs feed the algorithm",
    "States what outcome the algorithm optimizes for",
    "Uses the word 'algorithm' explicitly",
    "Acknowledges ML/AI model training on user data",
    "Discloses behavioral profiling for ad targeting",
    "Provides algorithmic opt-out mechanism",
    "Cross-platform data used for algorithmic targeting",
    "Defines algorithmic terms in the policy",
]

# Coding rationale per platform:
# Meta: mentions "Feed/Reels/Stories" but never calls them algorithms; extensive behavioral
#       data list but never connects it to recommendation logic; no opt-out from feed ranking.
# TikTok: names "For You" feed; acknowledges ML training; no opt-out from FYP; says
#         "we do not engage in profiling...as defined under applicable law" (narrow disclaimer).
# YouTube: most transparent — defines "algorithm" in glossary, explicit opt-out controls,
#          names recommendation and search systems; acknowledges cross-Google data use.
# X: never uses the word "algorithm"; ML training disclosed; no opt-out for content ranking;
#    uses "infer" heavily but vaguely.
# Snapchat: most explicit on feature names (Spotlight, Snap Map) and provides concrete
#           example of recommendation logic; defines ML models; opt-out for ads only.

TABLE = {
    "Indicator": INDICATORS,
    "Meta": [
        "Partial",  # names Feed/Reels/Stories but not as algorithms
        "Yes",      # extensive behavioral data list
        "No",       # never states optimization objective
        "No",       # never uses the word "algorithm"
        "Partial",  # "support research in...AI and machine learning"
        "Yes",      # "profiling" mentioned for legal protections
        "Partial",  # ad preferences only, not feed ranking
        "Yes",      # explicit cross-Meta-company sharing for personalization
        "No",       # no definitions section
    ],
    "TikTok": [
        "Partial",  # "For You" feed named but not described mechanically
        "Partial",  # mentions interaction data but vague on specifics
        "No",       # no optimization objective stated
        "Yes",      # "algorithms" used once in ML training context
        "Yes",      # "train, test, and improve...machine learning models and algorithms"
        "Partial",  # claims no "profiling...as defined under applicable law" (legalistic)
        "No",       # no opt-out from FYP recommendation algorithm
        "Partial",  # third-party data mentioned but mechanism vague
        "No",       # no definitions
    ],
    "YouTube": [
        "Yes",      # recommendation system and search named explicitly
        "Yes",      # "videos you watch", "searches", "web & app activity"
        "Partial",  # "more relevant results" — vague but present
        "Yes",      # defines "algorithm" in glossary
        "Partial",  # no explicit training disclosure
        "Yes",      # "profiling and targeted advertising" rights acknowledged
        "Yes",      # explicit opt-outs for personalization and signed-out search
        "Yes",      # cross-Google-services data use explicit
        "Yes",      # defines "algorithm" and "sensitive categories"
    ],
    "X": [
        "No",       # no specific algorithmic product named
        "Partial",  # behavioral inferences mentioned but vague
        "No",       # no optimization objective stated
        "No",       # never uses the word "algorithm"
        "Yes",      # "train our machine learning or artificial intelligence models"
        "No",       # no profiling disclosure
        "No",       # no opt-out for content ranking
        "Partial",  # ad partner data combined with user data
        "No",       # no definitions
    ],
    "Snapchat": [
        "Yes",      # Spotlight, Snap Map, "recommendation algorithms" named
        "Yes",      # explicit example: sports content → sports prioritized
        "Partial",  # "personalization, advertising, safety and security" listed
        "Yes",      # "recommendation algorithms", "algorithms and machine learning models"
        "Yes",      # "develop and improve the algorithms and machine learning models"
        "Partial",  # "infer your interests" for ads; no explicit profiling label
        "Partial",  # ad settings opt-out; not opt-out from content recommendations
        "Partial",  # third-party ad data mentioned but limited detail
        "Partial",  # defines "machine learning models" in parenthetical
    ],
}

df = pd.DataFrame(TABLE)
df.to_csv("outputs/operationalization_table.csv", index=False)
print(df.to_string(index=False))

# Heatmap visualization
COLOR_MAP = {"Yes": 2, "Partial": 1, "No": 0}
platforms = ["Meta", "TikTok", "YouTube", "X", "Snapchat"]
numeric = df[platforms].map(lambda x: COLOR_MAP[x])

fig, ax = plt.subplots(figsize=(10, 6))
cmap = plt.cm.get_cmap("RdYlGn", 3)
im = ax.imshow(numeric.values, cmap=cmap, vmin=-0.5, vmax=2.5, aspect="auto")

ax.set_xticks(range(len(platforms)))
ax.set_xticklabels(platforms, fontsize=11)
ax.set_yticks(range(len(INDICATORS)))
ax.set_yticklabels(INDICATORS, fontsize=9)

for i in range(len(INDICATORS)):
    for j in range(len(platforms)):
        val = df[platforms[j]].iloc[i]
        ax.text(j, i, val, ha="center", va="center", fontsize=8,
                color="black" if val == "Partial" else "white")

patches = [
    mpatches.Patch(color=cmap(2 / 2.5), label="Yes — explicit disclosure"),
    mpatches.Patch(color=cmap(1 / 2.5), label="Partial — vague or implied"),
    mpatches.Patch(color=cmap(0 / 2.5), label="No — absent"),
]
ax.legend(handles=patches, bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
ax.set_title("Table of Operationalization: Algorithmic Disclosure Indicators\nAcross Social Media Privacy Policies",
             fontsize=11, pad=12)
plt.tight_layout()
plt.savefig("outputs/operationalization_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()

print("\nSaved: outputs/operationalization_table.csv")
print("Saved: outputs/operationalization_heatmap.png")
