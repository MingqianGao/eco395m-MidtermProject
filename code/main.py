from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor


# ------------------------------#
# 0. Paths
# ------------------------------#
CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
RAW = ROOT / "raw"
INT = ROOT / "intermediate"
DATA = ROOT / "data_cleaning"
OUT = ROOT / "output"


# ----------------------------------------------------------#
# Model Evaluation
# ----------------------------------------------------------#

def evaluate_model(model, model_name):

    model.fit(X_train, y_train)

    y_pred_log = model.predict(X_test)

    y_test_exp = np.exp(y_test)
    y_pred_exp = np.exp(y_pred_log)

    rmse = np.sqrt(mean_squared_error(y_test_exp, y_pred_exp))
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

def run_linear_regression():

    model = LinearRegression()

    return evaluate_model(model, "Linear Regression")



# ----------------------------------------------------------#
# Polynomial Regression
# ----------------------------------------------------------#

def run_polynomial_regression():

    model = make_pipeline(
        PolynomialFeatures(degree=2, include_bias=False),
        StandardScaler(),
        LinearRegression()
    )

    return evaluate_model(model, "Polynomial Regression")


# ----------------------------------------------------------#
# KNN
# ----------------------------------------------------------#

def run_knn():

    model = make_pipeline(
        StandardScaler(),
        KNeighborsRegressor(n_neighbors=10)
    )

    return evaluate_model(model, "KNN")


# ----------------------------------------------------------#
# Decision Tree
# ----------------------------------------------------------#

def run_decision_tree():

    model = DecisionTreeRegressor(
        max_depth=5,
        random_state=42
    )

    return evaluate_model(model, "Decision Tree")


# ----------------------------------------------------------#
# Random Forest
# ----------------------------------------------------------#

def run_random_forest():

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=8,
        random_state=42
    )

    return evaluate_model(model, "Random Forest")


# ----------------------------------------------------------#
# XGBoost
# ----------------------------------------------------------#

def run_xgboost():

    model = XGBRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        objective="reg:squarederror"
    )

    return evaluate_model(model, "XGBoost")

# ---------------------------------------
# Model Comparison
# ---------------------------------------

def model_comparison(results):

    result_df = pd.DataFrame(results)

    result_df = result_df.sort_values("RMSE").reset_index(drop=True)

    result_df.to_csv(OUT/"model_comparison.csv", index=False)

    plt.figure(figsize=(8,5))
    plt.bar(result_df["Model"], result_df["RMSE"])
    plt.title("Model Comparison (RMSE)")
    plt.xlabel("Model")
    plt.ylabel("RMSE")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(OUT/"model_comparison.png")
    plt.close()

    print("\nModel Comparison:")
    print(result_df)

    return result_df

# ---------------------------------------
# Feature Importance
# ---------------------------------------
def feature_importance(best_model_name, best_model, feature_cols):

    if not hasattr(best_model, "feature_importances_"):
        print(best_model_name, "does not support feature importance.")
        return

    importance = best_model.feature_importances_

    fi_df = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": importance
    })

    fi_df = fi_df.sort_values("Importance", ascending=False)

    file_name = best_model_name.lower().replace(" ", "_")

    fi_df.to_csv(
        f"output/tables/feature_importance_{file_name}.csv",
        index=False
    )

    plt.figure(figsize=(8,5))
    plt.bar(fi_df["Feature"], fi_df["Importance"])
    plt.title(f"Feature Importance ({best_model_name})")
    plt.xlabel("Feature")
    plt.ylabel("Importance")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        f"output/figures/feature_importance_{file_name}.png"
    )

    plt.close()

    print("\nFeature Importance:")
    print(fi_df)


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

results = []
trained_models = {}

res, model = run_linear_regression()
results.append(res)
trained_models["Linear Regression"] = model

res, model = run_polynomial_regression()
results.append(res)
trained_models["Polynomial Regression"] = model

res, model = run_knn()
results.append(res)
trained_models["KNN"] = model

res, model = run_decision_tree()
results.append(res)
trained_models["Decision Tree"] = model

res, model = run_random_forest()
results.append(res)
trained_models["Random Forest"] = model

res, model = run_xgboost()
results.append(res)
trained_models["XGBoost"] = model

feature_cols = X_cols

# Model comparison
result_df = model_comparison(results)

# choose best model
best_model_name = result_df.iloc[0]["Model"]

best_model = trained_models[best_model_name]

# feature importance
feature_importance(best_model_name, best_model, feature_cols)