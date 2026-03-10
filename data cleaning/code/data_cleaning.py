#!/usr/bin/env python
# coding: utf-8

# In[23]:


import numpy as np
import pandas as pd


# In[24]:


df_paper = pd.read_csv('/Users/jeremysu/Downloads/paper_raw.csv')
df_paper.head()


# In[25]:


df_paper_wide = (
    df_paper.pivot_table(
        index=["Area", "Year"],
        columns="Element",
        values="Value",
        aggfunc="sum"
    )
    .reset_index()
)


# In[26]:


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


# In[27]:


df_paper_wide["Area_fixed"] = df_paper_wide["Area"].replace(name_map)


# In[28]:


drop_list = [
    'Anguilla',
    'Ascension, Saint Helena and Tristan da Cunha',
    'Belgium-Luxembourg',
    'China, Macao SAR', 
    'China, mainland',
    'China, Taiwan Province of',
    'Christmas Island',
    'Cocos (Keeling) Islands',
    'Cook Islands',
    "Democratic People's Republic of Korea",
    'Falkland Islands (Malvinas)',
    'French Guiana',
    'French Southern Territories',
    'Guadeloupe',
    'Martinique',
    'Montserrat',
    'Netherlands Antilles (former)',
    'Niue',
    'Norfolk Island',
    'Palestine',
    'Pitcairn',
    'Réunion',
    'Saint Pierre and Miquelon',
    'Serbia and Montenegro',
    'Sudan (former)',
    'Tokelau',
    'Wallis and Futuna Islands'
]


# In[29]:


df_paper_wide["Area_fixed"] = (
    df_paper_wide["Area"]
    .replace(name_map)
)

df_paper_wide = df_paper_wide[
    ~df_paper_wide["Area"].isin(drop_list)
]


# In[30]:


df_paper_wide.head()


# In[31]:


df_population = pd.read_csv('/Users/jeremysu/Downloads/API_SP.POP.TOTL_DS2_en_csv_v2_61/population_raw.csv', header=2)
df_population = df_population.drop(columns=["Unnamed: 70"])
df_population.head()


# In[32]:


df_population[df_population['Country Name'].str.contains('China')]


# In[33]:


df_population_long = df_population.melt(
    id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
    var_name="Year",
    value_name="population"
)
df_population_long["Year"] = df_population_long["Year"].astype(int)


# In[34]:


df_population_long.head()


# In[35]:


df_merge = df_paper_wide.merge(
    df_population_long,
    left_on=["Area_fixed", "Year"],
    right_on=["Country Name", "Year"],
    how="left"
)


# In[36]:


df_merge.head()


# In[37]:


df_merge[df_merge["population"].isna()]["Area_fixed"].unique()


# In[38]:


df_merge["paper_consumption"] = (
    df_merge["Production"]
    + df_merge["Import quantity"]
    - df_merge["Export quantity"]
)
df_merge = df_merge[df_merge["paper_consumption"] >= 0]
df_merge['paper_per_capita'] = df_merge['paper_consumption'] / df_merge['population']


# In[39]:


df_final = df_merge[["Country Name", "Year", "population", "paper_consumption", 'paper_per_capita']]

df_final = df_final.rename(columns={'Country Name': 'countryname', 'Year': 'year'})

df_final = df_final.dropna()

df_final = df_final.reset_index(drop=True)

df_final.head()


# In[40]:


df_final.shape


# In[41]:


df_final.to_csv("/Users/jeremysu/Downloads/paper_consumption_population.csv", index=False)


# In[ ]:




