import pandas as pd

df = pd.read_csv("data cleaning/raw/urban_population.csv", skiprows=4)

print("Columns:")
print(df.columns.tolist())

year_cols = [col for col in df.columns if str(col).isdigit()]

df = df[["Country Name", "Country Code"] + year_cols]

df_long = df.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=year_cols,
    var_name="year",
    value_name="urbanPopulation"
)

df_long = df_long.rename(columns={
    "Country Name": "countryname",
    "Country Code": "countrycode"
})

df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce").astype("Int64")
df_long["urbanPopulation"] = pd.to_numeric(df_long["urbanPopulation"], errors="coerce")

df_long = df_long.sort_values(["countryname", "year"]).reset_index(drop=True)

df_long = df_long[["countryname", "year", "countrycode", "urbanPopulation"]]

df_long.to_csv("data cleaning/output/urban_population_panel.csv", index=False)

print("Saved: ../output/urban_population_panel.csv")
print(df_long.head(20))
print(df_long.shape)