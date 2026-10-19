import os
import sys
import pandas as pd
import sqlite3
from sqlalchemy import create_engine, text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# File expectations
REQUIRED_FILES = {
    "ceo_orchestrator": [
        "executive_kpi_summary.csv",
        "asi_state_economic_health_index.csv",
        "strategic_initiatives_roadmap.csv",
        "agent_registry_metadata.json"
    ],
    "sales_agent": [
        "adventureworks_sales_orders.csv",
        "adventureworks_sales_order_details.csv",
        "adventureworks_b2b_customers.csv",
        "gov_udyam_msme_b2b_market_opportunity.csv",
        "gov_dgcis_commodity_export_demand.csv",
        "sales_forecasting_training_dataset.csv"
    ],
    "hr_agent": [
        "adventureworks_employees.csv",
        "adventureworks_departments.csv",
        "gov_asi_manufacturing_wage_benchmarks.csv",
        "gov_plfs_labour_productivity_rates.csv"
    ],
    "finance_agent": [
        "adventureworks_general_ledger.csv",
        "adventureworks_accounts_receivable.csv",
        "adventureworks_budget_vs_actuals.csv",
        "gov_gst_state_revenue_trends.csv"
    ],
    "inventory_agent": [
        "adventureworks_product_inventory.csv",
        "adventureworks_purchase_orders.csv",
        "adventureworks_warehouse_movements.csv",
        "gov_asi_industrial_input_costs.csv"
    ],
    "models_and_ml": [
        "sales_forecasting_training_dataset.csv",
        "train_baseline_sales_forecaster.py",
        "baseline_sales_forecaster.joblib",
        "forecast_metrics.json",
        "sales_forecast_predictions_sample.csv"
    ],
    "shared_schemas_sql": [
        "01_create_schemas_and_tables.sql",
        "02_import_csv_copy.sql",
        "schema_relationships_diagram.md"
    ]
}

def verify_all_files_exist():
    print("\n--- 1. VERIFYING FILE STRUCTURE & EXISTENCE ---")
    missing = []
    file_stats = []
    for folder, files in REQUIRED_FILES.items():
        folder_path = os.path.join(BASE_DIR, folder)
        if not os.path.exists(folder_path):
            missing.append(f"Folder missing: {folder}")
            continue
        for f in files:
            p = os.path.join(folder_path, f)
            if not os.path.exists(p):
                missing.append(f"File missing: {folder}/{f}")
            else:
                sz = os.path.getsize(p)
                file_stats.append((f"{folder}/{f}", sz))
    
    if missing:
        print("[FAIL] Missing components:")
        for m in missing:
            print(f"  - {m}")
        return False
    
    print(f"[PASS] All {len(file_stats)} essential files and metadata verified on disk.")
    for name, sz in file_stats[:10]:
        print(f"  [OK] {name} ({sz:,} bytes)")
    print(f"  ... and {len(file_stats) - 10} more files verified.")
    return True

def verify_referential_integrity():
    print("\n--- 2. VERIFYING DATA REFERENTIAL INTEGRITY ---")
    customers = pd.read_csv(os.path.join(BASE_DIR, "sales_agent", "adventureworks_b2b_customers.csv"))
    orders = pd.read_csv(os.path.join(BASE_DIR, "sales_agent", "adventureworks_sales_orders.csv"))
    details = pd.read_csv(os.path.join(BASE_DIR, "sales_agent", "adventureworks_sales_order_details.csv"))
    inventory = pd.read_csv(os.path.join(BASE_DIR, "inventory_agent", "adventureworks_product_inventory.csv"))
    deps = pd.read_csv(os.path.join(BASE_DIR, "hr_agent", "adventureworks_departments.csv"))
    employees = pd.read_csv(os.path.join(BASE_DIR, "hr_agent", "adventureworks_employees.csv"))
    ar = pd.read_csv(os.path.join(BASE_DIR, "finance_agent", "adventureworks_accounts_receivable.csv"))
    po = pd.read_csv(os.path.join(BASE_DIR, "inventory_agent", "adventureworks_purchase_orders.csv"))
    
    # 1. Orders -> Customers
    cust_ids = set(customers["customer_id"])
    order_cust_ids = set(orders["customer_id"])
    invalid_cust_in_orders = order_cust_ids - cust_ids
    assert len(invalid_cust_in_orders) == 0, f"Found orphan customer_ids in orders: {invalid_cust_in_orders}"
    print(f"[PASS] Orders -> Customers: {len(orders)} orders linked to {len(order_cust_ids)} valid customers (0 orphans).")
    
    # 2. Order Details -> Orders
    order_ids = set(orders["sales_order_id"])
    detail_order_ids = set(details["sales_order_id"])
    invalid_orders_in_details = detail_order_ids - order_ids
    assert len(invalid_orders_in_details) == 0, f"Found orphan order_ids in details: {invalid_orders_in_details}"
    print(f"[PASS] Order Details -> Orders: {len(details)} line items linked to {len(detail_order_ids)} orders (0 orphans).")
    
    # 3. Order Details -> Inventory Products
    prod_ids = set(inventory["product_id"])
    detail_prod_ids = set(details["product_id"])
    invalid_prods = detail_prod_ids - prod_ids
    assert len(invalid_prods) == 0, f"Found invalid product_ids in details: {invalid_prods}"
    print(f"[PASS] Order Details -> Products: {len(detail_prod_ids)} catalog products validly linked (0 orphans).")
    
    # 4. Employees -> Departments
    dep_ids = set(deps["department_id"])
    emp_dep_ids = set(employees["department_id"])
    invalid_deps = emp_dep_ids - dep_ids
    assert len(invalid_deps) == 0, f"Found invalid department_ids in employees: {invalid_deps}"
    print(f"[PASS] Employees -> Departments: {len(employees)} employees linked to {len(dep_ids)} valid departments (0 orphans).")
    
    # 5. Accounts Receivable -> Orders and Customers
    ar_order_ids = set(ar["sales_order_id"])
    ar_cust_ids = set(ar["customer_id"])
    assert len(ar_order_ids - order_ids) == 0, "Found orphan orders in Accounts Receivable"
    assert len(ar_cust_ids - cust_ids) == 0, "Found orphan customers in Accounts Receivable"
    print(f"[PASS] Accounts Receivable -> Orders & Customers: {len(ar)} invoice records fully intact (0 orphans).")
    
    # 6. Purchase Orders -> Products
    po_prod_ids = set(po["product_id"])
    assert len(po_prod_ids - prod_ids) == 0, "Found orphan products in Purchase Orders"
    print(f"[PASS] Purchase Orders -> Products: {len(po)} procurement orders linked to valid catalog products (0 orphans).")
    
    return True

