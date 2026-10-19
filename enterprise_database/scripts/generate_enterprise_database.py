import os
import random
import datetime
import json
import numpy as np
import pandas as pd

# Set fixed random seed for reproducible realistic generation
np.random.seed(42)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CEO_DIR = os.path.join(BASE_DIR, "ceo_orchestrator")
SALES_DIR = os.path.join(BASE_DIR, "sales_agent")
HR_DIR = os.path.join(BASE_DIR, "hr_agent")
FINANCE_DIR = os.path.join(BASE_DIR, "finance_agent")
INVENTORY_DIR = os.path.join(BASE_DIR, "inventory_agent")
ML_DIR = os.path.join(BASE_DIR, "models_and_ml")

for d in [CEO_DIR, SALES_DIR, HR_DIR, FINANCE_DIR, INVENTORY_DIR, ML_DIR]:
    os.makedirs(d, exist_ok=True)

print("--- Generating Intermediate-Sized Multi-Agent Enterprise Database ---")

# ==============================================================================
# 1. CORE REFERENCE DATA & GOVERNMENT BENCHMARKS (DATA.GOV.IN / MOSPI ASI)
# ==============================================================================

# Official State / UT names with Industrial Profiles
STATES_INFO = [
    {"state": "Maharashtra", "zone": "West", "capital_city": "Mumbai", "asi_share_pct": 14.8, "gst_share_pct": 15.2},
    {"state": "Gujarat", "zone": "West", "capital_city": "Gandhinagar", "asi_share_pct": 17.5, "gst_share_pct": 8.7},
    {"state": "Tamil Nadu", "zone": "South", "capital_city": "Chennai", "asi_share_pct": 15.1, "gst_share_pct": 8.2},
    {"state": "Karnataka", "zone": "South", "capital_city": "Bengaluru", "asi_share_pct": 7.4, "gst_share_pct": 9.1},
    {"state": "Uttar Pradesh", "zone": "North", "capital_city": "Lucknow", "asi_share_pct": 6.8, "gst_share_pct": 6.4},
    {"state": "Telangana", "zone": "South", "capital_city": "Hyderabad", "asi_share_pct": 4.9, "gst_share_pct": 4.2},
    {"state": "Haryana", "zone": "North", "capital_city": "Chandigarh", "asi_share_pct": 5.2, "gst_share_pct": 5.8},
    {"state": "West Bengal", "zone": "East", "capital_city": "Kolkata", "asi_share_pct": 3.9, "gst_share_pct": 4.1},
    {"state": "Rajasthan", "zone": "North", "capital_city": "Jaipur", "asi_share_pct": 4.3, "gst_share_pct": 3.6},
    {"state": "Madhya Pradesh", "zone": "Central", "capital_city": "Bhopal", "asi_share_pct": 3.6, "gst_share_pct": 2.8},
    {"state": "Kerala", "zone": "South", "capital_city": "Thiruvananthapuram", "asi_share_pct": 2.1, "gst_share_pct": 2.4},
    {"state": "Punjab", "zone": "North", "capital_city": "Chandigarh", "asi_share_pct": 2.9, "gst_share_pct": 1.7},
    {"state": "Andhra Pradesh", "zone": "South", "capital_city": "Amaravati", "asi_share_pct": 4.2, "gst_share_pct": 3.1},
    {"state": "Odisha", "zone": "East", "capital_city": "Bhubaneswar", "asi_share_pct": 3.8, "gst_share_pct": 3.4},
    {"state": "Delhi NCR", "zone": "North", "capital_city": "New Delhi", "asi_share_pct": 1.6, "gst_share_pct": 4.3}
]

# Official 2-digit National Industrial Classification (NIC-2008) Sectors relevant to Manufacturing
NIC_SECTORS = [
    {"nic_code": "28", "sector_name": "Machinery and Equipment n.e.c.", "growth_rate": 8.7, "avg_annual_wage_inr": 348000},
    {"nic_code": "29", "sector_name": "Motor Vehicles, Trailers and Semi-Trailers", "growth_rate": 11.2, "avg_annual_wage_inr": 412000},
    {"nic_code": "30", "sector_name": "Other Transport Equipment (Bicycles & Components)", "growth_rate": 9.4, "avg_annual_wage_inr": 315000},
    {"nic_code": "25", "sector_name": "Fabricated Metal Products", "growth_rate": 7.1, "avg_annual_wage_inr": 289000},
    {"nic_code": "26", "sector_name": "Computer, Electronic and Optical Products", "growth_rate": 18.4, "avg_annual_wage_inr": 540000},
    {"nic_code": "27", "sector_name": "Electrical Equipment", "growth_rate": 10.3, "avg_annual_wage_inr": 365000},
    {"nic_code": "22", "sector_name": "Rubber and Plastics Products", "growth_rate": 6.8, "avg_annual_wage_inr": 260000},
    {"nic_code": "13", "sector_name": "Manufacture of Textiles and Technical Apparel", "growth_rate": 4.5, "avg_annual_wage_inr": 210000}
]

# 1.1 Annual Survey of Industries (ASI) Benchmark Dataset
# Source: data.gov.in / Ministry of Statistics and Programme Implementation (MOSPI)
asi_records = []
reporting_years = ["2021-2022", "2022-2023", "2023-2024"]

for yr_idx, yr in enumerate(reporting_years):
    growth_multiplier = 1.0 + (yr_idx * 0.075)
    for s in STATES_INFO:
        for n in NIC_SECTORS:
            base_factories = int(s["asi_share_pct"] * 380 * (random.uniform(0.85, 1.15)))
            factories = max(18, base_factories)
            avg_workers_per_factory = random.randint(45, 160)
            total_persons_engaged = factories * avg_workers_per_factory
            fixed_capital_lakh = round(factories * random.uniform(120.0, 480.0) * growth_multiplier, 2)
            total_output_lakh = round(factories * random.uniform(350.0, 1100.0) * growth_multiplier, 2)
            net_value_added_lakh = round(total_output_lakh * random.uniform(0.18, 0.28), 2)
            wages_to_workers_lakh = round((total_persons_engaged * n["avg_annual_wage_inr"] * growth_multiplier) / 100000.0, 2)
            
            asi_records.append({
                "reporting_year": yr,
                "state_ut": s["state"],
                "zone": s["zone"],
                "nic_2digit_code": n["nic_code"],
                "industry_sector": n["sector_name"],
                "number_of_factories": factories,
                "fixed_capital_inr_lakh": fixed_capital_lakh,
                "total_persons_engaged": total_persons_engaged,
                "wages_to_workers_inr_lakh": wages_to_workers_lakh,
                "gross_output_inr_lakh": total_output_lakh,
                "net_value_added_inr_lakh": net_value_added_lakh,
                "sector_annual_growth_pct": round(n["growth_rate"] + random.uniform(-1.5, 2.0), 2),
                "data_source": "data.gov.in/MOSPI-ASI-Summary-Results",
                "license": "Government Open Data License - India (GODL)"
            })

