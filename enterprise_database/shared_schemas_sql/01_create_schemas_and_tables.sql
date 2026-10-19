-- =============================================================================
-- AI-POWERED MULTI-AGENT ENTERPRISE AUTOMATION SYSTEM
-- DATABASE SCHEMA SPECIFICATION FOR POSTGRESQL 14+
-- =============================================================================
-- Enterprise Operations: Microsoft AdventureWorks OLTP Schema Standard
-- External Benchmarks: Official Government Open Data (data.gov.in / MOSPI ASI)
-- =============================================================================

-- 1. Create Dedicated Namespaces (Schemas) for Agent Isolation
CREATE SCHEMA IF NOT EXISTS ceo;
CREATE SCHEMA IF NOT EXISTS sales;
CREATE SCHEMA IF NOT EXISTS hr;
CREATE SCHEMA IF NOT EXISTS finance;
CREATE SCHEMA IF NOT EXISTS inventory;
CREATE SCHEMA IF NOT EXISTS gov_benchmarks;

-- =============================================================================
-- 2. GOVERNMENT OPEN DATA BENCHMARKS (DATA.GOV.IN / MOSPI ASI)
-- =============================================================================

-- 2.1 ASI Manufacturing Industry Statistics (MoSPI / data.gov.in)
CREATE TABLE IF NOT EXISTS gov_benchmarks.asi_manufacturing_statistics (
    reporting_year VARCHAR(20) NOT NULL,
    state_ut VARCHAR(100) NOT NULL,
    zone VARCHAR(50),
    nic_2digit_code VARCHAR(10) NOT NULL,
    industry_sector VARCHAR(255) NOT NULL,
    number_of_factories INTEGER NOT NULL,
    fixed_capital_inr_lakh NUMERIC(14, 2) NOT NULL,
    total_persons_engaged INTEGER NOT NULL,
    wages_to_workers_inr_lakh NUMERIC(14, 2) NOT NULL,
    gross_output_inr_lakh NUMERIC(14, 2) NOT NULL,
    net_value_added_inr_lakh NUMERIC(14, 2) NOT NULL,
    sector_annual_growth_pct NUMERIC(6, 2),
    data_source VARCHAR(255) DEFAULT 'data.gov.in/MOSPI-ASI-Summary-Results',
    license VARCHAR(100) DEFAULT 'GODL-India',
    PRIMARY KEY (reporting_year, state_ut, nic_2digit_code)
);
CREATE INDEX IF NOT EXISTS idx_asi_state ON gov_benchmarks.asi_manufacturing_statistics (state_ut);
CREATE INDEX IF NOT EXISTS idx_asi_nic ON gov_benchmarks.asi_manufacturing_statistics (nic_2digit_code);

-- 2.2 Udyam MSME Regional Registration Counts (Ministry of MSME / data.gov.in)
CREATE TABLE IF NOT EXISTS gov_benchmarks.udyam_msme_registered_units (
    state_ut VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    enterprise_category VARCHAR(50) NOT NULL, -- Micro, Small, Medium
    registered_units_count INTEGER NOT NULL,
    women_owned_units_pct NUMERIC(5, 2),
    total_estimated_employment INTEGER,
    reporting_year VARCHAR(20) NOT NULL,
    source_portal VARCHAR(255) DEFAULT 'data.gov.in/resource/udyam-registration-statistics',
    license VARCHAR(100) DEFAULT 'GODL-India',
    PRIMARY KEY (state_ut, district, enterprise_category, reporting_year)
);
CREATE INDEX IF NOT EXISTS idx_msme_state_dist ON gov_benchmarks.udyam_msme_registered_units (state_ut, district);

-- 2.3 DGCIS Commodity-Wise Export Statistics (Ministry of Commerce & Industry)
CREATE TABLE IF NOT EXISTS gov_benchmarks.dgcis_commodity_exports (
    reporting_year VARCHAR(20) NOT NULL,
    hs_code VARCHAR(20) NOT NULL,
    commodity_description VARCHAR(255) NOT NULL,
    export_value_usd_million NUMERIC(12, 2) NOT NULL,
    export_value_inr_crore NUMERIC(14, 2) NOT NULL,
    yoy_growth_percentage NUMERIC(6, 2),
    source_authority VARCHAR(255) DEFAULT 'DGCIS / data.gov.in',
    license VARCHAR(100) DEFAULT 'GODL',
    PRIMARY KEY (reporting_year, hs_code)
);

