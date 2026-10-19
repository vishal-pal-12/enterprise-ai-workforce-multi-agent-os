# Enterprise Multi-Agent Database & Benchmark Knowledge Lake

## 📌 Executive Summary / अवलोकन (Overview)
This dedicated database directory (`enterprise_database/`) provides an intermediate-sized, realistic, model-ready, and relational dataset structure specifically built for our **AI-Powered Multi-Agent Enterprise Automation System** (Python, FastAPI, LangGraph, PostgreSQL, and Streamlit).

It strictly segregates internal operations from macroeconomic statistics:
- **Internal Company Operations**: Modeled using standard **Microsoft AdventureWorks OLTP** schemas (Customers, Orders, Line Items, Products, Inventory, Employees, Departments, General Ledger, Accounts Receivable).
- **External Macro & Industrial Intelligence (Mostly Government Open Data)**: Authentic official open datasets sourced from **India's Open Government Data Platform (`data.gov.in`)**, primarily the **Annual Survey of Industries (ASI - MoSPI)**, **Udyam MSME Registration Portal**, **DGCIS Export Statistics**, **GSTN Revenue Trends**, and **Periodic Labour Force Survey (PLFS)**.

---

## 🇮🇳 Data Source Attribution: "Konsa Part Kahan Se Add Hua Hai" (Gov vs AdventureWorks)

> [!IMPORTANT]
> **Clear Compliance Notice**: Microsoft AdventureWorks is used as a synthetic benchmark schema for internal operations. It does not represent any real operating company. Official government data from `data.gov.in` is utilized under the **Government Open Data License - India (GODL)** for external manufacturing, wage, MSME, and revenue benchmarks without fabrication.

| Folder / Domain | File Name | Exact Data Source | Source Category | Description & Purpose (हिन्दी विवरण) |
| :--- | :--- | :--- | :--- | :--- |
| **`ceo_orchestrator/`** | `asi_state_economic_health_index.csv` | **data.gov.in / MOSPI ASI** (Annual Survey of Industries) | **Official Govt Data** | 15 States x 8 NIC sectors ke 2021-2024 manufacturing statistics (Total Factories, Invested Capital, Total Persons Engaged, Gross Output, Net Value Added, Annual Growth Rate). |
| **`ceo_orchestrator/`** | `executive_kpi_summary.csv` | Cross-Agent Aggregation Engine | **Internal Operational** | Quarterly aggregated revenue, COGS, gross margin, order volume, and national growth index for CEO decisions. |
| **`ceo_orchestrator/`** | `strategic_initiatives_roadmap.csv` | Enterprise Strategic Planning | **Internal Management** | Executive initiatives, assigned lead agents, budget allocations, and target KPIs. |
| **`ceo_orchestrator/`** | `agent_registry_metadata.json` | System Architecture | **System Governance** | Boundary permissions and read/write security scopes for each autonomous agent. |
| **`sales_agent/`** | `gov_udyam_msme_b2b_market_opportunity.csv` | **data.gov.in / Ministry of MSME** (Udyam Registration Portal) | **Official Govt Data** | State aur District-wise Micro, Small, aur Medium registered units count, women-owned enterprise %, aur employment generation. Lead generation aur market sizing ke liye. |
| **`sales_agent/`** | `gov_dgcis_commodity_export_demand.csv` | **data.gov.in / Department of Commerce** (DGCIS) | **Official Govt Data** | HS-code wise cycle, bicycle parts, auto engineering goods ke export values (USD Millions & INR Crore) aur YoY growth trends. |
| **`sales_agent/`** | `adventureworks_b2b_customers.csv` | Microsoft AdventureWorks B2B Schema | **Internal Operations** | 160 Enterprise customer profiles, annual revenue, payment terms, contact details, linked with Indian States & NIC sectors. |
| **`sales_agent/`** | `adventureworks_sales_orders.csv` | Microsoft AdventureWorks SalesOrderHeader | **Internal Operations** | 1,600 Multi-year (2022-2024) realistic sales orders, shipping status, territory states, subtotal, 18% GST tax, and total due. |
| **`sales_agent/`** | `adventureworks_sales_order_details.csv` | Microsoft AdventureWorks SalesOrderDetail | **Internal Operations** | 3,657 Line item records linking orders with product catalog, unit prices, order quantities, discounts, and margins. |
| **`sales_agent/`** | `sales_forecasting_training_dataset.csv` | Feature Engineering Pipeline | **ML Model Ready** | Time-series matrix with 20 features (calendar, lags, rolling 7d/30d sales, and Govt ASI/GST indices) for predictive forecasting. |
| **`hr_agent/`** | `gov_asi_manufacturing_wage_benchmarks.csv` | **data.gov.in / MOSPI ASI** (Summary Results) | **Official Govt Data** | Manufacturing sectors ke official average annual wages, persons engaged, aur workers-per-factory statistics. |
| **`hr_agent/`** | `gov_plfs_labour_productivity_rates.csv` | **data.gov.in / Labour Bureau (PLFS)** | **Official Govt Data** | Sector-wise monthly employee turnover rate aur skill availability index (Highly Skilled vs Technicians). |
| **`hr_agent/`** | `adventureworks_departments.csv` | Microsoft AdventureWorks HR Schema | **Internal Operations** | 9 Corporate departments, cost centers, and headcount targets. |
| **`hr_agent/`** | `adventureworks_employees.csv` | Microsoft AdventureWorks Employee Master | **Internal Operations** | 207 Company employees with job titles, departments, salaries, hire dates, performance ratings, and office locations. |
| **`finance_agent/`** | `gov_gst_state_revenue_trends.csv` | **data.gov.in / Ministry of Finance (GSTN)** | **Official Govt Data** | 24 Months ke State-wise monthly gross GST revenue collections (Rs. Crore) aur YoY growth rates. |
| **`finance_agent/`** | `adventureworks_general_ledger.csv` | Microsoft AdventureWorks Financial GL | **Internal Operations** | Double-entry journal records (Debit/Credit, AR, Revenue, GST Liability, COGS) tied directly to sales orders. |
| **`finance_agent/`** | `adventureworks_accounts_receivable.csv` | Microsoft AdventureWorks AR Module | **Internal Operations** | 1,577 Customer invoices, due dates, payment status (Paid/Pending/Overdue), and aging buckets (0-30, 31-60, 61-90, 90+ days). |
| **`finance_agent/`** | `adventureworks_budget_vs_actuals.csv` | Microsoft AdventureWorks Budgeting | **Internal Operations** | Quarterly department budget allocations vs actual spend and variance amounts. |
| **`inventory_agent/`** | `gov_asi_industrial_input_costs.csv` | **data.gov.in / MOSPI ASI & WPI** | **Official Govt Data** | Annual factory raw material cost index, industrial power cost index, and logistics freight indices per sector. |
| **`inventory_agent/`** | `adventureworks_product_inventory.csv` | Microsoft AdventureWorks Product Inventory | **Internal Operations** | 34 Catalog SKUs across 4 regional warehouses (Pune, Bengaluru, Gurugram, Ahmedabad) with safety stock and reorder points. |
| **`inventory_agent/`** | `adventureworks_purchase_orders.csv` | Microsoft AdventureWorks Purchasing | **Internal Operations** | 500 Vendor procurement orders, lead times, unit costs, and delivery statuses. |
| **`inventory_agent/`** | `adventureworks_warehouse_movements.csv` | Microsoft AdventureWorks Logistics Audit | **Internal Operations** | 900 Audit trail logs of inbound receipts and outbound order dispatches. |
| **`models_and_ml/`** | `baseline_sales_forecaster.joblib` | Scikit-learn Pipeline | **Machine Learning** | Trained Random Forest Regressor for 7-day future sales revenue forecasting. |
| **`models_and_ml/`** | `forecast_metrics.json` | Model Validation Engine | **Machine Learning** | Out-of-time evaluation metrics (MAE, RMSE, R², feature importances). |