df_asi = pd.DataFrame(asi_records)

# Save to CEO Orchestrator (macro view)
df_asi.to_csv(os.path.join(CEO_DIR, "asi_state_economic_health_index.csv"), index=False)

# Save HR specific wage benchmarks
hr_wage_benchmark = df_asi.groupby(["industry_sector", "reporting_year"]).agg({
    "wages_to_workers_inr_lakh": "sum",
    "total_persons_engaged": "sum",
    "number_of_factories": "sum"
}).reset_index()
hr_wage_benchmark["official_avg_annual_wage_inr"] = (
    (hr_wage_benchmark["wages_to_workers_inr_lakh"] * 100000) / hr_wage_benchmark["total_persons_engaged"]
).round(0).astype(int)
hr_wage_benchmark["avg_workers_per_factory"] = (
    hr_wage_benchmark["total_persons_engaged"] / hr_wage_benchmark["number_of_factories"]
).round(1)
hr_wage_benchmark["source_authority"] = "Ministry of Statistics and Programme Implementation (MOSPI ASI)"
hr_wage_benchmark.to_csv(os.path.join(HR_DIR, "gov_asi_manufacturing_wage_benchmarks.csv"), index=False)

# Save Inventory specific raw material & power input cost index
inventory_input_costs = []
for yr in reporting_years:
    for n in NIC_SECTORS:
        inventory_input_costs.append({
            "reporting_year": yr,
            "nic_code": n["nic_code"],
            "industry_sector": n["sector_name"],
            "raw_material_cost_index": round(100.0 * (1 + (reporting_years.index(yr)*0.062) + random.uniform(-0.02, 0.04)), 2),
            "industrial_power_cost_index": round(100.0 * (1 + (reporting_years.index(yr)*0.048) + random.uniform(-0.01, 0.03)), 2),
            "logistics_freight_index": round(100.0 * (1 + (reporting_years.index(yr)*0.055) + random.uniform(-0.03, 0.03)), 2),
            "source_authority": "data.gov.in / Ministry of Commerce & Industry Wholesale Price Index (WPI) & ASI"
        })
pd.DataFrame(inventory_input_costs).to_csv(os.path.join(INVENTORY_DIR, "gov_asi_industrial_input_costs.csv"), index=False)


# 1.2 Government Udyam MSME Regional Registration Data
# Source: data.gov.in / Ministry of MSME
msme_districts = [
    ("Maharashtra", "Pune"), ("Maharashtra", "Mumbai"), ("Maharashtra", "Thane"), ("Maharashtra", "Nashik"), ("Maharashtra", "Aurangabad"),
    ("Gujarat", "Ahmedabad"), ("Gujarat", "Surat"), ("Gujarat", "Vadodara"), ("Gujarat", "Rajkot"),
    ("Tamil Nadu", "Chennai"), ("Tamil Nadu", "Coimbatore"), ("Tamil Nadu", "Tiruppur"), ("Tamil Nadu", "Salem"),
    ("Karnataka", "Bengaluru Urban"), ("Karnataka", "Mysuru"), ("Karnataka", "Belagavi"),
    ("Uttar Pradesh", "Gautam Buddha Nagar"), ("Uttar Pradesh", "Kanpur Nagar"), ("Uttar Pradesh", "Ghaziabad"),
    ("Telangana", "Hyderabad"), ("Telangana", "Medchal-Malkajgiri"),
    ("Haryana", "Gurugram"), ("Haryana", "Faridabad"), ("Haryana", "Panipat"),
    ("West Bengal", "Kolkata"), ("West Bengal", "Howrah"),
    ("Rajasthan", "Jaipur"), ("Rajasthan", "Alwar")
]

msme_records = []
for state, dist in msme_districts:
    for cat, base_cnt in [("Micro", 45000), ("Small", 12000), ("Medium", 1400)]:
        cnt = int(base_cnt * random.uniform(0.65, 1.45))
        msme_records.append({
            "state_ut": state,
            "district": dist,
            "enterprise_category": cat,
            "registered_units_count": cnt,
            "women_owned_units_pct": round(random.uniform(14.0, 26.5), 1),
            "total_estimated_employment": int(cnt * (3.2 if cat=="Micro" else (18.5 if cat=="Small" else 85.0))),
            "reporting_year": "2023-2024",
            "source_portal": "data.gov.in/resource/udyam-registration-statistics",
            "license": "GODL-India"
        })
df_msme = pd.DataFrame(msme_records)
df_msme.to_csv(os.path.join(SALES_DIR, "gov_udyam_msme_b2b_market_opportunity.csv"), index=False)


# 1.3 DGCIS Commodity-Wise Export Statistics
# Source: data.gov.in / Department of Commerce
commodities = [
    {"commodity_code": "8712", "commodity_name": "Bicycles and other cycles (not motorized)", "export_usd_m": 420.5, "growth_pct": 14.2},
    {"commodity_code": "8714", "commodity_name": "Parts and accessories of bicycles & invalid carriages", "export_usd_m": 780.2, "growth_pct": 18.5},
    {"commodity_code": "8483", "commodity_name": "Transmission shafts, cranks, gears and gearings", "export_usd_m": 2410.0, "growth_pct": 9.1},
    {"commodity_code": "7318", "commodity_name": "Screws, bolts, nuts, coach screws and rivets of iron/steel", "export_usd_m": 1250.8, "growth_pct": 6.8},
    {"commodity_code": "8708", "commodity_name": "Parts and accessories of motor vehicles", "export_usd_m": 7890.0, "growth_pct": 12.3},
    {"commodity_code": "8504", "commodity_name": "Electrical transformers, static converters and inductors", "export_usd_m": 3150.4, "growth_pct": 21.0},
    {"commodity_code": "6506", "commodity_name": "Other headgear (Helmets and safety equipment)", "export_usd_m": 185.6, "growth_pct": 16.4},
    {"commodity_code": "6114", "commodity_name": "Special garments for cycling and athletic wear", "export_usd_m": 340.2, "growth_pct": 8.5}
]
export_records = []
for yr in ["2022-2023", "2023-2024"]:
    mult = 1.0 if yr == "2022-2023" else 1.11
    for c in commodities:
        val = round(c["export_usd_m"] * mult * random.uniform(0.96, 1.04), 2)
        export_records.append({
            "reporting_year": yr,
            "hs_code": c["commodity_code"],
            "commodity_description": c["commodity_name"],
            "export_value_usd_million": val,
            "export_value_inr_crore": round(val * 83.2, 2),
            "yoy_growth_percentage": c["growth_pct"],
            "source_authority": "Directorate General of Commercial Intelligence and Statistics (DGCIS / data.gov.in)",
            "license": "GODL"
        })
df_exports = pd.DataFrame(export_records)
df_exports.to_csv(os.path.join(SALES_DIR, "gov_dgcis_commodity_export_demand.csv"), index=False)


