from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

df = pd.read_csv('Data/clean_dataframe.csv')

# checking columns for variance
threshold = 0.1
variance = df.var(numeric_only = True)
low_variance_columns = variance[variance < threshold].index.tolist()
print("Columns with low variance:", low_variance_columns)

df = df.pivot_table(index= ["Strain","Replicate"], columns = "Time_hrs", values = "Optical_Density_600nm")
df.columns = df.columns.astype(str)
# non of the columns have low variance
# moving to random forest to check for feature importance

X = df.drop(columns = ["Strain"])
y = df["Strain"]

def evaluate_model(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")
    feature_importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': feature_importances
    }).sort_values(by='Importance', ascending=False)
    print("\nFeature Importances:")
    print(feature_importance_df)
    
evaluate_model(RandomForestClassifier(n_estimators=100, random_state=42), X, y)
# importanted fearures are time 12, 14, 8, 10,24

# The only column that is important is Optical_Density_600nm
X = df[["12", "14", "8", "10", "24"]]
y = df["Strain"]
evaluate_model(RandomForestClassifier(n_estimators=100, random_state=42), X, y)
# The model is performing better than before, but still not great.
# Accuracy: 0.39
# Precision: 0.39
# Recall: 0.39
# F1 Score: 0.38
df
# moving to binary classification
# Converting Strain to binary classification
df["Strain"] = df_scaled["Strain"].apply(lambda x: 1 if x == "E. coli" else 0)
X = df[["Optical_Density_600nm"]]
y = df["Strain"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))
# Since the data was too small were not able to perform logistic regression

# NOTE: Based on how the random forest model performed, the data is concluded to be 
# too small for machine learning models to perform well. further data collection is needed.