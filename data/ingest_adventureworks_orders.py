import os
import json
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# 1. AdventureWorks Sales Orders Table (OLTP schema)
# SalesOrderID, OrderDate, OrderYear, CustomerID, TerritoryRegion, SubTotalUSD, TaxAmtUSD, FreightUSD, TotalDueUSD, OrderStatus
sales_orders = [
    # 2023 Orders
    {"sales_order_id": "SO-71001", "order_date": "2023-01-15", "order_year": 2023, "customer_id": "AW-1001", "territory_region": "Maharashtra", "subtotal_usd": 12400.0, "tax_amt_usd": 992.0, "total_due_usd": 13392.0, "status": "Shipped"},
    {"sales_order_id": "SO-71002", "order_date": "2023-03-22", "order_year": 2023, "customer_id": "AW-1002", "territory_region": "Gujarat", "subtotal_usd": 24500.0, "tax_amt_usd": 1960.0, "total_due_usd": 26460.0, "status": "Shipped"},
    {"sales_order_id": "SO-71003", "order_date": "2023-05-10", "order_year": 2023, "customer_id": "AW-1003", "territory_region": "Karnataka", "subtotal_usd": 48900.0, "tax_amt_usd": 3912.0, "total_due_usd": 52812.0, "status": "Shipped"},
    {"sales_order_id": "SO-71004", "order_date": "2023-07-18", "order_year": 2023, "customer_id": "AW-1004", "territory_region": "Tamil Nadu", "subtotal_usd": 18200.0, "tax_amt_usd": 1456.0, "total_due_usd": 19656.0, "status": "Shipped"},
    {"sales_order_id": "SO-71005", "order_date": "2023-09-04", "order_year": 2023, "customer_id": "AW-1005", "territory_region": "Uttar Pradesh", "subtotal_usd": 14300.0, "tax_amt_usd": 1144.0, "total_due_usd": 15444.0, "status": "Shipped"},
    {"sales_order_id": "SO-71006", "order_date": "2023-11-20", "order_year": 2023, "customer_id": "AW-1007", "territory_region": "Maharashtra", "subtotal_usd": 38600.0, "tax_amt_usd": 3088.0, "total_due_usd": 41688.0, "status": "Shipped"},

    # 2024 Orders (Latest Available Year)
    {"sales_order_id": "SO-72001", "order_date": "2024-02-12", "order_year": 2024, "customer_id": "AW-1001", "territory_region": "Maharashtra", "subtotal_usd": 19800.0, "tax_amt_usd": 1584.0, "total_due_usd": 21384.0, "status": "Shipped"},
    {"sales_order_id": "SO-72002", "order_date": "2024-03-15", "order_year": 2024, "customer_id": "AW-1002", "territory_region": "Gujarat", "subtotal_usd": 31200.0, "tax_amt_usd": 2496.0, "total_due_usd": 33696.0, "status": "Shipped"},
    {"sales_order_id": "SO-72003", "order_date": "2024-04-05", "order_year": 2024, "customer_id": "AW-1003", "territory_region": "Karnataka", "subtotal_usd": 68400.0, "tax_amt_usd": 5472.0, "total_due_usd": 73872.0, "status": "Shipped"},
    {"sales_order_id": "SO-72004", "order_date": "2024-06-11", "order_year": 2024, "customer_id": "AW-1004", "territory_region": "Tamil Nadu", "subtotal_usd": 9200.0, "tax_amt_usd": 736.0, "total_due_usd": 9936.0, "status": "Shipped"}, # Declining region
    {"sales_order_id": "SO-72005", "order_date": "2024-07-28", "order_year": 2024, "customer_id": "AW-1005", "territory_region": "Uttar Pradesh", "subtotal_usd": 6800.0, "tax_amt_usd": 544.0, "total_due_usd": 7344.0, "status": "Shipped"}, # Declining region
    {"sales_order_id": "SO-72006", "order_date": "2024-08-19", "order_year": 2024, "customer_id": "AW-1006", "territory_region": "Kerala", "subtotal_usd": 26400.0, "tax_amt_usd": 2112.0, "total_due_usd": 28512.0, "status": "Shipped"},
    {"sales_order_id": "SO-72007", "order_date": "2024-09-22", "order_year": 2024, "customer_id": "AW-1007", "territory_region": "Maharashtra", "subtotal_usd": 54100.0, "tax_amt_usd": 4328.0, "total_due_usd": 58428.0, "status": "Shipped"},
    {"sales_order_id": "SO-72008", "order_date": "2024-10-04", "order_year": 2024, "customer_id": "AW-1008", "territory_region": "Gujarat", "subtotal_usd": 22100.0, "tax_amt_usd": 1768.0, "total_due_usd": 23868.0, "status": "Shipped"},
]

df_orders = pd.DataFrame(sales_orders)
orders_path = os.path.join(RAW_DIR, "adventureworks_sales_orders.csv")
df_orders.to_csv(orders_path, index=False)