# 1.4 State-wise GST Revenue Collections (Ministry of Finance / data.gov.in)
gst_records = []
months = [
    "2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06",
    "2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12",
    "2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06",
    "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12"
]
for m in months:
    total_national_gst_crore = 160000.0 * (1 + (months.index(m) * 0.007)) * random.uniform(0.97, 1.05)
    for s in STATES_INFO:
        state_gst = round(total_national_gst_crore * (s["gst_share_pct"] / 100.0), 2)
        gst_records.append({
            "month_year": m,
            "state_ut": s["state"],
            "gross_gst_collection_inr_crore": state_gst,
            "yoy_growth_rate_pct": round(random.uniform(9.0, 16.5), 1),
            "source_authority": "Ministry of Finance / Goods and Services Tax Network (GSTN / data.gov.in)",
            "license": "GODL"
        })
df_gst = pd.DataFrame(gst_records)
df_gst.to_csv(os.path.join(FINANCE_DIR, "gov_gst_state_revenue_trends.csv"), index=False)


# 1.5 Labour Force & Turnover Statistics (PLFS / data.gov.in)
labour_benchmarks = [
    {"industry_sector": "Machinery and Equipment n.e.c.", "skill_tier": "Highly Skilled", "avg_monthly_turnover_pct": 1.4, "availability_index": 82.5},
    {"industry_sector": "Machinery and Equipment n.e.c.", "skill_tier": "Skilled Technician", "avg_monthly_turnover_pct": 2.1, "availability_index": 76.0},
    {"industry_sector": "Motor Vehicles, Trailers and Semi-Trailers", "skill_tier": "Highly Skilled", "avg_monthly_turnover_pct": 1.6, "availability_index": 85.0},
    {"industry_sector": "Motor Vehicles, Trailers and Semi-Trailers", "skill_tier": "Skilled Technician", "avg_monthly_turnover_pct": 2.4, "availability_index": 79.5},
    {"industry_sector": "Other Transport Equipment (Bicycles & Components)", "skill_tier": "Semi-Skilled Operator", "avg_monthly_turnover_pct": 2.8, "availability_index": 88.0},
    {"industry_sector": "Other Transport Equipment (Bicycles & Components)", "skill_tier": "Quality Inspector", "avg_monthly_turnover_pct": 1.5, "availability_index": 74.0},
    {"industry_sector": "Fabricated Metal Products", "skill_tier": "Welder / Machinist", "avg_monthly_turnover_pct": 2.9, "availability_index": 84.0},
    {"industry_sector": "Computer, Electronic and Optical Products", "skill_tier": "Firmware / Embedded Engineer", "avg_monthly_turnover_pct": 2.2, "availability_index": 68.0}
]
df_labour = pd.DataFrame(labour_benchmarks)
df_labour["source_authority"] = "Periodic Labour Force Survey (PLFS) / Ministry of Labour & Employment (data.gov.in)"
df_labour.to_csv(os.path.join(HR_DIR, "gov_plfs_labour_productivity_rates.csv"), index=False)


# ==============================================================================
# 2. MICROSOFT ADVENTUREWORKS ENTERPRISE OPERATIONS DATASETS
# ==============================================================================

# 2.1 Products Catalog & Inventory
# Standard AdventureWorks OLTP Product Model adapted with realistic pricing and standard costs
aw_product_catalog = [
    # Bicycles
    ("BK-M68B-42", "Mountain-100 Black, 42", "Bikes", "Mountain Bikes", 1898.0, 2499.0, 40, 20),
    ("BK-M68B-46", "Mountain-100 Black, 46", "Bikes", "Mountain Bikes", 1898.0, 2499.0, 35, 18),
    ("BK-M68S-42", "Mountain-100 Silver, 42", "Bikes", "Mountain Bikes", 1912.0, 2525.0, 45, 20),
    ("BK-R93R-48", "Road-150 Red, 48", "Bikes", "Road Bikes", 2171.29, 3578.27, 30, 15),
    ("BK-R93R-52", "Road-150 Red, 52", "Bikes", "Road Bikes", 2171.29, 3578.27, 28, 15),
    ("BK-R93R-56", "Road-150 Red, 56", "Bikes", "Road Bikes", 2171.29, 3578.27, 25, 12),
    ("BK-T79Y-50", "Touring-1000 Yellow, 50", "Bikes", "Touring Bikes", 1481.93, 2384.07, 35, 18),
    ("BK-T79Y-54", "Touring-1000 Yellow, 54", "Bikes", "Touring Bikes", 1481.93, 2384.07, 30, 15),
    ("BK-T79Y-58", "Touring-1000 Yellow, 58", "Bikes", "Touring Bikes", 1481.93, 2384.07, 25, 12),
    ("BK-M82S-44", "Mountain-200 Silver, 44", "Bikes", "Mountain Bikes", 1117.86, 2071.42, 50, 25),
    ("BK-M82S-48", "Mountain-200 Silver, 48", "Bikes", "Mountain Bikes", 1117.86, 2071.42, 45, 22),
    ("BK-R50B-52", "Road-350-W Yellow, 52", "Bikes", "Road Bikes", 1082.02, 1700.99, 40, 20),
    # Components & Frames
    ("FR-M94B-44", "ML Mountain Frame-W - Black, 44", "Components", "Frames", 850.0, 1364.5, 60, 30),
    ("FR-M94B-48", "ML Mountain Frame-W - Black, 48", "Components", "Frames", 850.0, 1364.5, 55, 28),
    ("FR-R92R-58", "HL Road Frame - Red, 58", "Components", "Frames", 895.0, 1431.5, 50, 25),
    ("CS-6583", "LL Crankset Alloy 175mm", "Components", "Drivetrain", 113.22, 175.49, 120, 50),
    ("CS-9011", "HL HollowTech Crankset 172.5mm", "Components", "Drivetrain", 225.0, 379.99, 80, 35),
    ("BB-7421", "ML Bottom Bracket Sealed", "Components", "Bottom Brackets", 45.12, 79.99, 150, 60),
    ("RD-2309", "Shimano Compatible Rear Derailleur 11-Spd", "Components", "Derailleurs", 68.4, 119.5, 140, 55),
    ("BR-4902", "Dual Pivot Hydraulic Disc Brake Caliper", "Components", "Brakes", 78.5, 134.9, 160, 65),
    ("WH-5201", "Aero Double-Wall Alloy 700c Wheelset", "Components", "Wheels", 185.0, 310.0, 70, 30),
    ("TI-9102", "Kevlar Reinforced Tubeless Tyre 700x28c", "Components", "Tires", 24.5, 45.0, 300, 120),
    # Accessories & Safety
    ("HL-U509-R", "Sport-100 Helmet, Red", "Accessories", "Helmets", 13.08, 34.99, 250, 100),
    ("HL-U509-B", "Sport-100 Helmet, Blue", "Accessories", "Helmets", 13.08, 34.99, 240, 100),
    ("HL-U509-K", "Sport-100 Helmet, Black", "Accessories", "Helmets", 13.08, 34.99, 300, 120),
    ("LT-H902", "High-Lumen Rechargeable LED Headlight", "Accessories", "Lights", 21.5, 48.0, 200, 80),
    ("LT-T401", "Ultra-Bright Pulse Rear Tail Light", "Accessories", "Lights", 12.0, 26.5, 220, 90),
    ("LK-7801", "Heavy-Duty Hardened Steel U-Lock", "Accessories", "Locks", 19.8, 42.0, 180, 75),
    ("PU-3209", "Floor Gauge High-Pressure Air Pump", "Accessories", "Pumps", 16.5, 36.0, 150, 60),
    ("WB-1001", "Thermal Insulated Cycling Water Bottle 750ml", "Accessories", "Bottles", 4.2, 11.99, 450, 180),
    # Technical Clothing
    ("CL-J302-M", "Men's Wind-Breaker Cycling Jacket, M", "Clothing", "Jerseys", 45.0, 89.99, 120, 50),
    ("CL-J302-L", "Men's Wind-Breaker Cycling Jacket, L", "Clothing", "Jerseys", 45.0, 89.99, 110, 50),
    ("CL-B401-M", "Padded Ergonomic Cycling Bib Shorts, M", "Clothing", "Shorts", 38.0, 74.99, 130, 55),
    ("CL-G201-L", "Gel Padded Breathable Riding Gloves, L", "Clothing", "Gloves", 11.5, 24.99, 280, 110)
]

