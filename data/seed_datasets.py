import os
import json
import pandas as pd
from datetime import datetime, timezone

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# 1. Dataset A: Udyam MSME Registered Units (Aggregate Regional Distribution by State & District)
# Source: data.gov.in / udyam registration portal
# Real-world official schema characteristics: State, District, Enterprise_Type (Micro/Small/Medium), Total_Registered, Reporting_Year
msme_data = [
    {"state": "Maharashtra", "district": "Mumbai", "enterprise_type": "Micro", "registered_units": 142500, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Maharashtra", "district": "Mumbai", "enterprise_type": "Small", "registered_units": 38200, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Maharashtra", "district": "Mumbai", "enterprise_type": "Medium", "registered_units": 4120, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Maharashtra", "district": "Pune", "enterprise_type": "Micro", "registered_units": 118400, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Maharashtra", "district": "Pune", "enterprise_type": "Small", "registered_units": 29600, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Maharashtra", "district": "Pune", "enterprise_type": "Medium", "registered_units": 3540, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Gujarat", "district": "Ahmedabad", "enterprise_type": "Micro", "registered_units": 125300, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Gujarat", "district": "Ahmedabad", "enterprise_type": "Small", "registered_units": 34100, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Gujarat", "district": "Ahmedabad", "enterprise_type": "Medium", "registered_units": 3890, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Gujarat", "district": "Surat", "enterprise_type": "Micro", "registered_units": 98200, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Gujarat", "district": "Surat", "enterprise_type": "Small", "registered_units": 24500, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Gujarat", "district": "Surat", "enterprise_type": "Medium", "registered_units": 2180, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Tamil Nadu", "district": "Chennai", "enterprise_type": "Micro", "registered_units": 112000, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Tamil Nadu", "district": "Chennai", "enterprise_type": "Small", "registered_units": 28400, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Tamil Nadu", "district": "Chennai", "enterprise_type": "Medium", "registered_units": 3100, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Tamil Nadu", "district": "Coimbatore", "enterprise_type": "Micro", "registered_units": 87400, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Tamil Nadu", "district": "Coimbatore", "enterprise_type": "Small", "registered_units": 22100, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Tamil Nadu", "district": "Coimbatore", "enterprise_type": "Medium", "registered_units": 2450, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Karnataka", "district": "Bengaluru Urban", "enterprise_type": "Micro", "registered_units": 138900, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Karnataka", "district": "Bengaluru Urban", "enterprise_type": "Small", "registered_units": 36500, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Karnataka", "district": "Bengaluru Urban", "enterprise_type": "Medium", "registered_units": 4410, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Uttar Pradesh", "district": "Gautam Buddha Nagar", "enterprise_type": "Micro", "registered_units": 76500, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Uttar Pradesh", "district": "Gautam Buddha Nagar", "enterprise_type": "Small", "registered_units": 19400, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Uttar Pradesh", "district": "Gautam Buddha Nagar", "enterprise_type": "Medium", "registered_units": 1820, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Kerala", "district": "Ernakulam", "enterprise_type": "Micro", "registered_units": 54200, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Kerala", "district": "Ernakulam", "enterprise_type": "Small", "registered_units": 11300, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
    {"state": "Kerala", "district": "Ernakulam", "enterprise_type": "Medium", "registered_units": 980, "reporting_year": "2023-2024", "source": "data.gov.in/resource/udyam"},
]

df_msme = pd.DataFrame(msme_data)
msme_path = os.path.join(RAW_DIR, "udyam_msme_registered_units.csv")
df_msme.to_csv(msme_path, index=False)

# 2. Dataset B: Principal Commodity-Wise Export
# Source: data.gov.in / Department of Commerce
# Real-world schema: Commodity, Sector, Export_Value_USD_Million, Reporting_Year, Growth_Rate_Pct
export_data = [
    {"commodity": "Engineering Goods", "sector": "Manufacturing", "export_value_usd_million": 109320.5, "growth_rate_pct": 8.4, "reporting_year": "2023-2024", "currency": "USD_MILLION", "source": "data.gov.in/catalog/principal-commodity-wise-export"},
    {"commodity": "Petroleum Products", "sector": "Energy & Petrochemicals", "export_value_usd_million": 86510.2, "growth_rate_pct": -4.2, "reporting_year": "2023-2024", "currency": "USD_MILLION", "source": "data.gov.in/catalog/principal-commodity-wise-export"},
    {"commodity": "Gems and Jewellery", "sector": "Luxury & Handicrafts", "export_value_usd_million": 32800.0, "growth_rate_pct": -9.8, "reporting_year": "2023-2024", "currency": "USD_MILLION", "source": "data.gov.in/catalog/principal-commodity-wise-export"},
    {"commodity": "Drugs and Pharmaceuticals", "sector": "Healthcare & Biotech", "export_value_usd_million": 27850.4, "growth_rate_pct": 9.6, "reporting_year": "2023-2024", "currency": "USD_MILLION", "source": "data.gov.in/catalog/principal-commodity-wise-export"},
    {"commodity": "Electronic Goods", "sector": "Electronics & Hardware", "export_value_usd_million": 29120.8, "growth_rate_pct": 23.6, "reporting_year": "2023-2024", "currency": "USD_MILLION", "source": "data.gov.in/catalog/principal-commodity-wise-export"},
    {"commodity": "Organic and Inorganic Chemicals", "sector": "Chemicals", "export_value_usd_million": 28430.1, "growth_rate_pct": -3.1, "reporting_year": "2023-2024", "currency": "USD_MILLION", "source": "data.gov.in/catalog/principal-commodity-wise-export"},
    {"commodity": "Readymade Garments of all Textiles", "sector": "Textiles & Apparel", "export_value_usd_million": 14500.6, "growth_rate_pct": -10.2, "reporting_year": "2023-2024", "currency": "USD_MILLION", "source": "data.gov.in/catalog/principal-commodity-wise-export"},
    {"commodity": "Agricultural Products & Marine", "sector": "Agri-business", "export_value_usd_million": 31200.0, "growth_rate_pct": 4.1, "reporting_year": "2023-2024", "currency": "USD_MILLION", "source": "data.gov.in/catalog/principal-commodity-wise-export"},
    {"commodity": "Software & IT-Enabled Services", "sector": "Information Technology", "export_value_usd_million": 195000.0, "growth_rate_pct": 12.8, "reporting_year": "2023-2024", "currency": "USD_MILLION", "source": "data.gov.in/catalog/principal-commodity-wise-export"},
]

df_export = pd.DataFrame(export_data)
export_path = os.path.join(RAW_DIR, "principal_commodity_wise_export.csv")
df_export.to_csv(export_path, index=False)

# Manifest of Data Sources
manifest = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "sources": [
        {
            "dataset_id": "udyam_msme",
            "name": "List of MSME Registered Units under Udyam",
            "official_url": "https://www.data.gov.in/resource/list-msme-registered-units-under-udyam",
            "catalog_url": "https://kerala.data.gov.in/catalog/udyam-registration-msme-registration",
            "local_file": "udyam_msme_registered_units.csv",
            "reporting_period": "2023-2024",
            "granularity": "State / District / Enterprise Type",
            "units": "Registered Units Count",
            "is_synthetic_seed": True,
            "license": "Government Open Data License - India (GODL)",
            "limitations": "Aggregated registration count; does not infer company revenue, profitability, or direct buyer intent."
        },
        {
            "dataset_id": "commodity_export",
            "name": "Principal Commodity-Wise Export Statistics",
            "official_url": "https://data.gov.in/catalog/principal-commodity-wise-export",
            "local_file": "principal_commodity_wise_export.csv",
            "reporting_period": "2023-2024",
            "granularity": "National / Commodity / Sector",
            "units": "USD Million",
            "is_synthetic_seed": True,
            "license": "Government Open Data License - India (GODL)",
            "limitations": "National level aggregates. Cannot be directly joined at district/firm level without sector mapping."
        }
    ]
}

with open(os.path.join(RAW_DIR, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print("Seed datasets and manifest successfully generated in", RAW_DIR)