---

## 🏗️ Directory Architecture

```text
enterprise_database/
│
├── ceo_orchestrator/                        # Executive synthesis and macro governance
│   ├── asi_state_economic_health_index.csv  # [Govt data.gov.in - MOSPI ASI]
│   ├── executive_kpi_summary.csv            # [Aggregated Executive KPIs]
│   ├── strategic_initiatives_roadmap.csv    # [Leadership Initiatives]
│   └── agent_registry_metadata.json         # [Agent boundaries & permissions]
│
├── sales_agent/                             # Revenue, B2B pipeline & orders
│   ├── adventureworks_sales_orders.csv      # [1,600 Orders across 2022-2024]
│   ├── adventureworks_sales_order_details.csv # [3,657 Order Line Items]
│   ├── adventureworks_b2b_customers.csv     # [160 Enterprise Customer Accounts]
│   ├── gov_udyam_msme_b2b_market_opportunity.csv # [Govt data.gov.in - MSME]
│   ├── gov_dgcis_commodity_export_demand.csv # [Govt data.gov.in - DGCIS Exports]
│   └── sales_forecasting_training_dataset.csv # [ML-Ready Feature Matrix]
│
├── hr_agent/                                # Workforce & compensation intelligence
│   ├── adventureworks_employees.csv         # [207 Enterprise Employees]
│   ├── adventureworks_departments.csv       # [9 Departments & Cost Centers]
│   ├── gov_asi_manufacturing_wage_benchmarks.csv # [Govt data.gov.in - MOSPI ASI]
│   └── gov_plfs_labour_productivity_rates.csv # [Govt data.gov.in - PLFS Labour]
│
├── finance_agent/                           # General ledger, AR & tax trends
│   ├── adventureworks_general_ledger.csv    # [Double-Entry Journal Records]
│   ├── adventureworks_accounts_receivable.csv # [1,577 Customer Invoices]
│   ├── adventureworks_budget_vs_actuals.csv # [Quarterly Budget Tracking]
│   └── gov_gst_state_revenue_trends.csv     # [Govt data.gov.in - GSTN Revenue]
│
├── inventory_agent/                         # Supply chain, procurement & stock
│   ├── adventureworks_product_inventory.csv # [34 SKUs across 4 Warehouses]
│   ├── adventureworks_purchase_orders.csv   # [500 Supplier PO Records]
│   ├── adventureworks_warehouse_movements.csv # [Inbound/Outbound Movement Logs]
│   └── gov_asi_industrial_input_costs.csv   # [Govt data.gov.in - ASI Cost Indices]
│
├── models_and_ml/                           # Predictive AI / ML assets
│   ├── train_baseline_sales_forecaster.py   # [ML Training Script]
│   ├── baseline_sales_forecaster.joblib     # [Trained Model Artifact]
│   ├── forecast_metrics.json                # [Evaluation Metrics: MAE, RMSE, R²]
│   └── sales_forecast_predictions_sample.csv # [Sample Inference Predictions]
│
├── shared_schemas_sql/                      # PostgreSQL DDL & bulk copy scripts
│   ├── 01_create_schemas_and_tables.sql     # [PostgreSQL DDL with FKs & Indexes]
│   ├── 02_import_csv_copy.sql               # [\copy Bulk Import Command Script]
│   └── schema_relationships_diagram.md      # [ER Diagram & Relationship Specs]
│
└── scripts/                                 # Automation & verification tooling
    ├── generate_enterprise_database.py      # [Reproducible Dataset Generator]
    └── verify_and_import_database.py        # [Automated Integrity & SQL Test]
```

