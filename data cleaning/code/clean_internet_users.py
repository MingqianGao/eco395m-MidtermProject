import pandas as pd

df = pd.read_csv("data cleaning/raw/Internet_users.csv", skiprows=4)

print("Columns:")
print(df.columns.tolist())

year_cols = [str(year) for year in range(1990, 2025)]

df = df[["Country Name", "Country Code"] + year_cols]

df_long = df.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=year_cols,
    var_name="year",
    value_name="internetUsers"
)

df_long = df_long.rename(columns={
    "Country Name": "countryname",
    "Country Code": "countrycode"
})

df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce")
df_long["internetUsers"] = pd.to_numeric(df_long["internetUsers"], errors="coerce")

df_long = df_long.sort_values(["countryname", "year"])

df_long.to_csv("data cleaning/output/internet_users_panel.csv", index=False)

print(df_long.head(20))
print(df_long.shape)