# Multi-Agent Enterprise Relational Schema & ER Diagram

This document illustrates the complete relational database architecture and boundary mappings for the **AI-Powered Multi-Agent Enterprise Automation System**, combining **Microsoft AdventureWorks OLTP** for enterprise operational tables with official **Government Open Data (data.gov.in / MOSPI ASI)** for macroeconomic and industrial benchmarks.

---

## 1. Entity-Relationship (ER) Architecture

```mermaid
erDiagram
    %% Core Sales Agent Domain
    SALES_CUSTOMERS ||--o{ SALES_ORDERS : "places (customer_id)"
    SALES_ORDERS ||--|{ SALES_ORDER_DETAILS : "contains (sales_order_id)"
    SALES_ORDERS ||--o{ FINANCE_ACCOUNTS_RECEIVABLE : "invoiced_as (sales_order_id)"
    SALES_CUSTOMERS ||--o{ FINANCE_ACCOUNTS_RECEIVABLE : "billed_to (customer_id)"

    %% Inventory Domain
    INVENTORY_PRODUCTS ||--o{ SALES_ORDER_DETAILS : "line_item (product_id)"
    INVENTORY_PRODUCTS ||--o{ INVENTORY_PURCHASE_ORDERS : "replenished_by (product_id)"

    %% HR Domain
    HR_DEPARTMENTS ||--|{ HR_EMPLOYEES : "employs (department_id)"
    HR_DEPARTMENTS ||--o{ FINANCE_BUDGET_ACTUALS : "allocates (department_id)"

    %% Finance & General Ledger
    SALES_ORDERS ||--o{ FINANCE_GENERAL_LEDGER : "generates_journal (reference_id)"

    %% Government Benchmark Joins (Macro & Regional)
    GOV_ASI_BENCHMARKS ||..o{ SALES_CUSTOMERS : "regional_industrial_benchmark (state_ut, nic_code)"
    GOV_UDYAM_MSME ||..o{ SALES_CUSTOMERS : "regional_msme_density (state_ut)"
    GOV_GST_REVENUE ||..o{ FINANCE_ACCOUNTS_RECEIVABLE : "tax_macro_trend (state_ut)"
    GOV_ASI_WAGES ||..o{ HR_EMPLOYEES : "wage_parity_benchmark (industry_sector)"

    %% CEO Orchestrator Synthesis
    CEO_EXECUTIVE_KPI ||..o{ SALES_ORDERS : "revenue_synthesis"
    CEO_EXECUTIVE_KPI ||..o{ HR_EMPLOYEES : "headcount_synthesis"
```

---

## 2. Agent Domain Responsibility & Table Ownership

| Agent Name | Schema / Namespace | Owned Relational Tables | External Benchmark Joins |
| :--- | :--- | :--- | :--- |
| **CEO Orchestrator** | `ceo.*` | `executive_kpi_summary`, `strategic_initiatives` | `asi_state_economic_health_index` (MOSPI ASI) |
| **Sales Agent** | `sales.*` | `customers`, `orders`, `order_details` | `gov_udyam_msme_b2b_market_opportunity`, `gov_dgcis_commodity_export_demand` |
| **HR Talent Agent** | `hr.*` | `departments`, `employees` | `gov_asi_manufacturing_wage_benchmarks`, `gov_plfs_labour_productivity_rates` |
| **Finance Agent** | `finance.*` | `general_ledger`, `accounts_receivable`, `budget_vs_actuals` | `gov_gst_state_revenue_trends` |
| **Inventory Agent** | `inventory.*` | `products`, `purchase_orders`, `warehouse_movements` | `gov_asi_industrial_input_costs` |

---

## 3. Referential Integrity Rules

1. **Order to Customer Integrity**:
   - `sales.orders(customer_id)` $\to$ `sales.customers(customer_id)`
   - Every sales order must be linked to a pre-existing enterprise account.
2. **Line Item to Order Integrity**:
   - `sales.order_details(sales_order_id)` $\to$ `sales.orders(sales_order_id)` (Cascade on delete).
3. **Line Item to Catalog Product Integrity**:
   - `sales.order_details(product_id)` $\to$ `inventory.products(product_id)`.
4. **Employee to Department Integrity**:
   - `hr.employees(department_id)` $\to$ `hr.departments(department_id)` (Restricted on delete).
5. **Invoice & Accounts Receivable Integrity**:
   - `finance.accounts_receivable(sales_order_id)` $\to$ `sales.orders(sales_order_id)`
   - `finance.accounts_receivable(customer_id)` $\to$ `sales.customers(customer_id)`.
6. **Government Benchmark Correlation**:
   - `sales.customers(state_ut)` maps to `gov_benchmarks.asi_manufacturing_statistics(state_ut)` and `gov_benchmarks.udyam_msme_registered_units(state_ut)`.
   - `sales.customers(nic_2digit_code)` maps to `gov_benchmarks.asi_manufacturing_statistics(nic_2digit_code)`.