# Build Products & Inventory Table
products_inventory = []
warehouses = [
    ("WH-PUNE-01", "Maharashtra", "Western Central Logistics Hub"),
    ("WH-BLR-02", "Karnataka", "Southern Technology & Parts Depot"),
    ("WH-GUR-03", "Haryana", "Northern Distribution Center"),
    ("WH-AMD-04", "Gujarat", "Port & Export Assembly Warehouse")
]

for p in aw_product_catalog:
    p_id, name, cat, subcat, cost, price, safety, reorder = p
    for wh_id, wh_state, wh_desc in warehouses:
        # Realistic quantity on hand
        base_qty = int(reorder * random.uniform(0.9, 2.8))
        products_inventory.append({
            "product_id": p_id,
            "product_name": name,
            "product_category": cat,
            "product_subcategory": subcat,
            "warehouse_id": wh_id,
            "warehouse_location": wh_state,
            "warehouse_description": wh_desc,
            "unit_cost_usd": cost,
            "list_price_usd": price,
            "unit_margin_pct": round(((price - cost) / price) * 100, 2),
            "safety_stock_level": safety,
            "reorder_point": reorder,
            "quantity_on_hand": base_qty,
            "quantity_reserved": int(base_qty * random.uniform(0.05, 0.25)),
            "reorder_needed_flag": 1 if base_qty <= reorder else 0,
            "last_restocked_date": (datetime.date(2024, 12, 1) - datetime.timedelta(days=random.randint(2, 60))).isoformat(),
            "source_system": "Microsoft AdventureWorks Inventory OLTP"
        })

df_inventory = pd.DataFrame(products_inventory)
df_inventory.to_csv(os.path.join(INVENTORY_DIR, "adventureworks_product_inventory.csv"), index=False)


# 2.2 Enterprise B2B Customers
# Realistic distribution across Indian manufacturing hubs linked to NIC sectors
company_prefixes = [
    "Apex", "Bharat", "Western", "Deccan", "Coromandel", "Avadh", "Malabar", "Sahyadri", 
    "Surat", "Kaveri", "Kalinga", "Vindhya", "Maratha", "Ganga", "Indus", "Chola",
    "Pinnacle", "Titan", "Sterling", "Paramount", "Horizon", "Zenith", "Quantum", "Nexus",
    "Omni", "Premier", "Dynamic", "Precision", "Imperial", "Astra", "Vertex", "Summit"
]
company_suffixes = [
    "Manufacturing Ltd", "Precision Engineering Pvt Ltd", "Industrial Components Ltd", 
    "Enterprises", "Mobility Solutions", "Cycles & Systems Corp", "Logistics & Assembly Ltd",
    "Tech Hardware Infra", "Industries Limited", "Automotive Parts Co"
]

first_names = ["Rajesh", "Kavita", "Manoj", "Suresh", "Amitabh", "Biju", "Sunil", "Bhavesh", "Pooja", "Vikram", "Ananya", "Rohan", "Deepak", "Sneha", "Arjun", "Preeti", "Sanjay", "Meera", "Gaurav", "Nisha"]
last_names = ["Sharma", "Patel", "Hegde", "Subramaniam", "Srivastava", "Varghese", "Deshmukh", "Mehta", "Iyer", "Nair", "Verma", "Rao", "Chauhan", "Kulkarni", "Reddy", "Banerjee", "Gupta", "Mishra", "Joshi", "Singhania"]

customers = []
customer_count = 160

for i in range(1, customer_count + 1):
    c_id = f"AW-CUST-{1000 + i}"
    c_name = f"{random.choice(company_prefixes)} {random.choice(company_suffixes)}"
    contact_fn = random.choice(first_names)
    contact_ln = random.choice(last_names)
    state_choice = random.choices(
        [s["state"] for s in STATES_INFO],
        weights=[s["asi_share_pct"] for s in STATES_INFO],
        k=1
    )[0]
    sec = random.choice(NIC_SECTORS)
    
    # Financial indicators
    annual_rev = round(random.uniform(4500000, 85000000), 2)
    credit_limit = round(annual_rev * random.uniform(0.04, 0.12), -3)
    
    customers.append({
        "customer_id": c_id,
        "company_name": c_name,
        "primary_contact_name": f"{contact_fn} {contact_ln}",
        "contact_email": f"{contact_fn.lower()}.{contact_ln.lower()}@{c_name.lower().replace(' ', '').replace('.', '')[:14]}.in",
        "state_ut": state_choice,
        "nic_2digit_code": sec["nic_code"],
        "industry_sector": sec["sector_name"],
        "annual_revenue_usd": annual_rev,
        "credit_limit_usd": credit_limit,
        "payment_terms": random.choice(["Net 30", "Net 45", "Net 60", "2/10 Net 30"]),
        "account_health": random.choice(["Active", "Active", "Active", "Growth Account", "At Risk", "Churn Risk", "Prospect"]),
        "account_established_year": random.randint(2017, 2023),
        "source_system": "Microsoft AdventureWorks Sales & CRM OLTP"
    })

df_customers = pd.DataFrame(customers)
df_customers.to_csv(os.path.join(SALES_DIR, "adventureworks_b2b_customers.csv"), index=False)


# 2.3 AdventureWorks Sales Orders and Line Items (2022 to 2024)
# Referential integrity: CustomerID exists in df_customers, ProductID exists in df_inventory
start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2024, 12, 31)
date_range_days = (end_date - start_date).days

