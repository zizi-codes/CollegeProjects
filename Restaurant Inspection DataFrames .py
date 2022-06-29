#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import datetime as dt
df = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
pd.options.display.max_columns = None
df.columns = df.columns.str.replace(' ','_')


# In[ ]:





# Fact Table: 
# df_inspection_results
# 
# Dimensions:  
# 
# df_restaurant-- Restaurant.csv  
# 
# df_cuisine  --    Cuisine.csv  
# 
# df_location  --   Location.csv  
# 
# df_violation  --  Violation.csv  
# 
# df_date  -- Date.csv (in progress)
# 
# 

# In[2]:


inspection_results = ['CAMIS', 'INSPECTION_DATE', 'ACTION', 'CRITICAL_FLAG', 'SCORE', 'GRADE', 'GRADE_DATE', 'RECORD_DATE', 'INSPECTION_TYPE', 'Community_Board', 'Council_District', 'Census_Tract', 'BIN', 'BBL', 'NTA'] 
restaurant = ['CAMIS', 'DBA', 'BUILDING', 'STREET', 'PHONE', 'Latitude', 'Longitude']

df_restaurant = df[restaurant]
df_restaurant.set_index('CAMIS', inplace = True)


# In[3]:


df_cuisine = pd.DataFrame(df['CUISINE_DESCRIPTION'])
df_cuisine.index +=1
df_cuisine.index.name ='idCuisine'


# In[4]:


#location = ['BORO', 'ZIPCODE']
df_location = pd.DataFrame(df[['BORO', 'ZIPCODE']])
df_location.index+=1
df_location.index.name ='idLocation'


# In[5]:


df_violation = pd.DataFrame(df[['VIOLATION_CODE', 'VIOLATION_DESCRIPTION']])
df_violation.index+=1
df_violation.index.name ='idViolation'


# In[6]:


df['INSPECTION_DATE']


# In[9]:


df['INSPECTION_DATE'] = pd.to_datetime(df['INSPECTION_DATE'], format = '%m/%d/%Y')
df_inspection_date = pd.DataFrame(df['INSPECTION_DATE'])
df_inspection_date.index = df_inspection_date['INSPECTION_DATE'].dt.strftime('%Y%m%d')
df_inspection_date.index.name ='idDate'


# In[12]:


df_inspection_date


# df_restaurant.to_csv('Restaurant.csv')
# df_cuisine.to_csv('Cuisine.csv')
# df_location.to_csv('Location.csv')
# df_violation.to_csv('Violation.csv')
