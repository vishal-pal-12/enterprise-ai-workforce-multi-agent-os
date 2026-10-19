-- =============================================================================
-- POSTGRESQL BULK CSV IMPORT SCRIPT (\copy)
-- Run via psql CLI: psql -U <username> -d <database_name> -f 02_import_csv_copy.sql
-- Note: Replace '/absolute/path/to' with your local project root path.
-- =============================================================================

-- 1. Government Open Data Benchmarks
\copy gov_benchmarks.asi_manufacturing_statistics FROM 'enterprise_database/ceo_orchestrator/asi_state_economic_health_index.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy gov_benchmarks.udyam_msme_registered_units FROM 'enterprise_database/sales_agent/gov_udyam_msme_b2b_market_opportunity.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy gov_benchmarks.dgcis_commodity_exports FROM 'enterprise_database/sales_agent/gov_dgcis_commodity_export_demand.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy gov_benchmarks.gst_state_revenue FROM 'enterprise_database/finance_agent/gov_gst_state_revenue_trends.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy gov_benchmarks.plfs_labour_benchmarks FROM 'enterprise_database/hr_agent/gov_plfs_labour_productivity_rates.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

-- 2. Human Resources (HR Agent)
\copy hr.departments FROM 'enterprise_database/hr_agent/adventureworks_departments.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy hr.employees FROM 'enterprise_database/hr_agent/adventureworks_employees.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

-- 3. Inventory & Supply Chain (Inventory Agent)
\copy inventory.products FROM 'enterprise_database/inventory_agent/adventureworks_product_inventory.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy inventory.purchase_orders FROM 'enterprise_database/inventory_agent/adventureworks_purchase_orders.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy inventory.warehouse_movements FROM 'enterprise_database/inventory_agent/adventureworks_warehouse_movements.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

-- 4. Sales Intelligence (Sales Agent)
\copy sales.customers FROM 'enterprise_database/sales_agent/adventureworks_b2b_customers.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy sales.orders FROM 'enterprise_database/sales_agent/adventureworks_sales_orders.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy sales.order_details FROM 'enterprise_database/sales_agent/adventureworks_sales_order_details.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

-- 5. Finance & Accounting (Finance Agent)
\copy finance.accounts_receivable FROM 'enterprise_database/finance_agent/adventureworks_accounts_receivable.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy finance.general_ledger FROM 'enterprise_database/finance_agent/adventureworks_general_ledger.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy finance.budget_vs_actuals FROM 'enterprise_database/finance_agent/adventureworks_budget_vs_actuals.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

-- 6. CEO Orchestrator (Executive Cross-Functional Views)
\copy ceo.executive_kpi_summary FROM 'enterprise_database/ceo_orchestrator/executive_kpi_summary.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

\copy ceo.strategic_initiatives FROM 'enterprise_database/ceo_orchestrator/strategic_initiatives_roadmap.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

