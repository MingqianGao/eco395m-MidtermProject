from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
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
DATA = ROOT / "data_cleaning"
OUT = ROOT / "output"

OUT.mkdir(exist_ok=True)

# ----------------------------------------------------------#
# Model Evaluation
# ----------------------------------------------------------#

def evaluate_model(model, model_name, X_train, X_test, y_train, y_test):
    """
    Fit a model, evaluate it on the test set, and return metrics.
    """
    
    model.fit(X_train, y_train)

    best_model = model.best_estimator_ if hasattr(model, "best_estimator_") else model

    y_pred_log = best_model.predict(X_test)

    y_test_exp = np.exp(y_test)
    y_pred_exp = np.exp(y_pred_log)

    rmse = np.sqrt(mean_squared_error(y_test_exp, y_pred_exp))
    r2 = r2_score(y_test_exp, y_pred_exp)

    result = {
        "Model": model_name,
        "RMSE": rmse,
        "R2": r2
    }

    return result, best_model


# ----------------------------------------------------------#
# Linear Regression
# ----------------------------------------------------------#

def run_linear_regression(X_train, X_test, y_train, y_test):
    """
    Train and evaluate a linear regression model.
    """
    model = LinearRegression()

    return evaluate_model(model, "Linear Regression", X_train, X_test, y_train, y_test)


# ----------------------------------------------------------#
# Polynomial Regression
# ----------------------------------------------------------#
    
def run_polynomial_regression(X_train, X_test, y_train, y_test):
    """
    Train and evaluate a polynomial regression model.
    """
    
    poly_pipe = make_pipeline(
    PolynomialFeatures(include_bias=False),
    StandardScaler(),
    LinearRegression()
    )
    
    param_grid = {
        "polynomialfeatures__degree": [1, 2, 3]
    }
    
    grid_poly = GridSearchCV(
        poly_pipe,
        param_grid,
        cv=5,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1
    )
    
    return evaluate_model(grid_poly, "Polynomial Regression", X_train, X_test, y_train, y_test)


# ----------------------------------------------------------#
# KNN
# ----------------------------------------------------------#

def run_knn(X_train, X_test, y_train, y_test):
    """
    Train and evaluate a KNN model.
    """
    
    knn_pipe = make_pipeline(
    StandardScaler(),
    KNeighborsRegressor()
    )
    
    param_grid = {
        "kneighborsregressor__n_neighbors": [3,5,7,9,11],
        "kneighborsregressor__weights": ["uniform","distance"]
    }
    
    grid_knn = GridSearchCV(
        knn_pipe,
        param_grid,
        cv=5,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1
    )

    return evaluate_model(grid_knn, "KNN", X_train, X_test, y_train, y_test)


# ----------------------------------------------------------#
# Decision Tree
# ----------------------------------------------------------#

def run_decision_tree(X_train, X_test, y_train, y_test):
    """
    Train and evaluate a decision tree model.
    """
    
    tree = DecisionTreeRegressor(random_state=42)

    param_grid = {
        "max_depth": [3,5,8,10,12,None],
        "min_samples_split": [2,5,10],
        "min_samples_leaf": [1,2,4]
    }
    
    grid_tree = GridSearchCV(
        tree,
        param_grid,
        cv=5,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1
    )

    return evaluate_model(grid_tree, "Decision Tree", X_train, X_test, y_train, y_test)


# ----------------------------------------------------------#
# Random Forest
# ----------------------------------------------------------#

def run_random_forest(X_train, X_test, y_train, y_test):
    """
    Train and evaluate a random forest model.
    """
    
    rf = RandomForestRegressor(random_state=42)

    param_grid = {
        "n_estimators": [300,400,500],
        "max_depth": [5,8,12,None],
        "min_samples_split": [2,5],
        "min_samples_leaf": [1,2,4]
    }
    
    grid_rf = GridSearchCV(
        rf,
        param_grid,
        cv=5,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1
    )

    return evaluate_model(grid_rf, "Random Forest", X_train, X_test, y_train, y_test)


# ----------------------------------------------------------#
# XGBoost
# ----------------------------------------------------------#

def run_xgboost(X_train, X_test, y_train, y_test):
    """
    Train and evaluate an XGBoost model.
    """
    
    xgb = XGBRegressor(
    random_state=42,
    objective="reg:squarederror"
    )
    
    param_grid = {
        "n_estimators": [200,300,400],
        "max_depth": [4,6,8],
        "learning_rate": [0.05,0.1,0.2],
        "subsample": [0.8,1.0],
        "colsample_bytree": [0.8,1.0]
    }
    
    grid_xgb = GridSearchCV(
        xgb,
        param_grid,
        cv=5,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1
    )

    return evaluate_model(grid_xgb, "XGBoost", X_train, X_test, y_train, y_test)

# ---------------------------------------
# Model Comparison
# ---------------------------------------

