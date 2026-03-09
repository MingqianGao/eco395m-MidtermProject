import pandas as pd

# clean urban population
urban = pd.read_csv("data cleaning/raw/urban_population.csv", skiprows=4)

urban_year_cols = [str(year) for year in range(1990, 2025)]
urban = urban[["Country Name", "Country Code"] + urban_year_cols]

urban_long = urban.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=urban_year_cols,
    var_name="year",
    value_name="urbanPopulation"
)

urban_long = urban_long.rename(columns={
    "Country Name": "countryname",
    "Country Code": "countrycode"
})

urban_long["year"] = pd.to_numeric(urban_long["year"], errors="coerce")
urban_long["urbanPopulation"] = pd.to_numeric(urban_long["urbanPopulation"], errors="coerce")

urban_long = urban_long.sort_values(["countryname", "year"]).reset_index(drop=True)
urban_long = urban_long[["countryname", "year", "countrycode", "urbanPopulation"]]

urban_long.to_csv("data cleaning/intermediate/urban_population_panel.csv", index=False)

print("urban_population_panel saved")
print(urban_long.head())
print(urban_long.shape)


# clean internet users
internet = pd.read_csv("data cleaning/raw/Internet_users.csv", skiprows=4)

internet_year_cols = [str(year) for year in range(1990, 2025)]
internet = internet[["Country Name", "Country Code"] + internet_year_cols]

internet_long = internet.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=internet_year_cols,
    var_name="year",
    value_name="internetUsers"
)

internet_long = internet_long.rename(columns={
    "Country Name": "countryname",
    "Country Code": "countrycode"
})

internet_long["year"] = pd.to_numeric(internet_long["year"], errors="coerce")
internet_long["internetUsers"] = pd.to_numeric(internet_long["internetUsers"], errors="coerce")

internet_long = internet_long.sort_values(["countryname", "year"]).reset_index(drop=True)
internet_long = internet_long[["countryname", "year", "countrycode", "internetUsers"]]

internet_long.to_csv("data cleaning/intermediate/internet_users_panel.csv", index=False)

print("internet_users_panel saved")
print(internet_long.head())
print(internet_long.shape)


# merge the two cleaned datasets
merged = pd.merge(
    urban_long,
    internet_long,
    on=["countryname", "year", "countrycode"],
    how="outer"
)

merged = merged.sort_values(["countryname", "year"]).reset_index(drop=True)

merged.to_csv("data cleaning/output/urban_internet_merged.csv", index=False)

print("urban_internet_merged saved")
print(merged.head(20))
print(merged.shape)