# eco395m-MidtermProject
Group Member: Mingqian Gao, Yuxin Zhao, and Chieh Su

## 1. Introduction

## 2. Data

### 2.1 Data Sources

This study combines multiple international datasets to construct a country–year panel dataset.  
Economic indicators, including GDP per capita, GDP growth, manufacturing share, trade openness, internet usage, urban population, and total population, are obtained from the World Bank's World Development Indicators (WDI).  

Data on paper production, imports, and exports are obtained from FAOSTAT. These data are used to construct measures of paper consumption. Writing and printing paper consumption is calculated as production plus imports minus exports. Total paper consumption is constructed using the same accounting identity.

The final dataset covers 114 countries over the period from 1990 to 2024. 
Because data availability varies across countries and indicators, the panel is not perfectly balanced. 
However, the majority of countries maintain relatively complete time coverage. 
Only 18 countries have fewer than 15 years of observations, while most countries contribute substantially longer time series.

---

### 2.2 Variable Construction

The main outcome variable is **writing and printing paper consumption per capita**, measured in kilograms per person. It is calculated by dividing national paper consumption by total population.

Key explanatory variables capture economic development, technological adoption, and economic structure. These include GDP per capita (constant 2015 USD), GDP growth rate, internet users as a share of population, urban population, manufacturing value added as a share of GDP, and trade openness measured as the ratio of trade to GDP.

Several variables are transformed or standardized to ensure comparability across countries. For example, manufacturing share and trade openness are expressed as proportions, and paper consumption is converted from tons to kilograms when constructing per capita measures.

### Table 1. Variable Definitions

| Variable | Description | Unit |
|---|---|---|
| Paper Consumption per Capita | Writing and printing paper consumption per capita, calculated as national paper consumption divided by total population | kilograms/person |
| Paper Writing Consumption | Total national consumption of writing and printing paper, calculated as production plus imports minus exports | kilograms |
| Total Paper Consumption | Total national consumption of all paper products, calculated as production plus imports minus exports | kilograms |
| GDP per Capita | Gross domestic product per capita, measured in constant 2015 USD | USD |
| GDP Growth | Annual growth rate of GDP | percent |
| Internet Users | Individuals using the internet as a share of the population | percent |
| Urban Population | Total population living in urban areas | persons |
| Total Population | Total national population | persons |
| Manufacturing Share | Manufacturing value added as a share of GDP | proportion |
| Trade Openness | Total trade (exports + imports) as a share of GDP | proportion |

### 2.3 Descriptive Statistics

Table 2 reports summary statistics for the main variables used in the analysis.  
The final panel dataset contains **5,373 country–year observations** covering multiple countries over time.

Paper consumption per capita exhibits a highly right-skewed distribution, with most observations concentrated at relatively low levels but a small number of extreme values.

The statistics also indicate substantial heterogeneity in economic development, technological adoption, and economic structure across the sample. 
Variables such as GDP per capita, internet penetration, and trade openness display wide variation, reflecting differences in development levels and economic characteristics across countries and over time.

---

# Table 2: Summary Statistics

| Variable | Count | Mean | Std. Dev. | Min | 25% | Median | 75% | Max |
|---|---|---|---|---|---|---|---|---|
| Paper Writing Consumption | 5373 | 586,248,428 | 2,472,254,841 | 0 | 2,956,000 | 26,700,000 | 237,800,000 | 2.817e10 |
| Total Paper Consumption | 4979 | 2,187,939,747 | 9,787,037,339 | 0 | 8,780,000 | 92,219,000 | 804,950,000 | 1.423e11 |
| GDP per Capita (USD) | 5373 | 13,159.81 | 17,802.52 | 170.23 | 1,774.64 | 5,175.20 | 17,980.73 | 167,187.16 |
| GDP Growth (%) | 5365 | 3.54 | 5.99 | -51.03 | 1.41 | 3.69 | 5.90 | 149.97 |
| Internet Users (% of population) | 5373 | 31.79 | 32.40 | 0 | 1.86 | 18.90 | 61.16 | 100 |
| Urban Population | 5373 | 20,412,950 | 64,241,165 | 4,344 | 1,263,587 | 4,262,417 | 14,315,364 | 928,439,823 |
| Total Population | 5373 | 392,414,999 | 1,402,894,242 | 9,544 | 2,392,978 | 8,472,313 | 27,154,515 | 1.425e9 |
| Manufacturing Share | 4810 | 0.126 | 0.064 | 0.003 | 0.079 | 0.123 | 0.167 | 0.450 |
| Trade Openness | 4739 | 0.850 | 0.530 | 0.100 | 0.515 | 0.731 | 1.025 | 1.426 |
| Paper Consumption per Capita | 5373 | 14.40 | 26.72 | 0 | 0.79 | 4.29 | 14.96 | 782.93 |

---