def model_comparison(results, suffix=""):
    """
    Create a model comparison table and save the comparison plot.
    """
    
    result_df = pd.DataFrame(results)

    result_df = result_df.sort_values("RMSE").reset_index(drop=True)

    result_df.to_csv(OUT / f"model_comparison{suffix}.csv", index=False)

    plt.figure(figsize=(8,5))
    plt.bar(result_df["Model"], result_df["RMSE"])
    plt.title("Model Comparison (RMSE)")
    plt.xlabel("Model")
    plt.ylabel("RMSE")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(OUT / f"model_comparison{suffix}.png")
    plt.close()

    print("\nModel Comparison:")
    print(result_df)

    return result_df

# ---------------------------------------
# Feature Importance
# ---------------------------------------
def feature_importance(best_model_name, best_model, feature_cols, suffix=""):
    """
    Save feature importance values and create a feature importance plot.
    """
    
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
        OUT / f"feature_importance_{file_name}{suffix}.csv",
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
        OUT / f"feature_importance_{file_name}{suffix}.png"
    )

    plt.close()

    print("\nFeature Importance:")
    print(fi_df)


# ------------------------------#
# 1. Descriptive Statistics
# ------------------------------#

df = pd.read_csv(DATA / "final_panel.csv")

df = df.drop(columns=["schoolsec", "schoolter"])
df = df.dropna(axis=0, how="any")
df = df[df["paper_writing"] > 0]
df = df[df["GDPperCapita"] > 0]
df = df[df["urbanpop"] > 0]

df["paper_per_capita"] = df["paper_writing"] / df["population"]
df["log_GDPperCapita"] = np.log(df["GDPperCapita"])
df["log_urbanpop"] = np.log(df["urbanpop"])


summary_vars = [
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

summary = df[summary_vars].describe().T

summary.to_csv(OUT / "summary_statistics.csv")

# ----------------------------------------------------------#
# Correlation Heatmap
# ----------------------------------------------------------#


corr = df[summary_vars].corr()

plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Matrix")

plt.savefig(OUT / "correlation_heatmap.png", dpi=300)
plt.close()

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

res, model = run_linear_regression(X_train, X_test, y_train, y_test)
results.append(res)
trained_models["Linear Regression"] = model

res, model = run_polynomial_regression(X_train, X_test, y_train, y_test)
results.append(res)
trained_models["Polynomial Regression"] = model

res, model = run_knn(X_train, X_test, y_train, y_test)
results.append(res)
trained_models["KNN"] = model

res, model = run_decision_tree(X_train, X_test, y_train, y_test)
results.append(res)
trained_models["Decision Tree"] = model

res, model = run_random_forest(X_train, X_test, y_train, y_test)
results.append(res)
trained_models["Random Forest"] = model

res, model = run_xgboost(X_train, X_test, y_train, y_test)
results.append(res)
trained_models["XGBoost"] = model

feature_cols = X_cols

# Model comparison
result_df = model_comparison(results, "_with_gdp")

# choose best model
best_model_name = result_df.iloc[0]["Model"]

best_model = trained_models[best_model_name]

# feature importance
feature_importance(best_model_name, best_model, feature_cols, "_with_gdp")

# Remove GDPperCapita from X and run again
X_cols_without_gdp = [
    "internetUsers",
    "Manushare",
    "year",
    "log_urbanpop",
    "trade",
    "GDPgrowth",
]

X_without_gdp = df[X_cols_without_gdp]
y_without_gdp = df["log_paper_pc"]

X_train_without_gdp, X_test_without_gdp, y_train_without_gdp, y_test_without_gdp = train_test_split(
    X_without_gdp, y_without_gdp, test_size=0.2, random_state=42
)

results = []
trained_models = {}

res, model = run_linear_regression(X_train_without_gdp, X_test_without_gdp, y_train_without_gdp, y_test_without_gdp)
results.append(res)
trained_models["Linear Regression"] = model

res, model = run_polynomial_regression(X_train_without_gdp, X_test_without_gdp, y_train_without_gdp, y_test_without_gdp)
results.append(res)
trained_models["Polynomial Regression"] = model

res, model = run_knn(X_train_without_gdp, X_test_without_gdp, y_train_without_gdp, y_test_without_gdp)
results.append(res)
trained_models["KNN"] = model

res, model = run_decision_tree(X_train_without_gdp, X_test_without_gdp, y_train_without_gdp, y_test_without_gdp)
results.append(res)
trained_models["Decision Tree"] = model

res, model = run_random_forest(X_train_without_gdp, X_test_without_gdp, y_train_without_gdp, y_test_without_gdp)
results.append(res)
trained_models["Random Forest"] = model

res, model = run_xgboost(X_train_without_gdp, X_test_without_gdp, y_train_without_gdp, y_test_without_gdp)
results.append(res)
trained_models["XGBoost"] = model

feature_cols = X_cols_without_gdp

# Model comparison
result_df = model_comparison(results, "_without_gdp")

# choose best model
best_model_name = result_df.iloc[0]["Model"]

best_model = trained_models[best_model_name]

# feature importance
feature_importance(best_model_name, best_model, feature_cols, "_without_gdp")