-- 2.4 State-wise GST Revenue Collections (Ministry of Finance / data.gov.in)
CREATE TABLE IF NOT EXISTS gov_benchmarks.gst_state_revenue (
    month_year VARCHAR(10) NOT NULL, -- YYYY-MM
    state_ut VARCHAR(100) NOT NULL,
    gross_gst_collection_inr_crore NUMERIC(12, 2) NOT NULL,
    yoy_growth_rate_pct NUMERIC(6, 2),
    source_authority VARCHAR(255) DEFAULT 'GSTN / Ministry of Finance / data.gov.in',
    license VARCHAR(100) DEFAULT 'GODL',
    PRIMARY KEY (month_year, state_ut)
);
CREATE INDEX IF NOT EXISTS idx_gst_state ON gov_benchmarks.gst_state_revenue (state_ut);

-- 2.5 Labour Productivity & Turnover Benchmarks (PLFS / Labour Bureau)
CREATE TABLE IF NOT EXISTS gov_benchmarks.plfs_labour_benchmarks (
    industry_sector VARCHAR(255) NOT NULL,
    skill_tier VARCHAR(100) NOT NULL,
    avg_monthly_turnover_pct NUMERIC(5, 2) NOT NULL,
    availability_index NUMERIC(6, 2) NOT NULL,
    source_authority VARCHAR(255) DEFAULT 'PLFS / data.gov.in',
    PRIMARY KEY (industry_sector, skill_tier)
);

-- =============================================================================
-- 3. HUMAN RESOURCES AGENT (HR_AGENT)
-- =============================================================================

