import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Data/bacterial_growth_data.csv")
df.head(10)
df.info() # based on this there are 8 missing values in Optical_Density_600nm
df.describe()

df_sorted = df.sort_values(by=['Strain', 'Treatment', 'Replicate', 'Time_hrs'])

df_cleaned = df_sorted.copy()

df_cleaned['Optical_Density_600nm'] = df_cleaned.groupby(
    ['Strain', 'Treatment', 'Replicate'])['Optical_Density_600nm'].transform(
    lambda x: x.interpolate(method='linear')
)
df_cleaned.dropna(inplace = True)
df_cleaned.head()
df_cleaned["Strain"] = df_cleaned["Strain"].astype("category")
df_cleaned["Treatment"] = df_cleaned["Treatment"].astype("category")
df_cleaned.info()

