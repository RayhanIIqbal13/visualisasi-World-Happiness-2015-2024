# -*- coding: utf-8 -*-
from config_whr import *

print("=== Testing get_happiness_report_all() ===")
data = get_happiness_report_all()
if data:
    print(f"Number of rows: {len(data)}")
    print(f"First row columns count: {len(data[0])}")
    print(f"First row: {data[0]}")
else:
    print("No data returned")

print("\n=== Testing get_economic_indicators_all() ===")
data = get_economic_indicators_all()
if data:
    print(f"Number of rows: {len(data)}")
    print(f"First row columns count: {len(data[0])}")
    print(f"First row: {data[0]}")
else:
    print("No data returned")

print("\n=== Testing get_social_indicators_all() ===")
data = get_social_indicators_all()
if data:
    print(f"Number of rows: {len(data)}")
    print(f"First row columns count: {len(data[0])}")
    print(f"First row: {data[0]}")
else:
    print("No data returned")

print("\n=== Testing get_perception_indicators_all() ===")
data = get_perception_indicators_all()
if data:
    print(f"Number of rows: {len(data)}")
    print(f"First row columns count: {len(data[0])}")
    print(f"First row: {data[0]}")
else:
    print("No data returned")