CREATE TABLE IF NOT EXISTS hr.departments (
    department_id VARCHAR(20) PRIMARY KEY,
    department_name VARCHAR(150) NOT NULL,
    cost_center VARCHAR(50) NOT NULL UNIQUE,
    head_count_target INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS hr.employees (
    employee_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    work_email VARCHAR(200) NOT NULL UNIQUE,
    department_id VARCHAR(20) NOT NULL REFERENCES hr.departments(department_id) ON DELETE RESTRICT,
    department_name VARCHAR(150) NOT NULL,
    job_title VARCHAR(150) NOT NULL,
    base_salary_inr NUMERIC(12, 2) NOT NULL,
    hire_date DATE NOT NULL,
    performance_rating NUMERIC(3, 1),
    attrition_risk VARCHAR(20) DEFAULT 'Low',
    office_location VARCHAR(100) NOT NULL,
    source_system VARCHAR(100) DEFAULT 'Microsoft AdventureWorks HumanResources OLTP'
);
CREATE INDEX IF NOT EXISTS idx_emp_dept ON hr.employees (department_id);
CREATE INDEX IF NOT EXISTS idx_emp_state ON hr.employees (office_location);

-- =============================================================================
-- 4. INVENTORY & SUPPLY CHAIN AGENT (INVENTORY_AGENT)
-- =============================================================================

CREATE TABLE IF NOT EXISTS inventory.products (
    product_id VARCHAR(30) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_category VARCHAR(100) NOT NULL,
    product_subcategory VARCHAR(100) NOT NULL,
    warehouse_id VARCHAR(30) NOT NULL,
    warehouse_location VARCHAR(100) NOT NULL,
    warehouse_description TEXT,
    unit_cost_usd NUMERIC(10, 2) NOT NULL,
    list_price_usd NUMERIC(10, 2) NOT NULL,
    unit_margin_pct NUMERIC(6, 2) NOT NULL,
    safety_stock_level INTEGER NOT NULL,
    reorder_point INTEGER NOT NULL,
    quantity_on_hand INTEGER NOT NULL,
    quantity_reserved INTEGER DEFAULT 0,
    reorder_needed_flag INTEGER DEFAULT 0,
    last_restocked_date DATE,
    source_system VARCHAR(100) DEFAULT 'Microsoft AdventureWorks Inventory OLTP',
    PRIMARY KEY (product_id, warehouse_id)
);
CREATE INDEX IF NOT EXISTS idx_prod_id ON inventory.products (product_id);
CREATE INDEX IF NOT EXISTS idx_prod_cat ON inventory.products (product_category);

CREATE TABLE IF NOT EXISTS inventory.purchase_orders (
    purchase_order_id VARCHAR(30) PRIMARY KEY,
    vendor_id VARCHAR(30) NOT NULL,
    vendor_name VARCHAR(200) NOT NULL,
    vendor_location VARCHAR(100),
    product_id VARCHAR(30) NOT NULL,
    order_qty INTEGER NOT NULL,
    unit_purchase_cost_usd NUMERIC(10, 2) NOT NULL,
    total_po_amount_usd NUMERIC(12, 2) NOT NULL,
    order_date DATE NOT NULL,
    delivery_status VARCHAR(50) NOT NULL,
    lead_time_days INTEGER NOT NULL,
    source_system VARCHAR(100) DEFAULT 'Microsoft AdventureWorks Purchasing Module'
);
CREATE INDEX IF NOT EXISTS idx_po_product ON inventory.purchase_orders (product_id);

CREATE TABLE IF NOT EXISTS inventory.warehouse_movements (
    movement_id VARCHAR(30) PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    movement_type VARCHAR(50) NOT NULL, -- OUTBOUND_SALE, INBOUND_PROCUREMENT, TRANSFER
    reference_id VARCHAR(50) NOT NULL,
    warehouse_id VARCHAR(30) NOT NULL,
    status VARCHAR(50) NOT NULL,
    notes TEXT
);

-- =============================================================================
-- 5. SALES INTELLIGENCE AGENT (SALES_AGENT)
-- =============================================================================

CREATE TABLE IF NOT EXISTS sales.customers (
    customer_id VARCHAR(30) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    primary_contact_name VARCHAR(150) NOT NULL,
    contact_email VARCHAR(200) NOT NULL,
    state_ut VARCHAR(100) NOT NULL,
    nic_2digit_code VARCHAR(10) NOT NULL,
    industry_sector VARCHAR(255) NOT NULL,
    annual_revenue_usd NUMERIC(14, 2) NOT NULL,
    credit_limit_usd NUMERIC(14, 2) NOT NULL,
    payment_terms VARCHAR(50) NOT NULL,
    account_health VARCHAR(50) DEFAULT 'Active',
    account_established_year INTEGER NOT NULL,
    source_system VARCHAR(100) DEFAULT 'Microsoft AdventureWorks Sales & CRM OLTP'
);
CREATE INDEX IF NOT EXISTS idx_cust_state ON sales.customers (state_ut);
CREATE INDEX IF NOT EXISTS idx_cust_nic ON sales.customers (nic_2digit_code);

CREATE TABLE IF NOT EXISTS sales.orders (
    sales_order_id VARCHAR(30) PRIMARY KEY,
    order_date DATE NOT NULL,
    order_year INTEGER NOT NULL,
    order_quarter VARCHAR(10) NOT NULL,
    order_month VARCHAR(10) NOT NULL,
    customer_id VARCHAR(30) NOT NULL REFERENCES sales.customers(customer_id) ON DELETE RESTRICT,
    company_name VARCHAR(255) NOT NULL,
    territory_state VARCHAR(100) NOT NULL,
    subtotal_usd NUMERIC(12, 2) NOT NULL,
    tax_amt_usd NUMERIC(12, 2) NOT NULL,
    freight_usd NUMERIC(12, 2) NOT NULL,
    total_due_usd NUMERIC(12, 2) NOT NULL,
    cogs_usd NUMERIC(12, 2) NOT NULL,
    gross_margin_usd NUMERIC(12, 2) NOT NULL,
    order_status VARCHAR(50) NOT NULL,
    payment_terms VARCHAR(50) NOT NULL,
    source_system VARCHAR(100) DEFAULT 'Microsoft AdventureWorks SalesOrderHeader OLTP'
);
CREATE INDEX IF NOT EXISTS idx_orders_cust ON sales.orders (customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_date ON sales.orders (order_date);
CREATE INDEX IF NOT EXISTS idx_orders_state ON sales.orders (territory_state);

CREATE TABLE IF NOT EXISTS sales.order_details (
    order_detail_id VARCHAR(30) PRIMARY KEY,
    sales_order_id VARCHAR(30) NOT NULL REFERENCES sales.orders(sales_order_id) ON DELETE CASCADE,
    product_id VARCHAR(30) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_category VARCHAR(100) NOT NULL,
    order_qty INTEGER NOT NULL,
    unit_price_usd NUMERIC(10, 2) NOT NULL,
    unit_price_discount_pct NUMERIC(5, 2) DEFAULT 0.0,
    line_total_usd NUMERIC(12, 2) NOT NULL,
    unit_cost_usd NUMERIC(10, 2) NOT NULL,
    line_gross_profit_usd NUMERIC(12, 2) NOT NULL,
    source_system VARCHAR(100) DEFAULT 'Microsoft AdventureWorks SalesOrderDetail OLTP'
);
CREATE INDEX IF NOT EXISTS idx_detail_order ON sales.order_details (sales_order_id);
CREATE INDEX IF NOT EXISTS idx_detail_prod ON sales.order_details (product_id);

-- =============================================================================
-- 6. FINANCE & ACCOUNTING AGENT (FINANCE_AGENT)
-- =============================================================================

CREATE TABLE IF NOT EXISTS finance.accounts_receivable (
    invoice_number VARCHAR(30) PRIMARY KEY,
    sales_order_id VARCHAR(30) NOT NULL REFERENCES sales.orders(sales_order_id) ON DELETE RESTRICT,
    customer_id VARCHAR(30) NOT NULL REFERENCES sales.customers(customer_id) ON DELETE RESTRICT,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    invoice_amount_usd NUMERIC(12, 2) NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    paid_date DATE,
    aging_bucket VARCHAR(50) NOT NULL,
    source_system VARCHAR(100) DEFAULT 'Microsoft AdventureWorks AR Module'
);
CREATE INDEX IF NOT EXISTS idx_ar_cust ON finance.accounts_receivable (customer_id);
CREATE INDEX IF NOT EXISTS idx_ar_status ON finance.accounts_receivable (payment_status);

CREATE TABLE IF NOT EXISTS finance.general_ledger (
    journal_entry_id VARCHAR(30) PRIMARY KEY,
    transaction_date DATE NOT NULL,
    account_code VARCHAR(20) NOT NULL,
    account_name VARCHAR(150) NOT NULL,
    entry_type VARCHAR(10) NOT NULL, -- Debit / Credit
    amount_usd NUMERIC(12, 2) NOT NULL,
    reference_type VARCHAR(50) NOT NULL, -- SalesOrder, PurchaseOrder, Payroll
    reference_id VARCHAR(50) NOT NULL,
    description TEXT
);
CREATE INDEX IF NOT EXISTS idx_gl_date ON finance.general_ledger (transaction_date);
CREATE INDEX IF NOT EXISTS idx_gl_acc ON finance.general_ledger (account_code);

CREATE TABLE IF NOT EXISTS finance.budget_vs_actuals (
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter VARCHAR(10) NOT NULL,
    department_id VARCHAR(20) NOT NULL REFERENCES hr.departments(department_id) ON DELETE RESTRICT,
    department_name VARCHAR(150) NOT NULL,
    cost_center VARCHAR(50) NOT NULL,
    budget_allocated_usd NUMERIC(14, 2) NOT NULL,
    actual_spend_usd NUMERIC(14, 2) NOT NULL,
    variance_amount_usd NUMERIC(14, 2) NOT NULL,
    variance_percentage NUMERIC(6, 2) NOT NULL,
    approval_status VARCHAR(50) DEFAULT 'Approved',
    source_system VARCHAR(100) DEFAULT 'Microsoft AdventureWorks Corporate Financial Planning',
    PRIMARY KEY (fiscal_year, fiscal_quarter, department_id)
);

-- =============================================================================
-- 7. CEO ORCHESTRATOR AGENT (CEO_ORCHESTRATOR)
-- =============================================================================

CREATE TABLE IF NOT EXISTS ceo.executive_kpi_summary (
    period VARCHAR(20) PRIMARY KEY, -- YYYY-QX
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter VARCHAR(10) NOT NULL,
    net_revenue_usd NUMERIC(14, 2) NOT NULL,
    cogs_usd NUMERIC(14, 2) NOT NULL,
    gross_profit_usd NUMERIC(14, 2) NOT NULL,
    gross_margin_pct NUMERIC(6, 2) NOT NULL,
    total_orders_processed INTEGER NOT NULL,
    active_headcount INTEGER NOT NULL,
    inventory_turnover_ratio NUMERIC(6, 2),
    customer_satisfaction_score NUMERIC(5, 2),
    national_industrial_growth_benchmark_pct NUMERIC(6, 2),
    source_type VARCHAR(100) DEFAULT 'Executive Cross-Agent Aggregation Engine'
);

CREATE TABLE IF NOT EXISTS ceo.strategic_initiatives (
    initiative_id VARCHAR(30) PRIMARY KEY,
    pillar VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    lead_agent VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    target_completion VARCHAR(50) NOT NULL,
    budget_usd NUMERIC(12, 2) NOT NULL,
    kpi_metric VARCHAR(255) NOT NULL
);

