from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------#
# 0. Paths
# ------------------------------#
CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
RAW = ROOT / "raw"
INT = ROOT / "intermediate"
DATA = ROOT / "data_cleaning"
OUT = ROOT / "output"

# ------------------------------#
# 1. Descriptive Statistics
# ------------------------------#

df = pd.read_csv(DATA / "final_panel.csv")

df['paper_per_capita'] = df['paper_writing'] / df['population']
df["log_GDPperCapita"] = np.log(df["GDPperCapita"])
df["log_urbanpop"] = np.log(df["urbanpop"])


vars = [
    "paper_writing",
    "paper_all",
    "GDPperCapita",
    "GDPgrowth",
    "internetUsers",
    "urbanpop",
    "population",
    "Manushare",
    "trade",
"paper_per_capita",
]

summary = df[vars].describe().T

summary.to_csv(OUT / "summary_statistics.csv")

# ----------------------------------------------------------#
# Correlation Heatmap
# ----------------------------------------------------------#


corr = df[vars].corr()

plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Matrix")

plt.savefig(OUT / "correlation_heatmap.png", dpi=300)
plt.show()

missing = df[vars].isnull().sum()

summary.to_csv(OUT / "summary_statistics.csv")


