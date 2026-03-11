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
# 1. clean data
# ------------------------------#

# ------------------------------#
# clean GDPperCapita
# ------------------------------#

df = pd.read_csv(RAW / "GDP per capita (constant 2015USD).csv")
df = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={"Country Name": "countryname"})

year_cols = [col for col in df.columns if str(col).isdigit()]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(id_vars=["countryname"], var_name="year", value_name="GDPperCapita")
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "gdp.csv", index=False)

# ------------------------------#
# clean GDP growth
# ------------------------------#

df = pd.read_csv(RAW / "GDP growth.csv")
df = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={"Country Name": "countryname"})

year_cols = [col for col in df.columns if str(col).isdigit()]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(id_vars=["countryname"], var_name="year", value_name="GDPgrowth")
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "gdp_growth.csv", index=False)

# ------------------------------#
# clean Manufacturing share
# ------------------------------#

df = pd.read_csv(RAW / "Manufacturing share.csv")
df = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={"Country Name": "countryname"})

year_cols = [col for col in df.columns if str(col).isdigit()]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(id_vars=["countryname"], var_name="year", value_name="Manushare")
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "Manushare.csv", index=False)

# ------------------------------#
# clean trade share
# ------------------------------#

df = pd.read_csv(RAW / "Trade.csv")
df = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={"Country Name": "countryname"})

year_cols = [col for col in df.columns if str(col).isdigit()]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(id_vars=["countryname"], var_name="year", value_name="trade")
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "Trade.csv", index=False)

# ------------------------------#
# clean secondary school enrollment
# ------------------------------#

df = pd.read_csv(RAW / "secondary.csv")
df = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={"Country Name": "countryname"})

year_cols = [col for col in df.columns if str(col).isdigit()]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(id_vars=["countryname"], var_name="year", value_name="schoolsec")
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "secondary.csv", index=False)

# ------------------------------#
# clean tertiary school enrollment
# ------------------------------#

df = pd.read_csv(RAW / "tertiary.csv")
df = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={"Country Name": "countryname"})

year_cols = [col for col in df.columns if str(col).isdigit()]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(id_vars=["countryname"], var_name="year", value_name="schoolter")
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "tertiary.csv", index=False)

# ------------------------------#
# clean urban population
# ------------------------------#

df = pd.read_csv(RAW / "urban_population.csv", skiprows=4)

year_cols = [str(year) for year in range(1990, 2025)]
keep_cols = ["Country Name", "Country Code"] + year_cols
df = df[keep_cols]

df = df.rename(columns={
    "Country Name": "countryname",
    "Country Code": "countrycode"
})

df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(
    id_vars=["countryname", "countrycode"],
    var_name="year",
    value_name="urbanpop"
)

df["year"] = df["year"].str.replace("y", "", regex=False)
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["urbanpop"] = pd.to_numeric(df["urbanpop"], errors="coerce")

df.to_csv(INT / "urban_population.csv", index=False)

# ------------------------------#
# clean internet users
# ------------------------------#

df = pd.read_csv(RAW / "Internet_users.csv", skiprows=4)
df = df.drop(columns=["Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={
    "Country Name": "countryname",
    "Country Code": "countrycode"
})


year_cols = [str(year) for year in range(1990, 2025)]

df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(
    id_vars=["countryname", "countrycode"],
    var_name="year",
    value_name="internetUsers"
)

df["year"] = df["year"].str.replace("y", "", regex=False)
df["year"] = pd.to_numeric(df["year"], errors="coerce")

df.to_csv(INT / "internet_users.csv", index=False)

# ------------------------------#
# clean population
# ------------------------------#

df = pd.read_csv(RAW / "population.csv", header=2)
df = df.drop(columns=["Unnamed: 70"], errors="ignore")
df = df.drop(columns=["Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={
    "Country Name": "countryname",
    "Country Code": "countrycode"
})

year_cols = [col for col in df.columns if str(col).isdigit() and len(str(col)) == 4]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(
    id_vars=["countryname", "countrycode"],
    var_name="year",
    value_name="population"
)
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "population.csv", index=False)

