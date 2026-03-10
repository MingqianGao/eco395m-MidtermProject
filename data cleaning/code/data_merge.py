#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


paper_population = pd.read_csv('/Users/jeremysu/Downloads/paper_consumption_population.csv')


# In[3]:


paper_population.head()


# In[4]:


gdpedu = pd.read_excel('/Users/jeremysu/Downloads/gdpedu.xlsx')


# In[5]:


gdpedu.head()


# In[6]:


urban_internet = pd.read_csv('/Users/jeremysu/Downloads/urban_internet_merged.csv')


# In[7]:


urban_internet.drop(columns=['countrycode'], inplace=True)


# In[8]:


urban_internet.head()


# In[9]:


df_tmp = paper_population.merge(
    gdpedu,
    on=["countryname", "year"],
    how="left"
)


# In[10]:


df = df_tmp.merge(
    urban_internet,
    on=["countryname", "year"],
    how="left"
)


# In[11]:


df.shape


# In[12]:


df.to_csv('/Users/jeremysu/Downloads/final_dataset.csv', index=False)


# In[ ]:




