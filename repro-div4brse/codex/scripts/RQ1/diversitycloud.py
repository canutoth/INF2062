import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from wordcloud import STOPWORDS, WordCloud

np.random.seed(42)
warnings.filterwarnings("ignore")

CSV_PATH = os.path.join("..", "..", "data", "diversity_cloud.csv")
OUT_DIR = os.path.join("..", "..", "results", "RQ1")

CUSTOM_STOPWORDS = "a an and the to of in for on with is it this that we i you they github code project use using without someone based people person etc act action".split()

os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH)
text = " ".join(df.iloc[:, 1].dropna().astype(str))

stopwords = STOPWORDS | set(CUSTOM_STOPWORDS)

wc = WordCloud(
    width=1200,
    height=900,
    background_color="white",
    stopwords=stopwords,
    random_state=42,
)
wc.generate(text)

plt.imshow(wc)
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "diversitycloud.png"), dpi=300, bbox_inches="tight")
plt.show()