# ------------------------------#
# clean paper consumption
# ------------------------------#

df = pd.read_csv(RAW / "paper_writing.csv")

df = (
    df.pivot_table(
        index=["Area", "Year"],
        columns="Element",
        values="Value",
        aggfunc="sum"
    )
    .reset_index()
)

name_map = {
    "Bahamas": "Bahamas, The",
    "Bolivia (Plurinational State of)": "Bolivia",
    "China, Hong Kong SAR": "Hong Kong SAR, China",
    "Curaçao": "Curacao",
    "Côte d'Ivoire": "Cote d'Ivoire",
    "Democratic Republic of the Congo": "Congo, Dem. Rep.",
    "Congo": "Congo, Rep.",
    "Egypt": "Egypt, Arab Rep.",
    "Gambia": "Gambia, The",
    "Iran (Islamic Republic of)": "Iran, Islamic Rep.",
    "Kyrgyzstan": "Kyrgyz Republic",
    "Lao People's Democratic Republic": "Lao PDR",
    "Micronesia (Federated States of)": "Micronesia, Fed. Sts.",
    "Netherlands (Kingdom of the)": "Netherlands",
    "Republic of Korea": "Korea, Rep.",
    "Republic of Moldova": "Moldova",
    "Saint Kitts and Nevis": "St. Kitts and Nevis",
    "Saint Lucia": "St. Lucia",
    "Saint Martin (French part)": "St. Martin (French part)",
    "Saint Vincent and the Grenadines": "St. Vincent and the Grenadines",
    "Slovakia": "Slovak Republic",
    "Somalia": "Somalia, Fed. Rep.",
    "Türkiye": "Turkiye",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "United Republic of Tanzania": "Tanzania",
    "United States of America": "United States",
    "Venezuela (Bolivarian Republic of)": "Venezuela, RB",
    "Yemen": "Yemen, Rep."
}

df["countryname"] = df["Area"].replace(name_map)


df["paper_writing"] = (
    df["Production"].fillna(0)
    + df["Import quantity"].fillna(0)
    - df["Export quantity"].fillna(0)
)

df = df[df["paper_writing"] >= 0]

df = df.rename(columns={"Year": "year"})
df["year"] = pd.to_numeric(df["year"], errors="coerce")

df = df[["countryname", "year", "paper_writing"]]

df.to_csv(INT / "paper_writing.csv", index=False)

df = pd.read_csv(RAW / "paper_all.csv")

df = (
    df.pivot_table(
        index=["Area", "Year"],
        columns="Element",
        values="Value",
        aggfunc="sum"
    )
    .reset_index()
)

name_map = {
    "Bahamas": "Bahamas, The",
    "Bolivia (Plurinational State of)": "Bolivia",
    "China, Hong Kong SAR": "Hong Kong SAR, China",
    "Curaçao": "Curacao",
    "Côte d'Ivoire": "Cote d'Ivoire",
    "Democratic Republic of the Congo": "Congo, Dem. Rep.",
    "Congo": "Congo, Rep.",
    "Egypt": "Egypt, Arab Rep.",
    "Gambia": "Gambia, The",
    "Iran (Islamic Republic of)": "Iran, Islamic Rep.",
    "Kyrgyzstan": "Kyrgyz Republic",
    "Lao People's Democratic Republic": "Lao PDR",
    "Micronesia (Federated States of)": "Micronesia, Fed. Sts.",
    "Netherlands (Kingdom of the)": "Netherlands",
    "Republic of Korea": "Korea, Rep.",
    "Republic of Moldova": "Moldova",
    "Saint Kitts and Nevis": "St. Kitts and Nevis",
    "Saint Lucia": "St. Lucia",
    "Saint Martin (French part)": "St. Martin (French part)",
    "Saint Vincent and the Grenadines": "St. Vincent and the Grenadines",
    "Slovakia": "Slovak Republic",
    "Somalia": "Somalia, Fed. Rep.",
    "Türkiye": "Turkiye",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "United Republic of Tanzania": "Tanzania",
    "United States of America": "United States",
    "Venezuela (Bolivarian Republic of)": "Venezuela, RB",
    "Yemen": "Yemen, Rep."
}