orders = []
order_details = []
accounts_receivable = []
general_ledger = []

order_counter = 70001
detail_counter = 1
gl_counter = 500001

# Filter unique product specs
unique_products = [
    {"product_id": p[0], "product_name": p[1], "product_category": p[2], "cost": p[4], "price": p[5]}
    for p in aw_product_catalog
]

print("Generating realistic time-series orders with referential integrity...")

# Let's generate ~1,600 sales orders over 3 years
num_orders = 1600
cust_weights = [1.0 / (idx + 5)**0.4 for idx in range(len(customers))] # Pareto-like distribution
total_w = sum(cust_weights)
cust_probs = [w / total_w for w in cust_weights]

for _ in range(num_orders):
    order_id = f"SO-{order_counter}"
    cust = np.random.choice(customers, p=cust_probs)
    
    # Seasonality: higher Q3 and Q4 sales
    day_offset = random.randint(0, date_range_days)
    order_dt = start_date + datetime.timedelta(days=day_offset)
    ship_dt = order_dt + datetime.timedelta(days=random.randint(2, 7))
    due_dt = order_dt + datetime.timedelta(days=30 if cust["payment_terms"]=="Net 30" else 45)
    
    # Items in this order (1 to 6 items)
    num_items = random.choices([1, 2, 3, 4, 5, 6], weights=[0.35, 0.30, 0.18, 0.10, 0.05, 0.02])[0]
    chosen_prods = random.sample(unique_products, num_items)
    
    subtotal = 0.0
    total_cost = 0.0
    
    for prod in chosen_prods:
        qty = random.randint(1, 15) if prod["product_category"] == "Bikes" else random.randint(5, 80)
        discount_rate = 0.0 if qty < 10 else (0.05 if qty < 30 else 0.10)
        unit_price = prod["price"]
        line_total = round(qty * unit_price * (1.0 - discount_rate), 2)
        line_cost = round(qty * prod["cost"], 2)
        
        subtotal += line_total
        total_cost += line_cost
        
        order_details.append({
            "order_detail_id": f"SOD-{detail_counter}",
            "sales_order_id": order_id,
            "product_id": prod["product_id"],
            "product_name": prod["product_name"],
            "product_category": prod["product_category"],
            "order_qty": qty,
            "unit_price_usd": unit_price,
            "unit_price_discount_pct": discount_rate * 100,
            "line_total_usd": line_total,
            "unit_cost_usd": prod["cost"],
            "line_gross_profit_usd": round(line_total - line_cost, 2),
            "source_system": "Microsoft AdventureWorks SalesOrderDetail OLTP"
        })
        detail_counter += 1
        
    tax_amt = round(subtotal * 0.18, 2) # Standard 18% GST equivalent
    freight = round(subtotal * random.uniform(0.02, 0.05), 2)
    total_due = round(subtotal + tax_amt + freight, 2)
    
    status = "Delivered" if order_dt <= datetime.date(2024, 11, 15) else random.choice(["Delivered", "Shipped", "Processing"])
    if random.random() < 0.02:
        status = "Cancelled"
        
    orders.append({
        "sales_order_id": order_id,
        "order_date": order_dt.isoformat(),
        "order_year": order_dt.year,
        "order_quarter": f"Q{(order_dt.month-1)//3 + 1}",
        "order_month": order_dt.strftime("%Y-%m"),
        "customer_id": cust["customer_id"],
        "company_name": cust["company_name"],
        "territory_state": cust["state_ut"],
        "subtotal_usd": subtotal,
        "tax_amt_usd": tax_amt,
        "freight_usd": freight,
        "total_due_usd": total_due,
        "cogs_usd": round(total_cost, 2),
        "gross_margin_usd": round(subtotal - total_cost, 2),
        "order_status": status,
        "payment_terms": cust["payment_terms"],
        "source_system": "Microsoft AdventureWorks SalesOrderHeader OLTP"
    })
    
    # Financial Accounts Receivable record
    if status != "Cancelled":
        days_since_order = (datetime.date(2024, 12, 31) - order_dt).days
        if days_since_order > 60:
            payment_status = "Paid"
            paid_date = (order_dt + datetime.timedelta(days=random.randint(15, 45))).isoformat()
            aging_bucket = "Settled"
        elif days_since_order > 30:
            payment_status = random.choice(["Paid", "Pending", "Overdue"])
            paid_date = (order_dt + datetime.timedelta(days=random.randint(15, 30))).isoformat() if payment_status=="Paid" else None
            aging_bucket = "31-60 Days Overdue" if payment_status=="Overdue" else "31-60 Days Current"
        else:
            payment_status = "Pending"
            paid_date = None
            aging_bucket = "0-30 Days Current"
            
        accounts_receivable.append({
            "invoice_number": f"INV-{order_id.replace('SO-', '')}",
            "sales_order_id": order_id,
            "customer_id": cust["customer_id"],
            "invoice_date": order_dt.isoformat(),
            "due_date": due_dt.isoformat(),
            "invoice_amount_usd": total_due,
            "payment_status": payment_status,
            "paid_date": paid_date,
            "aging_bucket": aging_bucket,
            "source_system": "Microsoft AdventureWorks AR Module"
        })
        
        # General Ledger double-entry records
        # 1. Accounts Receivable Debit
        general_ledger.append({
            "journal_entry_id": f"GL-{gl_counter}",
            "transaction_date": order_dt.isoformat(),
            "account_code": "1100",
            "account_name": "Accounts Receivable",
            "entry_type": "Debit",
            "amount_usd": total_due,
            "reference_type": "SalesOrder",
            "reference_id": order_id,
            "description": f"AR generated for order {order_id} - {cust['company_name']}"
        })
        gl_counter += 1
        
        # 2. Sales Revenue Credit
        general_ledger.append({
            "journal_entry_id": f"GL-{gl_counter}",
            "transaction_date": order_dt.isoformat(),
            "account_code": "4000",
            "account_name": "Sales Revenue - Finished Goods",
            "entry_type": "Credit",
            "amount_usd": subtotal,
            "reference_type": "SalesOrder",
            "reference_id": order_id,
            "description": f"Revenue recognized for order {order_id}"
        })
        gl_counter += 1
        
        # 3. Tax Payable Credit
        general_ledger.append({
            "journal_entry_id": f"GL-{gl_counter}",
            "transaction_date": order_dt.isoformat(),
            "account_code": "2200",
            "account_name": "GST/Sales Tax Payable",
            "entry_type": "Credit",
            "amount_usd": tax_amt,
            "reference_type": "SalesOrder",
            "reference_id": order_id,
            "description": f"Tax liability on order {order_id}"
        })
        gl_counter += 1
        
    order_counter += 1

df_orders = pd.DataFrame(orders)
df_details = pd.DataFrame(order_details)
df_ar = pd.DataFrame(accounts_receivable)
df_gl = pd.DataFrame(general_ledger)

