"""RQ1 Part B — word cloud of the diversity & inclusion definitions.

Specification 02 §B. Seeded with `np.random.seed(42)` and
`WordCloud(random_state=42)` (Spec 00 §3) so the layout is deterministic.

Run from `scripts/RQ1/`.
"""

import os
import warnings

import matplotlib

matplotlib.use("Agg")  # headless / autonomous execution

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch  # noqa: F401  (imported by the upstream script)
from wordcloud import STOPWORDS, WordCloud

warnings.filterwarnings("ignore")

np.random.seed(42)

DATA_PATH = "../../data/diversity_cloud.csv"
OUTPUT_DIR = "../../results/RQ1"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "diversitycloud.png")

CUSTOM_STOPWORDS = [
    "a", "an", "and", "the", "to", "of", "in", "for", "on", "with", "is", "it",
    "this", "that", "we", "i", "you", "they", "github", "code", "project",
    "use", "using", "without", "someone", "based", "people", "person", "etc",
    "act", "action",
]

SEED = 42


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    text = " ".join(df.iloc[:, 1].dropna().astype(str))

    stopwords = set(STOPWORDS)
    stopwords.update(CUSTOM_STOPWORDS)

    wc = WordCloud(
        width=1200,
        height=900,
        background_color="white",
        stopwords=stopwords,
        random_state=SEED,
    ).generate(text)

    plt.figure()
    plt.imshow(wc)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Word cloud built from {df.iloc[:, 1].dropna().shape[0]} answers")
    print(f"Figure written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
