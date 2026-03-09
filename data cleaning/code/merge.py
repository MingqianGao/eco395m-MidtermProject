from pathlib import Path
import pandas as pd

# ------------------------------#
# 0. Paths
# ------------------------------#
CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
RAW = ROOT / "raw"
OUT = ROOT / "output"
INT = ROOT / "intermediate"


# ------------------------------#
# 1. Read data
# ------------------------------#
df1 = pd.read_csv(OUT / "urban_internet_merged.csv")
df2 = pd.read_csv(OUT / "paper_consumption_population.csv")
df3 = pd.read_excel(OUT / "gdpedu.xlsx")

# ------------------------------#
# 2. Basic cleaning
# ------------------------------#
for df in [df1, df2, df3]:
    df["countryname"] = df["countryname"].astype(str).str.strip()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")


# ------------------------------#
# 3. Year filter
# ------------------------------#
df1 = df1[(df1["year"] > 1994) & (df1["year"] != 2025)]
df2 = df2[(df2["year"] > 1994) & (df2["year"] != 2025)]
df3 = df3[(df3["year"] > 1994) & (df3["year"] != 2025)]


# ------------------------------#
# 4. Merge datasets
# ------------------------------#
m1 = df1.merge(
    df2,
    on=["countryname", "year"],
    how="left",
    indicator=True,
    validate="one_to_one"
)

m1 = m1[m1["_merge"] == "both"].drop(columns="_merge")

m2 = m1.merge(
    df3,
    on=["countryname", "year"],
    how="left",
    indicator=True,
    validate="one_to_one"
)

final = (
    m2[m2["_merge"] == "both"]
    .drop(columns="_merge")
    .sort_values(["countryname", "year"])
)


# ------------------------------#
# 5. Save
# ------------------------------#
final.to_excel(OUT / "final_dataset.xlsx", index=False)

print("Final dataset saved.")