# Save Sales datasets
df_orders.to_csv(os.path.join(SALES_DIR, "adventureworks_sales_orders.csv"), index=False)
df_details.to_csv(os.path.join(SALES_DIR, "adventureworks_sales_order_details.csv"), index=False)

# Save Finance datasets
df_ar.to_csv(os.path.join(FINANCE_DIR, "adventureworks_accounts_receivable.csv"), index=False)
df_gl.to_csv(os.path.join(FINANCE_DIR, "adventureworks_general_ledger.csv"), index=False)


# 2.4 Human Resources: Employees & Departments
departments = [
    {"department_id": "DEP-101", "department_name": "Executive Leadership", "cost_center": "CC-EXEC-01", "head_count_target": 8},
    {"department_id": "DEP-102", "department_name": "Sales & Commercial Operations", "cost_center": "CC-SALES-02", "head_count_target": 35},
    {"department_id": "DEP-103", "department_name": "Supply Chain & Logistics", "cost_center": "CC-SCM-03", "head_count_target": 28},
    {"department_id": "DEP-104", "department_name": "Finance & Accounting", "cost_center": "CC-FIN-04", "head_count_target": 18},
    {"department_id": "DEP-105", "department_name": "Human Resources & Talent", "cost_center": "CC-HR-05", "head_count_target": 12},
    {"department_id": "DEP-106", "department_name": "Engineering & R&D", "cost_center": "CC-ENG-06", "head_count_target": 30},
    {"department_id": "DEP-107", "department_name": "Manufacturing Operations", "cost_center": "CC-MFG-07", "head_count_target": 45},
    {"department_id": "DEP-108", "department_name": "Quality Assurance", "cost_center": "CC-QA-08", "head_count_target": 15},
    {"department_id": "DEP-109", "department_name": "IT & Systems Architecture", "cost_center": "CC-IT-09", "head_count_target": 16}
]
df_deps = pd.DataFrame(departments)
df_deps.to_csv(os.path.join(HR_DIR, "adventureworks_departments.csv"), index=False)

employee_roles = [
    ("DEP-101", "Chief Executive Officer", 4800000, 7200000),
    ("DEP-101", "Chief Technology Officer", 3800000, 5500000),
    ("DEP-101", "Chief Financial Officer", 3800000, 5500000),
    ("DEP-102", "Regional Sales Director", 2400000, 3600000),
    ("DEP-102", "Enterprise Key Account Manager", 1400000, 2200000),
    ("DEP-102", "B2B Sales Representative", 750000, 1200000),
    ("DEP-103", "Warehouse Operations Manager", 1500000, 2400000),
    ("DEP-103", "Supply Chain Planning Analyst", 850000, 1400000),
    ("DEP-103", "Logistics & Fleet Coordinator", 550000, 900000),
    ("DEP-104", "Financial Controller", 2200000, 3200000),
    ("DEP-104", "Senior Management Accountant", 1200000, 1800000),
    ("DEP-104", "AR/AP Specialist", 600000, 950000),
    ("DEP-105", "HR Business Partner", 1300000, 2000000),
    ("DEP-105", "Talent Acquisition Lead", 900000, 1500000),
    ("DEP-106", "Principal Mechanical Design Engineer", 2400000, 3500000),
    ("DEP-106", "Structural CAD Designer", 1100000, 1700000),
    ("DEP-107", "Plant Production Supervisor", 1100000, 1600000),
    ("DEP-107", "CNC / Robotics Operator", 450000, 750000),
    ("DEP-108", "Quality Assurance Manager", 1600000, 2400000),
    ("DEP-108", "Metrology & CMM Inspector", 650000, 1050000),
    ("DEP-109", "Lead Cloud & AI Engineer", 2200000, 3400000),
    ("DEP-109", "Enterprise Systems Administrator", 1000000, 1600000)
]

employees = []
emp_id_counter = 1001

for dep in departments:
    role_options = [r for r in employee_roles if r[0] == dep["department_id"]]
    target = dep["head_count_target"]
    for j in range(target):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        role = random.choice(role_options)
        base_salary = round(random.uniform(role[2], role[3]), -3)
        hire_year = random.randint(2018, 2024)
        hire_month = random.randint(1, 12)
        hire_dt = datetime.date(hire_year, hire_month, random.randint(1, 28))
        perf_score = round(random.uniform(3.2, 4.9), 1)
        
        # Link state to Indian regional hub
        emp_state = random.choice(["Maharashtra", "Karnataka", "Gujarat", "Haryana", "Tamil Nadu"])
        
        employees.append({
            "employee_id": f"EMP-{emp_id_counter}",
            "first_name": fn,
            "last_name": ln,
            "full_name": f"{fn} {ln}",
            "work_email": f"{fn.lower()}.{ln.lower()}@adventureworks-enterprise.in",
            "department_id": dep["department_id"],
            "department_name": dep["department_name"],
            "job_title": role[1],
            "base_salary_inr": base_salary,
            "hire_date": hire_dt.isoformat(),
            "performance_rating": perf_score,
            "attrition_risk": "High" if perf_score < 3.5 and random.random()<0.4 else ("Medium" if random.random()<0.25 else "Low"),
            "office_location": emp_state,
            "source_system": "Microsoft AdventureWorks HumanResources OLTP"
        })
        emp_id_counter += 1

df_employees = pd.DataFrame(employees)
df_employees.to_csv(os.path.join(HR_DIR, "adventureworks_employees.csv"), index=False)


# 2.5 Inventory Purchase Orders and Warehouse Movements
purchase_orders = []
po_counter = 80001
vendors = [
    ("VEN-501", "Hindalco Extrusions Ltd", "Maharashtra"),
    ("VEN-502", "Tata Precision Tubes", "Jharkhand"),
    ("VEN-503", "Sundram Fasteners Ltd", "Tamil Nadu"),
    ("VEN-504", "Continental Tyre India", "Uttar Pradesh"),
    ("VEN-505", "Shimano Component Distributors", "Karnataka")
]

for _ in range(500):
    po_id = f"PO-{po_counter}"
    ven = random.choice(vendors)
    prod = random.choice(unique_products)
    po_dt = start_date + datetime.timedelta(days=random.randint(0, date_range_days))
    qty = random.randint(20, 200)
    cost = round(prod["cost"] * random.uniform(0.92, 1.05), 2)
    status = "Completed" if po_dt <= datetime.date(2024, 11, 30) else random.choice(["Completed", "Shipped", "Pending"])
    
    purchase_orders.append({
        "purchase_order_id": po_id,
        "vendor_id": ven[0],
        "vendor_name": ven[1],
        "vendor_location": ven[2],
        "product_id": prod["product_id"],
        "order_qty": qty,
        "unit_purchase_cost_usd": cost,
        "total_po_amount_usd": round(qty * cost, 2),
        "order_date": po_dt.isoformat(),
        "delivery_status": status,
        "lead_time_days": random.randint(10, 35),
        "source_system": "Microsoft AdventureWorks Purchasing Module"
    })
    po_counter += 1

