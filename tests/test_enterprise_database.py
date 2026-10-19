import os
import json
import joblib
import pandas as pd
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "enterprise_database")

def test_enterprise_folders_exist():
    expected_folders = [
        "ceo_orchestrator",
        "sales_agent",
        "hr_agent",
        "finance_agent",
        "inventory_agent",
        "models_and_ml",
        "shared_schemas_sql",
        "scripts"
    ]
    for folder in expected_folders:
        folder_path = os.path.join(DB_DIR, folder)
        assert os.path.isdir(folder_path), f"Folder {folder} does not exist in {DB_DIR}"

def test_referential_integrity_sales_and_customers():
    cust_file = os.path.join(DB_DIR, "sales_agent", "adventureworks_b2b_customers.csv")
    orders_file = os.path.join(DB_DIR, "sales_agent", "adventureworks_sales_orders.csv")
    details_file = os.path.join(DB_DIR, "sales_agent", "adventureworks_sales_order_details.csv")
    
    df_cust = pd.read_csv(cust_file)
    df_orders = pd.read_csv(orders_file)
    df_details = pd.read_csv(details_file)
    
    assert len(df_cust) >= 100
    assert len(df_orders) >= 1000
    assert len(df_details) >= 2000
    
    # Check FK: Orders -> Customers
    cust_ids = set(df_cust["customer_id"])
    order_cust_ids = set(df_orders["customer_id"])
    assert order_cust_ids.issubset(cust_ids), "Orphan customer_ids found in orders table"
    
    # Check FK: Details -> Orders
    order_ids = set(df_orders["sales_order_id"])
    detail_order_ids = set(df_details["sales_order_id"])
    assert detail_order_ids.issubset(order_ids), "Orphan sales_order_ids found in order details table"

def test_referential_integrity_hr():
    dep_file = os.path.join(DB_DIR, "hr_agent", "adventureworks_departments.csv")
    emp_file = os.path.join(DB_DIR, "hr_agent", "adventureworks_employees.csv")
    
    df_dep = pd.read_csv(dep_file)
    df_emp = pd.read_csv(emp_file)
    
    assert len(df_dep) >= 5
    assert len(df_emp) >= 100
    
    dep_ids = set(df_dep["department_id"])
    emp_dep_ids = set(df_emp["department_id"])
    assert emp_dep_ids.issubset(dep_ids), "Orphan department_ids found in employees table"

def test_government_data_sources_valid():
    asi_file = os.path.join(DB_DIR, "ceo_orchestrator", "asi_state_economic_health_index.csv")
    msme_file = os.path.join(DB_DIR, "sales_agent", "gov_udyam_msme_b2b_market_opportunity.csv")
    gst_file = os.path.join(DB_DIR, "finance_agent", "gov_gst_state_revenue_trends.csv")
    
    df_asi = pd.read_csv(asi_file)
    df_msme = pd.read_csv(msme_file)
    df_gst = pd.read_csv(gst_file)
    
    assert "nic_2digit_code" in df_asi.columns
    assert "number_of_factories" in df_asi.columns
    assert len(df_asi) > 200
    
    assert "registered_units_count" in df_msme.columns
    assert "enterprise_category" in df_msme.columns
    
    assert "gross_gst_collection_inr_crore" in df_gst.columns
    assert len(df_gst) > 100

def test_baseline_forecasting_model():
    model_file = os.path.join(DB_DIR, "models_and_ml", "baseline_sales_forecaster.joblib")
    metrics_file = os.path.join(DB_DIR, "models_and_ml", "forecast_metrics.json")
    dataset_file = os.path.join(DB_DIR, "models_and_ml", "sales_forecasting_training_dataset.csv")
    
    assert os.path.isfile(model_file), "Trained model joblib missing"
    assert os.path.isfile(metrics_file), "Metrics JSON missing"
    
    model = joblib.load(model_file)
    df_ml = pd.read_csv(dataset_file)
    
    feature_cols = [
        "daily_order_count", "daily_revenue",
        "day_of_week", "day_of_month", "month", "quarter", "is_weekend", "is_quarter_end",
        "lag_1d_revenue", "lag_7d_revenue", "lag_14d_revenue", "lag_30d_revenue",
        "rolling_mean_7d", "rolling_std_7d", "rolling_mean_30d",
        "state_gov_asi_share_pct", "state_gov_gst_share_pct"
    ]
    
    sample_X = df_ml.head(5)[feature_cols]
    preds = model.predict(sample_X)
    assert len(preds) == 5
    assert not any(pd.isna(preds))

def test_sql_schema_files_exist_and_non_empty():
    ddl_file = os.path.join(DB_DIR, "shared_schemas_sql", "01_create_schemas_and_tables.sql")
    copy_file = os.path.join(DB_DIR, "shared_schemas_sql", "02_import_csv_copy.sql")
    er_file = os.path.join(DB_DIR, "shared_schemas_sql", "schema_relationships_diagram.md")
    
    assert os.path.isfile(ddl_file) and os.path.getsize(ddl_file) > 1000
    assert os.path.isfile(copy_file) and os.path.getsize(copy_file) > 500
    assert os.path.isfile(er_file) and os.path.getsize(er_file) > 500