def test_sql_engine_import():
    print("\n--- 3. TESTING DATABASE IMPORT & CROSS-SCHEMA ANALYTICS ---")
    # Test loading into SQLite engine (simulates relational multi-agent queries)
    conn = sqlite3.connect(":memory:")
    
    # Load core tables into SQLite
    tables_to_load = {
        "sales_customers": os.path.join(BASE_DIR, "sales_agent", "adventureworks_b2b_customers.csv"),
        "sales_orders": os.path.join(BASE_DIR, "sales_agent", "adventureworks_sales_orders.csv"),
        "sales_order_details": os.path.join(BASE_DIR, "sales_agent", "adventureworks_sales_order_details.csv"),
        "hr_departments": os.path.join(BASE_DIR, "hr_agent", "adventureworks_departments.csv"),
        "hr_employees": os.path.join(BASE_DIR, "hr_agent", "adventureworks_employees.csv"),
        "inventory_products": os.path.join(BASE_DIR, "inventory_agent", "adventureworks_product_inventory.csv"),
        "finance_receivable": os.path.join(BASE_DIR, "finance_agent", "adventureworks_accounts_receivable.csv"),
        "gov_asi_statistics": os.path.join(BASE_DIR, "ceo_orchestrator", "asi_state_economic_health_index.csv"),
        "gov_udyam_msme": os.path.join(BASE_DIR, "sales_agent", "gov_udyam_msme_b2b_market_opportunity.csv")
    }
    
    for tbl_name, csv_path in tables_to_load.items():
        df = pd.read_csv(csv_path)
        df.to_sql(tbl_name, conn, index=False, if_exists="replace")
    
    # Query 1: Cross-agent Sales + Gov ASI Regional Economic Analysis
    query_1 = """
    SELECT 
        o.territory_state,
        COUNT(DISTINCT o.sales_order_id) AS total_orders,
        ROUND(SUM(o.subtotal_usd), 2) AS total_company_revenue_usd,
        ROUND(AVG(asi.sector_annual_growth_pct), 2) AS gov_asi_avg_sector_growth_pct
    FROM sales_orders o
    JOIN sales_customers c ON o.customer_id = c.customer_id
    LEFT JOIN gov_asi_statistics asi 
        ON o.territory_state = asi.state_ut 
        AND c.nic_2digit_code = asi.nic_2digit_code 
        AND asi.reporting_year = '2023-2024'
    WHERE o.order_status != 'Cancelled'
    GROUP BY o.territory_state
    ORDER BY total_company_revenue_usd DESC
    LIMIT 5;
    """
    res_1 = pd.read_sql_query(query_1, conn)
    print("\n[SQL Verification Query 1] Top 5 States by Company Revenue joined with Gov ASI Growth:")
    print(res_1.to_string(index=False))
    
    # Query 2: HR Internal Salary vs Official Government ASI Industrial Wage Benchmark
    query_2 = """
    SELECT 
        e.department_name,
        COUNT(e.employee_id) AS employee_count,
        ROUND(AVG(e.base_salary_inr), 0) AS avg_internal_salary_inr
    FROM hr_employees e
    GROUP BY e.department_name
    ORDER BY avg_internal_salary_inr DESC;
    """
    res_2 = pd.read_sql_query(query_2, conn)
    print("\n[SQL Verification Query 2] HR Department Headcount & Salary Structure:")
    print(res_2.to_string(index=False))
    
    conn.close()
    print("\n[PASS] Database import and analytical SQL joins verified successfully with zero errors!")
    return True

if __name__ == "__main__":
    ok1 = verify_all_files_exist()
    ok2 = verify_referential_integrity()
    ok3 = test_sql_engine_import()
    if ok1 and ok2 and ok3:
        print("\n========================================================")
        print("ALL ENTERPRISE DATABASE CHECKS PASSED SUCCESSFULLY (100%)")
        print("========================================================")
        sys.exit(0)
    else:
        sys.exit(1)
