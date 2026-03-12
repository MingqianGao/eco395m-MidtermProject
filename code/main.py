from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ------------------------------#
# 0. Paths
# ------------------------------#
CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
RAW = ROOT / "raw"
INT = ROOT / "intermediate"
DATA = ROOT / "data_cleaning"
OUT = ROOT / "output"

# ------------------------------#
# 1. Descriptive Statistics
# ------------------------------#

df = pd.read_csv(DATA / "final_panel.csv")

df = df.drop(columns=['schoolsec', 'schoolter'])
df = df.dropna(axis=0, how='any')
df = df[df["paper_writing"] > 0]
df = df[df["GDPperCapita"] > 0]
df = df[df["urbanpop"] > 0]

df["paper_per_capita"] = df["paper_writing"] / df["population"]
df["log_GDPperCapita"] = np.log(df["GDPperCapita"])
df["log_urbanpop"] = np.log(df["urbanpop"])


vars = [
    "paper_writing",
    "paper_all",
    "GDPperCapita",
    "GDPgrowth",
    "internetUsers",
    "urbanpop",
    "population",
    "Manushare",
    "trade",
    "paper_per_capita",
]

summary = df[vars].describe().T

summary.to_csv(OUT / "summary_statistics.csv")

# ----------------------------------------------------------#
# Correlation Heatmap
# ----------------------------------------------------------#


corr = df[vars].corr()

plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Matrix")

plt.savefig(OUT / "correlation_heatmap.png", dpi=300)
plt.show()

# ----------------------------------------------------------#
# 2. Models
# ----------------------------------------------------------#

# prepare modeling dataset
df["log_paper_pc"] = np.log(df["paper_per_capita"])

X_cols = [
    "log_GDPperCapita", 
    "internetUsers",
    "Manushare",
    "year",
    "log_urbanpop",
    "trade",
    "GDPgrowth",
]

X = df[X_cols]
y = df["log_paper_pc"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


def evaluate_model(model, model_name):

    model.fit(X_train, y_train)

    y_pred_log = model.predict(X_test)

    y_test_exp = np.exp(y_test)
    y_pred_exp = np.exp(y_pred_log)

    rmse = mean_squared_error(y_test_exp, y_pred_exp, squared=False)
    r2 = r2_score(y_test_exp, y_pred_exp)

    result = {
        "Model": model_name,
        "RMSE": rmse,
        "R2": r2
    }

    return result, model


# ----------------------------------------------------------#
# Linear Regression
# ----------------------------------------------------------#




# ----------------------------------------------------------#
# Polynomial Regression
# ----------------------------------------------------------#




# ----------------------------------------------------------#
# KNN
# ----------------------------------------------------------#




# ----------------------------------------------------------#
# Decision Tree
# ----------------------------------------------------------#




# ----------------------------------------------------------#
# Random Forest
# ----------------------------------------------------------#




# ----------------------------------------------------------#
# XGBoost
# ----------------------------------------------------------#







