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
DATA = ROOT / "data_cleaning"

# ------------------------------#
# 1. Descriptive Statistics
# ------------------------------#

df = pd.read_csv(DATA / "final_panel.csv")

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

summary.to_csv(OUT / "summary_statistics.csv")