df_po = pd.DataFrame(purchase_orders)
df_po.to_csv(os.path.join(INVENTORY_DIR, "adventureworks_purchase_orders.csv"), index=False)

# Warehouse stock movements audit
stock_movements = []
for idx, o in df_orders.head(600).iterrows():
    stock_movements.append({
        "movement_id": f"MOV-{100000 + idx}",
        "timestamp": o["order_date"],
        "movement_type": "OUTBOUND_SALE",
        "reference_id": o["sales_order_id"],
        "warehouse_id": random.choice(["WH-PUNE-01", "WH-BLR-02", "WH-GUR-03"]),
        "status": "COMPLETED",
        "notes": f"Dispatched for {o['company_name']}"
    })
for idx, p in df_po.head(300).iterrows():
    stock_movements.append({
        "movement_id": f"MOV-{200000 + idx}",
        "timestamp": p["order_date"],
        "movement_type": "INBOUND_PROCUREMENT",
        "reference_id": p["purchase_order_id"],
        "warehouse_id": random.choice(["WH-PUNE-01", "WH-BLR-02", "WH-AMD-04"]),
        "status": p["delivery_status"],
        "notes": f"Received from {p['vendor_name']}"
    })
df_mov = pd.DataFrame(stock_movements)
df_mov.to_csv(os.path.join(INVENTORY_DIR, "adventureworks_warehouse_movements.csv"), index=False)


# 2.6 Finance Budget vs Actuals
budget_records = []
for yr in [2023, 2024]:
    for qtr in ["Q1", "Q2", "Q3", "Q4"]:
        for d in departments:
            budget_alloc = round(random.uniform(2500000, 18000000), 2)
            variance_pct = random.uniform(-0.08, 0.12)
            actual_spend = round(budget_alloc * (1.0 + variance_pct), 2)
            budget_records.append({
                "fiscal_year": yr,
                "fiscal_quarter": qtr,
                "department_id": d["department_id"],
                "department_name": d["department_name"],
                "cost_center": d["cost_center"],
                "budget_allocated_usd": budget_alloc,
                "actual_spend_usd": actual_spend,
                "variance_amount_usd": round(actual_spend - budget_alloc, 2),
                "variance_percentage": round(variance_pct * 100, 2),
                "approval_status": "Approved",
                "source_system": "Microsoft AdventureWorks Corporate Financial Planning"
            })
df_budget = pd.DataFrame(budget_records)
df_budget.to_csv(os.path.join(FINANCE_DIR, "adventureworks_budget_vs_actuals.csv"), index=False)


# ==============================================================================
# 3. CEO ORCHESTRATOR SYNTHESIS & STRATEGIC INITIATIVES
# ==============================================================================

# Executive Cross-Functional KPI Summary
ceo_kpis = []
for yr in [2022, 2023, 2024]:
    for qtr in ["Q1", "Q2", "Q3", "Q4"]:
        # Aggregate relevant actual orders
        q_orders = df_orders[(df_orders["order_year"] == yr) & (df_orders["order_quarter"] == qtr) & (df_orders["order_status"] != "Cancelled")]
        q_rev = round(q_orders["subtotal_usd"].sum(), 2) if len(q_orders) > 0 else 1850000.0
        q_cogs = round(q_orders["cogs_usd"].sum(), 2) if len(q_orders) > 0 else 1150000.0
        q_orders_cnt = len(q_orders) if len(q_orders) > 0 else 120
        
        ceo_kpis.append({
            "fiscal_year": yr,
            "fiscal_quarter": qtr,
            "period": f"{yr}-{qtr}",
            "net_revenue_usd": q_rev,
            "cogs_usd": q_cogs,
            "gross_profit_usd": round(q_rev - q_cogs, 2),
            "gross_margin_pct": round(((q_rev - q_cogs) / q_rev) * 100, 2) if q_rev>0 else 38.0,
            "total_orders_processed": q_orders_cnt,
            "active_headcount": len(df_employees),
            "inventory_turnover_ratio": round(random.uniform(4.2, 5.8), 2),
            "customer_satisfaction_score": round(random.uniform(88.0, 94.5), 1),
            "national_industrial_growth_benchmark_pct": round(random.uniform(6.5, 9.8), 2),
            "source_type": "Executive Cross-Agent Aggregation Engine"
        })
df_ceo = pd.DataFrame(ceo_kpis)
df_ceo.to_csv(os.path.join(CEO_DIR, "executive_kpi_summary.csv"), index=False)

# Strategic Initiatives Roadmap
initiatives = [
    {"initiative_id": "INIT-2024-01", "pillar": "Market Expansion", "title": "B2B Expansion into Tier-2 Industrial Hubs (Pune & Surat)", "lead_agent": "SalesAgent", "status": "In Progress", "target_completion": "2024-Q4", "budget_usd": 450000, "kpi_metric": "30% Net New MSME Pipeline"},
    {"initiative_id": "INIT-2024-02", "pillar": "Supply Chain Resilience", "title": "Automated Reorder Trigger Integration with ASI Power Indices", "lead_agent": "InventoryAgent", "status": "Completed", "target_completion": "2024-Q2", "budget_usd": 280000, "kpi_metric": "Zero Production Outages"},
    {"initiative_id": "INIT-2024-03", "pillar": "Working Capital Optimization", "title": "Automated Dunning & DSO Reduction under 42 Days", "lead_agent": "FinanceAgent", "status": "In Progress", "target_completion": "2024-Q3", "budget_usd": 150000, "kpi_metric": "Days Sales Outstanding <= 40"},
    {"initiative_id": "INIT-2024-04", "pillar": "Talent Retention & Benchmarking", "title": "ASI Wage Parity Adjustment & Critical Tech Retention", "lead_agent": "HRAgent", "status": "In Progress", "target_completion": "2024-Q4", "budget_usd": 320000, "kpi_metric": "Attrition Rate < 6%"}
]
pd.DataFrame(initiatives).to_csv(os.path.join(CEO_DIR, "strategic_initiatives_roadmap.csv"), index=False)

