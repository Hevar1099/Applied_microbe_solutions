# Applied Microbe Solutions: Bacterial Growth Analysis

## Overview

This repository contains all scripts, data, and instructions necessary to replicate the analysis of bacterial growth under different treatments. The project focuses on comparing the growth dynamics of *E. coli* and *S. aureus* strains, using optical density measurements over time, and visualizing the results with professional plots including error bands. Statistical testing (t-tests) is also performed to compare treatment effects.  
**A machine learning model (Random Forest Classifier) is used to classify strains based on growth curves.**

---

## Repository Structure

```
Applied_microbe_solutions/
│
├── Data/
│   └── bacterial_growth_data.csv         # Raw experimental data
│   └── clean_dataframe.csv               # Cleaned data after preprocessing
│
├── Output/
│   └── Replicate_growth_lineplot.png     # Growth curves by replicate
│   └── Lineplot_compoundX.png            # Mean growth curves with error bands
│
├── Scripts/
│   └── analysis.py                       # Main analysis script
│
├── README.md                             # This file
```

---

## Requirements

- Python 3.8+
- [pandas](https://pandas.pydata.org/)
- [numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/)
- [seaborn](https://seaborn.pydata.org/)
- [scipy](https://scipy.org/) (for statistical tests)
- [scikit-learn](https://scikit-learn.org/) (for machine learning)

Install dependencies with:

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn
```

---

## Data Description

- **bacterial_growth_data.csv**: Contains columns:
  - `Strain`: Bacterial strain (*E. coli* or *S. aureus*)
  - `Treatment`: Experimental treatment group
  - `Replicate`: Replicate number
  - `Time_hrs`: Time in hours
  - `Optical_Density_600nm`: Optical density measurement at 600nm

---

## How to Run the Analysis

1. **Clone the repository:**

    ```bash
    git clone <https://github.com/Hevar1099/Applied_microbe_solutions>
    cd Applied_microbe_solutions
    ```

2. **Ensure the data is in the `Data/` folder.**

3. **Run the analysis script:**

    ```bash
    python Scripts/analysis.py
    ```

    This will:
    - Load and inspect the data
    - Clean and interpolate missing values
    - Save the cleaned data to `Data/clean_dataframe.csv`
    - Generate and save plots to the `Output/` folder
    - Perform t-tests to compare treatments
    - Train and evaluate a Random Forest Classifier to predict strain from growth curves

---

## Analysis Workflow

1. **Data Loading & Inspection**
    - Loads raw CSV data.
    - Checks for missing values and data types.

2. **Data Cleaning**
    - Sorts data for consistent processing.
    - Interpolates missing optical density values within each group (`Strain`, `Treatment`, `Replicate`).
    - Drops any remaining missing values.
    - Converts categorical columns for efficiency.

3. **Exploratory Data Analysis (EDA)**
    - Plots growth curves for each replicate and strain.
    - Calculates group means and variances for optical density.

4. **Visualization**
    - Plots mean growth curves for each strain and treatment.
    - Adds error bands (mean ± standard deviation) using `plt.fill_between` for professional visualization.

5. **Statistical Testing**
    - Performs independent t-tests (using `scipy.stats.ttest_ind`) to compare the effects of treatments (e.g., Control vs. CompoundX) within each strain.
    - Example code:

      ```python
      import scipy.stats as sp
      t_stat, p_value = sp.ttest_ind(
          df_cleaned_E[df_cleaned_E["Treatment"] == "Control"]["Optical_Density_600nm"],
          df_cleaned_E[df_cleaned_E["Treatment"] == "CompoundX"]["Optical_Density_600nm"]
      )
      print(f"T-statistic: {t_stat}, P-value: {p_value}")
      ```

6. **Machine Learning Classification**
    - A Random Forest Classifier is trained using the time-course OD measurements as features to predict the bacterial strain.
    - The model achieved **100% accuracy on the held-out test set**.

---

## Model Performance

**Random Forest Classifier Results:**

- **Accuracy:** 1.00
- **Precision:** 1.00
- **Recall:** 1.00
- **F1 Score:** 1.00

**Discussion:**  
While a perfect score can often indicate overfitting, in this case, it reflects the clean, synthetic nature of the dataset where the growth profiles of the two species were designed to be distinct and non-overlapping. This result demonstrates that the growth curve dynamics are a highly effective and sufficient feature for classifying these two strains under these experimental conditions. In a real-world application with noisier experimental data and more biological variability, we would expect performance to be lower, and a more robust validation technique like k-fold cross-validation would be necessary to estimate the model's true generalization error.

---

## Example Plots

- **Growth Curves by Replicate:**  
  ![Replicate_growth_lineplot](Output/Replicate_growth_lineplot.png)

- **Mean Growth Curves with Error Bands:**  
  ![Lineplot_compoundX](Output/Lineplot_compoundX.png)

---

## Interpretation

- *E. coli* strains exhibit faster initial growth.
- Over time, *S. aureus* surpasses the maximum growth level reached by *E. coli*.
- Statistical tests (t-tests) help determine if treatment effects are significant.
- Machine learning can robustly classify strains based on growth curves in this synthetic dataset.

---

## Customization

- To analyze additional strains or treatments, add them to the CSV and rerun the script.
- Modify plotting parameters in `Scripts/analysis.py` for different visual styles.
- Adjust statistical tests or machine learning models as needed for your experimental design.

---

## Troubleshooting

- **No plots generated?**  
  Ensure all dependencies are installed and the data file is present in the correct folder.

- **Error bars not showing?**  
  Make sure you are plotting with the correct DataFrame and using `plt.fill_between` for error bands.

- **Statistical test errors?**  
  Check that your data subsets are not empty and contain numeric values.

- **Model performance is too high or too low?**  
  Double-check your train/test split. Perfect scores may indicate synthetic data or data leakage. For real-world data, use cross-validation for a more realistic estimate.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or collaboration, please open an issue or contact the repository owner.