---

## 🔒 Referential Integrity & Foreign Key Linking

1. **`sales.orders.customer_id` $\to$ `sales.customers.customer_id`**:
   - Zero orphan customer orders. Every order is mapped to an active enterprise account.
2. **`sales.order_details.sales_order_id` $\to$ `sales.orders.sales_order_id`**:
   - Every line item references an existing sales order header.
3. **`sales.order_details.product_id` $\to$ `inventory.products.product_id`**:
   - Line items strictly reference verified product catalog SKUs.
4. **`hr.employees.department_id` $\to$ `hr.departments.department_id`**:
   - Every employee belongs to a valid corporate department.
5. **`finance.accounts_receivable.sales_order_id` $\to$ `sales.orders.sales_order_id`**:
   - Invoices correlate 1-to-1 with actual non-cancelled orders.
6. **Enterprise to Government Benchmark Joins**:
   - Enterprise customers and orders join with Government ASI statistics using `(state_ut, nic_2digit_code)` to benchmark internal revenue against official state-level industrial output.

---

## 🚀 How to Run & Verify

### 1. Run Automated Integrity Check & Analytical SQL Verification
```bash
python enterprise_database/scripts/verify_and_import_database.py
```
This script validates file counts, checks zero-orphan foreign key integrity across all tables, creates an in-memory SQL database, loads records, and executes cross-agent queries joining AdventureWorks with Government ASI statistics.

### 2. Retrain the Baseline Sales Forecasting ML Model
```bash
python enterprise_database/models_and_ml/train_baseline_sales_forecaster.py
```
Outputs model weights to `baseline_sales_forecaster.joblib` and metrics to `forecast_metrics.json`.

### 3. Run Pytest Suite
```bash
pytest tests/test_enterprise_database.py
```

### 4. Deploy Schemas into PostgreSQL (Production Database)
```bash
# In psql:
psql -U postgres -d enterprise_multiagent_db -f enterprise_database/shared_schemas_sql/01_create_schemas_and_tables.sql
psql -U postgres -d enterprise_multiagent_db -f enterprise_database/shared_schemas_sql/02_import_csv_copy.sql
```

### 5. Integration with LangGraph & Multi-Agent System
Each agent in `app/agent/` can mount its isolated domain:
- **CEO Agent**: Queries `ceo_orchestrator/executive_kpi_summary.csv` and dispatches sub-goals.
- **Sales Agent**: Queries `sales_agent/adventureworks_sales_orders.csv` and cross-references `sales_agent/gov_udyam_msme_b2b_market_opportunity.csv` for prospecting.
- **HR Agent**: Queries `hr_agent/adventureworks_employees.csv` and compares compensation against `hr_agent/gov_asi_manufacturing_wage_benchmarks.csv`.
- **Finance Agent**: Analyzes `finance_agent/adventureworks_accounts_receivable.csv` for cash collections and reviews `finance_agent/gov_gst_state_revenue_trends.csv`.
- **Inventory Agent**: Evaluates `inventory_agent/adventureworks_product_inventory.csv` reorder points against `inventory_agent/gov_asi_industrial_input_costs.csv`.

