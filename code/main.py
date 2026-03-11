from pathlib import Path
import pandas as pd

# ------------------------------#
# 0. Paths
# ------------------------------#
CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
RAW = ROOT / "raw"
INT = ROOT / "intermediate"
OUT = ROOT / "output"

# ------------------------------#
# 1. Descriptive Statistics
# ------------------------------#

df = pd.read_csv("../final_panel.csv")

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
]

summary = df[vars].describe().T

missing = df[vars].isnull().sum()

print("Summary statistics:")
print(summary)

print("\nMissing values:")
print(missing)

summary.to_csv(OUT / "summary_statistics.csv")
missing.to_csv(OUT / "missing_values.csv")