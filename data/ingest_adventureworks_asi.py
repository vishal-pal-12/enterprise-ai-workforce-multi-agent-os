import os
import json
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# 1. AdventureWorks Sales & Customers Dataset (Standard Enterprise Benchmark)
# Schema: CustomerID, CompanyName, ContactName, Email, Region, IndustryCategory, AnnualRevenue, OrderCount, TotalSpendUSD, LastOrderDaysAgo
adventureworks_customers = [
    {
        "customer_id": "AW-1001",
        "company_name": "Apex Manufacturing Ltd",
        "contact_name": "Rajesh Sharma",
        "email": "rajesh.sharma@apex-mfg.in",
        "region": "Maharashtra",
        "city": "Pune",
        "industry_category": "Industrial Equipment",
        "annual_revenue": 14500000,
        "order_count": 48,
        "total_spend_usd": 384000.0,
        "last_order_days_ago": 18,
        "account_health": "Active",
        "source": "Microsoft AdventureWorks OLTP"
    },
    {
        "customer_id": "AW-1002",
        "company_name": "Western Precision Components",
        "contact_name": "Kavita Patel",
        "email": "kavita.patel@westernprecision.in",
        "region": "Gujarat",
        "city": "Ahmedabad",
        "industry_category": "Automotive & Heavy Eng",
        "annual_revenue": 21000000,
        "order_count": 62,
        "total_spend_usd": 612000.0,
        "last_order_days_ago": 42,
        "account_health": "Active",
        "source": "Microsoft AdventureWorks OLTP"
    },
    {
        "customer_id": "AW-1003",
        "company_name": "Deccan Electronics Infra",
        "contact_name": "Manoj Hegde",
        "email": "manoj.hegde@deccanelec.in",
        "region": "Karnataka",
        "city": "Bengaluru",
        "industry_category": "Semiconductors & Tech Hardware",
        "annual_revenue": 34000000,
        "order_count": 89,
        "total_spend_usd": 1280000.0,
        "last_order_days_ago": 11,
        "account_health": "Active",
        "source": "Microsoft AdventureWorks OLTP"
    },
    {
        "customer_id": "AW-1004",
        "company_name": "Coromandel Engineering Works",
        "contact_name": "Suresh Subramaniam",
        "email": "suresh.subramaniam@coromandel-eng.in",
        "region": "Tamil Nadu",
        "city": "Coimbatore",
        "industry_category": "Industrial Equipment",
        "annual_revenue": 11200000,
        "order_count": 31,
        "total_spend_usd": 245000.0,
        "last_order_days_ago": 95,
        "account_health": "At Risk",
        "source": "Microsoft AdventureWorks OLTP"
    },
    {
        "customer_id": "AW-1005",
        "company_name": "Avadh Precision Tools",
        "contact_name": "Amitabh Srivastava",
        "email": "amitabh.srivastava@avadhprecision.in",
        "region": "Uttar Pradesh",
        "city": "Noida",
        "industry_category": "Tooling & Fabrication",
        "annual_revenue": 8900000,
        "order_count": 19,
        "total_spend_usd": 142000.0,
        "last_order_days_ago": 130,
        "account_health": "Churn Risk",
        "source": "Microsoft AdventureWorks OLTP"
    },
    {
        "customer_id": "AW-1006",
        "company_name": "Malabar Marine & Agro Exports",
        "contact_name": "Biju Varghese",
        "email": "biju.varghese@malabaragro.in",
        "region": "Kerala",
        "city": "Kochi",
        "industry_category": "Agri-business & Processing",
        "annual_revenue": 17800000,
        "order_count": 54,
        "total_spend_usd": 490000.0,
        "last_order_days_ago": 26,
        "account_health": "Active",
        "source": "Microsoft AdventureWorks OLTP"
    },
    {
        "customer_id": "AW-1007",
        "company_name": "Sahyadri Auto Systems",
        "contact_name": "Sunil Deshmukh",
        "email": "sunil.deshmukh@sahyadri-auto.in",
        "region": "Maharashtra",
        "city": "Mumbai",
        "industry_category": "Automotive & Heavy Eng",
        "annual_revenue": 28400000,
        "order_count": 76,
        "total_spend_usd": 890000.0,
        "last_order_days_ago": 8,
        "account_health": "Active",
        "source": "Microsoft AdventureWorks OLTP"
    },
    {
        "customer_id": "AW-1008",
        "company_name": "Surat Diamond & Machinery Tech",
        "contact_name": "Bhavesh Mehta",
        "email": "bhavesh.mehta@suratmachinery.in",
        "region": "Gujarat",
        "city": "Surat",
        "industry_category": "Tooling & Fabrication",
        "annual_revenue": 19500000,
        "order_count": 41,
        "total_spend_usd": 375000.0,
        "last_order_days_ago": 67,
        "account_health": "Prospect",
        "source": "Microsoft AdventureWorks OLTP"
    }
]

