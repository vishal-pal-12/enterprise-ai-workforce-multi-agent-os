import pytest
import json
from app.agent.tools.sales_tools import (
    get_top_selling_products,
    identify_regional_sales_trends
)

def test_get_top_selling_products():
    res_str = get_top_selling_products.invoke({"limit": 5, "year": 2024})
    res = json.loads(res_str)
    assert res["status"] == "SUCCESS"
    assert res["reporting_year"] == 2024
    assert len(res["top_products"]) == 5
    # Verify ranking descending
    assert res["top_products"][0]["total_revenue_usd"] >= res["top_products"][-1]["total_revenue_usd"]

def test_identify_regional_sales_trends():
    res_str = identify_regional_sales_trends.invoke({})
    res = json.loads(res_str)
    assert res["status"] == "SUCCESS"
    assert len(res["regional_trends"]) > 0
    # Check that declining regions are properly flagged (e.g. Tamil Nadu or UP)
    declining = [r for r in res["regional_trends"] if r["trajectory"] == "DECLINING"]
    assert len(declining) > 0
    for d in declining:
        assert d["sales_2024_usd"] < d["sales_2023_usd"]

