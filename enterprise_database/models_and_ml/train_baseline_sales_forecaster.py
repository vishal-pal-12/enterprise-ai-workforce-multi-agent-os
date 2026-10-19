import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR = os.path.join(BASE_DIR, "models_and_ml")
DATASET_PATH = os.path.join(ML_DIR, "sales_forecasting_training_dataset.csv")

def run_forecaster():
    print(f"Loading ML dataset from {DATASET_PATH}...")
    df = pd.read_csv(DATASET_PATH)
    print(f"Total dataset shape: {df.shape}")
    
    # Feature columns and target
    feature_cols = [
        "daily_order_count", "daily_revenue",
        "day_of_week", "day_of_month", "month", "quarter", "is_weekend", "is_quarter_end",
        "lag_1d_revenue", "lag_7d_revenue", "lag_14d_revenue", "lag_30d_revenue",
        "rolling_mean_7d", "rolling_std_7d", "rolling_mean_30d",
        "state_gov_asi_share_pct", "state_gov_gst_share_pct"
    ]
    target_col = "target_future_7d_revenue"
    
    # Temporal Train/Test split: Train on 2022-2023, Test on 2024 to prevent temporal data leakage
    df["order_date_dt"] = pd.to_datetime(df["order_date"])
    train_mask = df["order_date_dt"] < pd.to_datetime("2024-01-01")
    test_mask = df["order_date_dt"] >= pd.to_datetime("2024-01-01")
    
    X_train = df.loc[train_mask, feature_cols]
    y_train = df.loc[train_mask, target_col]
    
    X_test = df.loc[test_mask, feature_cols]
    y_test = df.loc[test_mask, target_col]
    
    print(f"Training samples (2022-2023): {len(X_train)}")
    print(f"Evaluation samples (2024): {len(X_test)}")
    
    # Baseline Model: Pipeline with StandardScaler and Random Forest Regressor
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    
    print("Fitting Random Forest Baseline Regressor...")
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    train_mae = float(mean_absolute_error(y_train, y_pred_train))
    test_mae = float(mean_absolute_error(y_test, y_pred_test))
    test_rmse = float(np.sqrt(mean_squared_error(y_test, y_pred_test)))
    test_r2 = float(r2_score(y_test, y_pred_test))
    
    # Feature importances
    importances = dict(zip(feature_cols, [float(v) for v in model.feature_importances_]))
    sorted_importances = dict(sorted(importances.items(), key=lambda item: item[1], reverse=True))
    
    metrics = {
        "model_architecture": "RandomForestRegressor(n_estimators=100, max_depth=12)",
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "train_mae_usd": round(train_mae, 2),
        "test_mae_usd": round(test_mae, 2),
        "test_rmse_usd": round(test_rmse, 2),
        "test_r2_score": round(test_r2, 4),
        "top_predictive_features": sorted_importances,
        "evaluation_period": "2024-01-01 to 2024-12-31 (Out-of-Time Validation)"
    }
    
    print(f"Evaluation Results -> Test MAE: ${test_mae:,.2f} | Test RMSE: ${test_rmse:,.2f} | Test R2: {test_r2:.4f}")
    
    # Save metrics
    metrics_path = os.path.join(ML_DIR, "forecast_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(f"Saved evaluation metrics to {metrics_path}")
    
    # Save model
    model_path = os.path.join(ML_DIR, "baseline_sales_forecaster.joblib")
    joblib.dump(model, model_path)
    print(f"Saved trained model artifact to {model_path}")
    
    # Generate sample inference predictions
    sample_eval = df.loc[test_mask, ["order_date", "territory_state", "daily_revenue", target_col]].copy()
    sample_eval["predicted_future_7d_revenue"] = np.round(y_pred_test, 2)
    sample_eval["forecast_error_usd"] = np.round(sample_eval["predicted_future_7d_revenue"] - sample_eval[target_col], 2)
    
    sample_output_path = os.path.join(ML_DIR, "sales_forecast_predictions_sample.csv")
    sample_eval.head(100).to_csv(sample_output_path, index=False)
    print(f"Saved sample test predictions to {sample_output_path}")

if __name__ == "__main__":
    run_forecaster()