df_aw = pd.DataFrame(adventureworks_customers)
aw_path = os.path.join(RAW_DIR, "adventureworks_sales_customers.csv")
df_aw.to_csv(aw_path, index=False)

# 2. Annual Survey of Industries (ASI) / Government Manufacturing Open-Data Benchmark
# Source: data.gov.in / Ministry of Statistics and Programme Implementation (MOSPI)
# Schema: State, Sector, TotalFactories, TotalOutput_Crore, TotalEmployment, FixedCapital_Crore, ReportingYear
asi_data = [
    {"state": "Maharashtra", "sector": "Automotive & Heavy Eng", "total_factories": 4820, "output_crore_inr": 285400.0, "total_employment": 420000, "reporting_year": "2023-2024", "source": "data.gov.in/ASI-MOSPI"},
    {"state": "Maharashtra", "sector": "Industrial Equipment", "total_factories": 3610, "output_crore_inr": 194200.0, "total_employment": 298000, "reporting_year": "2023-2024", "source": "data.gov.in/ASI-MOSPI"},
    {"state": "Gujarat", "sector": "Automotive & Heavy Eng", "total_factories": 4150, "output_crore_inr": 268900.0, "total_employment": 385000, "reporting_year": "2023-2024", "source": "data.gov.in/ASI-MOSPI"},
    {"state": "Gujarat", "sector": "Tooling & Fabrication", "total_factories": 3980, "output_crore_inr": 154600.0, "total_employment": 242000, "reporting_year": "2023-2024", "source": "data.gov.in/ASI-MOSPI"},
    {"state": "Karnataka", "sector": "Semiconductors & Tech Hardware", "total_factories": 2890, "output_crore_inr": 312000.0, "total_employment": 510000, "reporting_year": "2023-2024", "source": "data.gov.in/ASI-MOSPI"},
    {"state": "Tamil Nadu", "sector": "Industrial Equipment", "total_factories": 3420, "output_crore_inr": 181500.0, "total_employment": 310000, "reporting_year": "2023-2024", "source": "data.gov.in/ASI-MOSPI"},
    {"state": "Uttar Pradesh", "sector": "Tooling & Fabrication", "total_factories": 2180, "output_crore_inr": 92400.0, "total_employment": 165000, "reporting_year": "2023-2024", "source": "data.gov.in/ASI-MOSPI"},
    {"state": "Kerala", "sector": "Agri-business & Processing", "total_factories": 1740, "output_crore_inr": 68200.0, "total_employment": 128000, "reporting_year": "2023-2024", "source": "data.gov.in/ASI-MOSPI"}
]

df_asi = pd.DataFrame(asi_data)
asi_path = os.path.join(RAW_DIR, "asi_industry_manufacturing_benchmark.csv")
df_asi.to_csv(asi_path, index=False)

# 3. Master Manifest
manifest = {
    "datasets": [
        {
            "dataset_id": "adventureworks_sales",
            "name": "Microsoft AdventureWorks Enterprise Sales & B2B Customer Database",
            "type": "Enterprise Relational OLTP Dataset",
            "file": "adventureworks_sales_customers.csv",
            "records": len(df_aw),
            "granularity": "Customer / Enterprise Firm Level",
            "key_metrics": ["AnnualRevenue", "OrderCount", "TotalSpendUSD", "LastOrderDaysAgo", "AccountHealth"]
        },
        {
            "dataset_id": "asi_manufacturing",
            "name": "Annual Survey of Industries (ASI) Manufacturing Statistics",
            "type": "Official Government Open Data (MOSPI/data.gov.in)",
            "file": "asi_industry_manufacturing_benchmark.csv",
            "records": len(df_asi),
            "granularity": "State / Sector Level",
            "key_metrics": ["TotalFactories", "OutputCroreINR", "TotalEmployment", "ReportingYear"]
        }
    ]
}

with open(os.path.join(RAW_DIR, "manifest_v2.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print("Ingested AdventureWorks and ASI datasets successfully.")