df["countryname"] = df["Area"].replace(name_map)


df["paper_all"] = (
    df["Production"].fillna(0)
    + df["Import quantity"].fillna(0)
    - df["Export quantity"].fillna(0)
)

df = df[df["paper_all"] >= 0]

df = df.rename(columns={"Year": "year"})
df["year"] = pd.to_numeric(df["year"], errors="coerce")

df = df[["countryname", "year", "paper_all"]]

df.to_csv(INT / "paper_all.csv", index=False)

# ------------------------------#
# clean population
# ------------------------------#
df = pd.read_csv(RAW / "population.csv", header=2)
df = df.drop(columns=["Unnamed: 70"], errors="ignore")
df = df.drop(columns=["Indicator Name", "Indicator Code"], errors="ignore")
df = df.rename(columns={
    "Country Name": "countryname",
    "Country Code": "countrycode"
})

year_cols = [col for col in df.columns if str(col).isdigit() and len(str(col)) == 4]
df = df.rename(columns={col: f"y{col}" for col in year_cols})

df = df.melt(
    id_vars=["countryname", "countrycode"],
    var_name="year",
    value_name="population"
)
df["year"] = df["year"].str.replace("y", "", regex=False).astype(int)

df.to_csv(INT / "population.csv", index=False)

# ------------------------------#
# 2. Merge
# ------------------------------#

# ------------------------------#
# 2.1 Read data from intermediate
# ------------------------------#

gdp = pd.read_csv(INT / "gdp.csv")
gdp_growth = pd.read_csv(INT / "gdp_growth.csv")
manushare = pd.read_csv(INT / "Manushare.csv")
trade = pd.read_csv(INT / "Trade.csv")
secondary = pd.read_csv(INT / "secondary.csv")
tertiary = pd.read_csv(INT / "tertiary.csv")

urban = pd.read_csv(INT / "urban_population.csv")
internet = pd.read_csv(INT / "internet_users.csv")

paper_writing = pd.read_csv(INT / "paper_writing.csv")
paper_all = pd.read_csv(INT / "paper_all.csv")
population = pd.read_csv(INT / "population.csv")

# ------------------------------#
# 2.2 Basic cleaning
# ------------------------------#

all_dfs = [urban, internet, gdp, gdp_growth, manushare, trade, secondary, tertiary, paper_writing, paper_all, population]

for df in all_dfs:
    df["countryname"] = df["countryname"].astype(str).str.strip()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

# ------------------------------#
# 2.3 Year filter
# ------------------------------#

for i, df in enumerate(all_dfs):
    all_dfs[i] = df[(df["year"] > 1989) & (df["year"] != 2025)]

urban, internet, gdp, gdp_growth, manushare, trade, secondary, tertiary, paper_writing, paper_all, population = all_dfs

# ------------------------------#
# 2.4 Merge all datasets
# ------------------------------#

final_panel = urban.merge(internet, on=["countryname", "year"], how="outer")
final_panel = final_panel.merge(gdp, on=["countryname", "year"], how="outer")
final_panel = final_panel.merge(gdp_growth, on=["countryname", "year"], how="outer")
final_panel = final_panel.merge(manushare, on=["countryname", "year"], how="outer")
final_panel = final_panel.merge(trade, on=["countryname", "year"], how="outer")
final_panel = final_panel.merge(secondary, on=["countryname", "year"], how="outer")
final_panel = final_panel.merge(tertiary, on=["countryname", "year"], how="outer")
final_panel = final_panel.merge(paper_writing, on=["countryname", "year"], how="outer")
final_panel = final_panel.merge(paper_all, on=["countryname", "year"], how="outer")
final_panel = final_panel.merge(population, on=["countryname", "year"], how="outer")

final_panel = final_panel.drop(columns=["countrycode", "countrycode_x", "countrycode_y"], errors="ignore")


final_panel = final_panel.dropna(subset=["GDPperCapita", "paper_writing", "internetUsers"])
final_panel.to_excel(OUT / "final_panel.xlsx", index=False)