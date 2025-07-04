import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as sp

df = pd.read_csv("Data/bacterial_growth_data.csv")
df.head(10)
df.info()  # based on this there are 8 missing values in Optical_Density_600nm
df.describe()

df_sorted = df.sort_values(by=["Strain", "Treatment", "Replicate", "Time_hrs"])

df_cleaned = df_sorted.copy()

df_cleaned["Optical_Density_600nm"] = df_cleaned.groupby(
    ["Strain", "Treatment", "Replicate"]
)["Optical_Density_600nm"].transform(lambda x: x.interpolate(method="linear"))
df_cleaned.dropna(inplace=True)
df_cleaned.head()
df_cleaned["Strain"] = df_cleaned["Strain"].astype("category")
df_cleaned["Treatment"] = df_cleaned["Treatment"].astype("category")
df_cleaned.info()

df_cleaned.to_csv("Data/clean_dataframe.csv", index=False)

# ---------------- #
# EDA

df_cleaned.head()
g = sns.FacetGrid(row="Replicate", data=df_cleaned, aspect=2, height=3, hue="Strain")
g = g.map(sns.lineplot, "Time_hrs", "Optical_Density_600nm")
plt.legend()
plt.savefig("Output/Replicate_growth_lineplot.png", dpi=300, format="png")

# NOTE Based on this plot, E. coli strains exhibit faster
# initial growth; however, over time, S. aureus surpasses
# the maximum growth level reached by E. coli.

mean = pd.DataFrame(
    df_cleaned.groupby(["Strain", "Treatment", "Time_hrs"])["Optical_Density_600nm"]
    .mean()
    .reset_index()
)
std = pd.DataFrame(
    df_cleaned.groupby(["Strain", "Treatment", "Time_hrs"])["Optical_Density_600nm"]
    .std()
    .reset_index()
)
varianceP = mean["Optical_Density_600nm"] - std["Optical_Density_600nm"]

import matplotlib.pyplot as plt

# Merge mean and std into one DataFrame for easy plotting
plot_df = mean.copy()
plot_df["Std"] = std["Optical_Density_600nm"]
plt.figure(figsize=(10, 6))

# Loop through each group and plot mean line with error band
for (strain, treatment), group in plot_df.groupby(["Strain", "Treatment"]):
    x = group["Time_hrs"]
    y = group["Optical_Density_600nm"]
    yerr = group["Std"]
    label = f"{strain}, {treatment}"

    # Plot mean line
    plt.plot(x, y, label=label)
    # Plot error band (mean ± std)
    plt.fill_between(x, y - yerr, y + yerr, alpha=0.2)

plt.xlabel("Time (hrs)")
plt.ylabel("Optical Density (600nm)")
plt.title("Mean Optical Density with Variance Error Bands")
plt.legend()
plt.savefig("Output/Lineplot_compoundX.png", format="png", dpi=300)
# NOTE based on this compound X seems to be inhibiting both strain at an extreme rate

final_time = df_cleaned[df_cleaned["Time_hrs"] == 24]
final_time.head()
mean_values = pd.DataFrame(
    final_time.groupby(["Treatment", "Strain"])["Optical_Density_600nm"]
    .mean()
    .reset_index()
)
mean_values

sns.barplot(
    x="Treatment",
    y="Optical_Density_600nm",
    hue="Strain",
    data=mean_values,
    palette="Set2",
)
plt.savefig("Output/barplot_growth_rate.png", dpi=300)
df_cleaned_E

# ------------ #
# statistical analysis

df_cleaned_E = final_time[final_time["Strain"] == "E. coli"]
df_cleaned_S = final_time[final_time["Strain"] == "S. aureus"]

# Null hypothesis: There is no significant difference on the growth rates of E. coli and when compound X is used.
# Alternative hypothesis: There is a significant difference on the growth rates of E. coli and when compound X is used.
t_stat, p_value = sp.ttest_ind(
    df_cleaned_E[df_cleaned_E["Treatment"] == "Control"]["Optical_Density_600nm"],
    df_cleaned_E[df_cleaned_E["Treatment"] == "Compound-X"]["Optical_Density_600nm"],
)
print(f"E. coli t-statistic: {round(t_stat, 5)}, p-value: {round(p_value, 5)}")

# Null hypothesis: There is no significant difference in the growth rates of S. aureus when compound X is applied.
# Alternative hypothesis: There is a significant difference in the growth rates of S. aureus when compound X is applied.

t_stat, p_value = sp.ttest_ind(
    df_cleaned_S[df_cleaned_S["Treatment"] == "Control"]["Optical_Density_600nm"],
    df_cleaned_S[df_cleaned_S["Treatment"] == "Compound-X"]["Optical_Density_600nm"],
)
print(f"S. aureus t-statistic: {round(t_stat, 5)}, p-value: {round(p_value, 5)}")

# Alternative hypothesis: There is a significant difference in the growth rates of E. coli and S. aureus when compound X is applied.
# NOTE: Based on the p-values, we can conclude that compound X has a significant inhibitory effect on the growth of both E. coli and S. aureus.
# there fore we reject the null hypothesis in both cases.