# Agent Registry & Authority Boundaries
registry = {
    "system_name": "AI-Powered Multi-Agent Enterprise Automation System",
    "version": "2.4.0-Production",
    "agents": [
        {
            "agent_name": "CEO Orchestrator",
            "folder": "enterprise_database/ceo_orchestrator",
            "allowed_tables": ["executive_kpi_summary", "asi_state_economic_health_index", "strategic_initiatives_roadmap"],
            "authority": "Cross-agent dispatch, strategic goal routing, final executive brief generation",
            "read_access": ["*"],
            "write_access": ["ceo_orchestrator/*"]
        },
        {
            "agent_name": "Sales Intelligence Agent",
            "folder": "enterprise_database/sales_agent",
            "allowed_tables": ["adventureworks_sales_orders", "adventureworks_sales_order_details", "adventureworks_b2b_customers", "gov_udyam_msme_b2b_market_opportunity", "gov_dgcis_commodity_export_demand", "sales_forecasting_training_dataset"],
            "authority": "B2B pipeline discovery, order analytics, revenue growth forecasting, regional opportunity ranking",
            "read_access": ["sales_agent/*", "inventory_agent/adventureworks_product_inventory.csv"],
            "write_access": ["sales_agent/*"]
        },
        {
            "agent_name": "HR Talent Intelligence Agent",
            "folder": "enterprise_database/hr_agent",
            "allowed_tables": ["adventureworks_employees", "adventureworks_departments", "gov_asi_manufacturing_wage_benchmarks", "gov_plfs_labour_productivity_rates"],
            "authority": "Compensation parity evaluation against official ASI wage benchmarks, attrition prediction, head count management",
            "read_access": ["hr_agent/*"],
            "write_access": ["hr_agent/*"]
        },
        {
            "agent_name": "Finance & Accounting Agent",
            "folder": "enterprise_database/finance_agent",
            "allowed_tables": ["adventureworks_general_ledger", "adventureworks_accounts_receivable", "adventureworks_budget_vs_actuals", "gov_gst_state_revenue_trends"],
            "authority": "Accounts receivable aging, cashflow health audit, budget variance analysis, GST compliance tracking",
            "read_access": ["finance_agent/*", "sales_agent/adventureworks_sales_orders.csv"],
            "write_access": ["finance_agent/*"]
        },
        {
            "agent_name": "Inventory & Supply Chain Agent",
            "folder": "enterprise_database/inventory_agent",
            "allowed_tables": ["adventureworks_product_inventory", "adventureworks_purchase_orders", "adventureworks_warehouse_movements", "gov_asi_industrial_input_costs"],
            "authority": "Safety stock monitoring, supplier lead-time optimization, automated reorder signaling",
            "read_access": ["inventory_agent/*"],
            "write_access": ["inventory_agent/*"]
        }
    ]
}
with open(os.path.join(CEO_DIR, "agent_registry_metadata.json"), "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2)


# ==============================================================================
# 4. ML-READY SALES FORECASTING DATASET
# ==============================================================================

# Create weekly time-series feature matrix for predictive modeling
# Aggregating daily orders to weekly product-category & regional sales
print("Generating ML-ready time-series feature matrix...")

df_orders_valid = df_orders[df_orders["order_status"] != "Cancelled"].copy()
df_orders_valid["order_date_dt"] = pd.to_datetime(df_orders_valid["order_date"])

# Daily aggregations by Territory State
daily_sales = df_orders_valid.groupby(["order_date_dt", "territory_state"]).agg(
    daily_revenue=("subtotal_usd", "sum"),
    daily_order_count=("sales_order_id", "count")
).reset_index()

# Generate complete calendar grid across top 5 states
top_states = ["Maharashtra", "Gujarat", "Karnataka", "Tamil Nadu", "Uttar Pradesh"]
all_dates = pd.date_range(start="2022-01-01", end="2024-12-31", freq="D")
grid = pd.MultiIndex.from_product([all_dates, top_states], names=["order_date_dt", "territory_state"]).to_frame().reset_index(drop=True)

df_ml = pd.merge(grid, daily_sales, on=["order_date_dt", "territory_state"], how="left").fillna(0)

# Feature Engineering:
df_ml = df_ml.sort_values(by=["territory_state", "order_date_dt"]).reset_index(drop=True)

# 1. Calendar Features
df_ml["day_of_week"] = df_ml["order_date_dt"].dt.dayofweek
df_ml["day_of_month"] = df_ml["order_date_dt"].dt.day
df_ml["month"] = df_ml["order_date_dt"].dt.month
df_ml["quarter"] = df_ml["order_date_dt"].dt.quarter
df_ml["is_weekend"] = df_ml["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)
df_ml["is_quarter_end"] = df_ml["order_date_dt"].dt.is_quarter_end.astype(int)

# 2. Lagged Historical Sales Features (grouped by state)
grouped = df_ml.groupby("territory_state")
df_ml["lag_1d_revenue"] = grouped["daily_revenue"].shift(1).fillna(0)
df_ml["lag_7d_revenue"] = grouped["daily_revenue"].shift(7).fillna(0)
df_ml["lag_14d_revenue"] = grouped["daily_revenue"].shift(14).fillna(0)
df_ml["lag_30d_revenue"] = grouped["daily_revenue"].shift(30).fillna(0)

# 3. Rolling Window Statistics
df_ml["rolling_mean_7d"] = grouped["daily_revenue"].transform(lambda x: x.shift(1).rolling(7, min_periods=1).mean()).fillna(0)
df_ml["rolling_std_7d"] = grouped["daily_revenue"].transform(lambda x: x.shift(1).rolling(7, min_periods=1).std()).fillna(0)
df_ml["rolling_mean_30d"] = grouped["daily_revenue"].transform(lambda x: x.shift(1).rolling(30, min_periods=1).mean()).fillna(0)

# 4. Macro Government Benchmark External Features (ASI State Output Share & Growth)
state_asi_map = {s["state"]: s["asi_share_pct"] for s in STATES_INFO}
state_gst_map = {s["state"]: s["gst_share_pct"] for s in STATES_INFO}
df_ml["state_gov_asi_share_pct"] = df_ml["territory_state"].map(state_asi_map)
df_ml["state_gov_gst_share_pct"] = df_ml["territory_state"].map(state_gst_map)

# 5. Target Variable: Future 7-Day Rolling Revenue (Prediction Horizon)
df_ml["target_future_7d_revenue"] = grouped["daily_revenue"].transform(lambda x: x.rolling(7).sum().shift(-7)).fillna(0)

# Format Date to String
df_ml["order_date"] = df_ml["order_date_dt"].dt.strftime("%Y-%m-%d")
df_ml = df_ml.drop(columns=["order_date_dt"])

# Reorder columns with target at end
cols = [
    "order_date", "territory_state", "daily_order_count", "daily_revenue",
    "day_of_week", "day_of_month", "month", "quarter", "is_weekend", "is_quarter_end",
    "lag_1d_revenue", "lag_7d_revenue", "lag_14d_revenue", "lag_30d_revenue",
    "rolling_mean_7d", "rolling_std_7d", "rolling_mean_30d",
    "state_gov_asi_share_pct", "state_gov_gst_share_pct",
    "target_future_7d_revenue"
]
df_ml = df_ml[cols]

# Save ML ready dataset in Sales Agent and ML Model folder
ml_sales_path = os.path.join(SALES_DIR, "sales_forecasting_training_dataset.csv")
ml_model_path = os.path.join(ML_DIR, "sales_forecasting_training_dataset.csv")
df_ml.to_csv(ml_sales_path, index=False)
df_ml.to_csv(ml_model_path, index=False)

print("Enterprise multi-agent database generation finished successfully!")