# 2. AdventureWorks Products & Line Item Sales Details Table
# SalesOrderID, ProductID, ProductName, ProductCategory, UnitPriceUSD, OrderQty, LineTotalUSD, UnitCostUSD
order_details = [
    {"sales_order_id": "SO-71001", "product_id": "BK-M68B-42", "product_name": "Mountain-100 Black, 42", "product_category": "Bikes", "unit_price_usd": 2499.0, "order_qty": 4, "line_total_usd": 9996.0, "unit_cost_usd": 1898.0},
    {"sales_order_id": "SO-71001", "product_id": "HL-U509-R", "product_name": "Sport-100 Helmet, Red", "product_category": "Accessories", "unit_price_usd": 34.99, "order_qty": 68, "line_total_usd": 2379.32, "unit_cost_usd": 13.08},
    
    {"sales_order_id": "SO-71002", "product_id": "BK-R93R-48", "product_name": "Road-150 Red, 48", "product_category": "Bikes", "unit_price_usd": 3578.27, "order_qty": 6, "line_total_usd": 21469.62, "unit_cost_usd": 2171.29},
    {"sales_order_id": "SO-71003", "product_id": "FR-M94B-44", "product_name": "ML Mountain Frame-W - Black, 44", "product_category": "Components", "unit_price_usd": 1364.5, "order_qty": 30, "line_total_usd": 40935.0, "unit_cost_usd": 850.0},
    {"sales_order_id": "SO-71004", "product_id": "BK-T79Y-54", "product_name": "Touring-1000 Yellow, 54", "product_category": "Bikes", "unit_price_usd": 2384.07, "order_qty": 7, "line_total_usd": 16688.49, "unit_cost_usd": 1481.93},
    {"sales_order_id": "SO-71005", "product_id": "CS-6583", "product_name": "LL Crankset", "product_category": "Components", "unit_price_usd": 175.49, "order_qty": 70, "line_total_usd": 12284.3, "unit_cost_usd": 113.22},
    {"sales_order_id": "SO-71006", "product_id": "BK-R93R-48", "product_name": "Road-150 Red, 48", "product_category": "Bikes", "unit_price_usd": 3578.27, "order_qty": 10, "line_total_usd": 35782.7, "unit_cost_usd": 2171.29},

    # 2024 Line items
    {"sales_order_id": "SO-72001", "product_id": "BK-M68B-42", "product_name": "Mountain-100 Black, 42", "product_category": "Bikes", "unit_price_usd": 2499.0, "order_qty": 7, "line_total_usd": 17493.0, "unit_cost_usd": 1898.0},
    {"sales_order_id": "SO-72002", "product_id": "BK-R93R-48", "product_name": "Road-150 Red, 48", "product_category": "Bikes", "unit_price_usd": 3578.27, "order_qty": 8, "line_total_usd": 28626.16, "unit_cost_usd": 2171.29},
    {"sales_order_id": "SO-72003", "product_id": "FR-M94B-44", "product_name": "ML Mountain Frame-W - Black, 44", "product_category": "Components", "unit_price_usd": 1364.5, "order_qty": 45, "line_total_usd": 61402.5, "unit_cost_usd": 850.0},
    {"sales_order_id": "SO-72004", "product_id": "HL-U509-R", "product_name": "Sport-100 Helmet, Red", "product_category": "Accessories", "unit_price_usd": 34.99, "order_qty": 200, "line_total_usd": 6998.0, "unit_cost_usd": 13.08},
    {"sales_order_id": "SO-72005", "product_id": "CS-6583", "product_name": "LL Crankset", "product_category": "Components", "unit_price_usd": 175.49, "order_qty": 35, "line_total_usd": 6142.15, "unit_cost_usd": 113.22},
    {"sales_order_id": "SO-72006", "product_id": "BK-T79Y-54", "product_name": "Touring-1000 Yellow, 54", "product_category": "Bikes", "unit_price_usd": 2384.07, "order_qty": 10, "line_total_usd": 23840.7, "unit_cost_usd": 1481.93},
    {"sales_order_id": "SO-72007", "product_id": "BK-R93R-48", "product_name": "Road-150 Red, 48", "product_category": "Bikes", "unit_price_usd": 3578.27, "order_qty": 14, "line_total_usd": 50095.78, "unit_cost_usd": 2171.29},
    {"sales_order_id": "SO-72008", "product_id": "BK-M68B-42", "product_name": "Mountain-100 Black, 42", "product_category": "Bikes", "unit_price_usd": 2499.0, "order_qty": 8, "line_total_usd": 19992.0, "unit_cost_usd": 1898.0},
]

df_details = pd.DataFrame(order_details)
details_path = os.path.join(RAW_DIR, "adventureworks_order_details.csv")
df_details.to_csv(details_path, index=False)

print("Generated AdventureWorks sales orders and order details successfully.")

