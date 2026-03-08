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
# clean data
# ------------------------------#
# clean GDPperCapita
df = pd.read_csv(RAW / "GDP per capita (constant 2015USD).csv")
df = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={"Country Name": "countryname"})

year_cols = [col for col in df.columns if str(col).isdigit()]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(id_vars=["countryname"], var_name="year", value_name="GDPperCapita")
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "gdp.csv", index=False)

# clean GDP growth
df = pd.read_csv(RAW / "GDP growth.csv")
df = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={"Country Name": "countryname"})

year_cols = [col for col in df.columns if str(col).isdigit()]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(id_vars=["countryname"], var_name="year", value_name="GDPgrowth")
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "gdp_growth.csv", index=False)

# clean Manufacturing share
df = pd.read_csv(RAW / "Manufacturing share.csv")
df = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={"Country Name": "countryname"})

year_cols = [col for col in df.columns if str(col).isdigit()]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(id_vars=["countryname"], var_name="year", value_name="Manushare")
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "Manushare.csv", index=False)

# clean trade
df = pd.read_csv(RAW / "Trade.csv")
df = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={"Country Name": "countryname"})

year_cols = [col for col in df.columns if str(col).isdigit()]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(id_vars=["countryname"], var_name="year", value_name="trade")
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "Trade.csv", index=False)

# clean secondary school enrollment
df = pd.read_csv(RAW / "secondary.csv")
df = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={"Country Name": "countryname"})

year_cols = [col for col in df.columns if str(col).isdigit()]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(id_vars=["countryname"], var_name="year", value_name="schoolsec")
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "secondary.csv", index=False)

# clean tertiary school enrollment
df = pd.read_csv(RAW / "tertiary.csv")
df = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={"Country Name": "countryname"})

year_cols = [col for col in df.columns if str(col).isdigit()]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(id_vars=["countryname"], var_name="year", value_name="schoolter")
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "tertiary.csv", index=False)

# ------------------------------#
# merge data
# ------------------------------#
gdp = pd.read_csv(INT / "gdp.csv")
gdp_growth = pd.read_csv(INT / "gdp_growth.csv")
manushare = pd.read_csv(INT / "Manushare.csv")
trade = pd.read_csv(INT / "Trade.csv")
secondary = pd.read_csv(INT / "secondary.csv")
tertiary = pd.read_csv(INT / "tertiary.csv")

final_panel = gdp.merge(gdp_growth, on=["countryname", "year"], how="outer")
final_panel = final_panel.merge(manushare, on=["countryname", "year"], how="outer")
final_panel = final_panel.merge(trade, on=["countryname", "year"], how="outer")
final_panel = final_panel.merge(secondary, on=["countryname", "year"], how="outer")
final_panel = final_panel.merge(tertiary, on=["countryname", "year"], how="outer")

final_panel.to_excel(OUT / "final_panel.xlsx", index=False)
