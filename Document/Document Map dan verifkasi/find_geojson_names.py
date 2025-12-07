#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Find exact GeoJSON names for mismatched countries
"""

import json
import requests

# List of countries that failed
failed_countries = [
    "Bahrain",
    "Comoros",
    "Congo",
    "Congo (Brazzaville)",
    "Congo (Kinshasa)",
    "Hong Kong",
    "Hong Kong S.A.R. of China",
    "Maldives",
    "Malta",
    "Mauritius",
    "North Cyprus",
    "Palestinian Territories",
    "Singapore",
    "State of Palestine"
]

# Download GeoJSON
print("Downloading GeoJSON...")
geojson_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
response = requests.get(geojson_url)
geojson_data = response.json()

# Get all GeoJSON names
geojson_names = set()
for feature in geojson_data['features']:
    geojson_names.add(feature['properties'].get('name', ''))

print("\nSearching for matching GeoJSON names for failed countries:\n")

for failed in failed_countries:
    print(f"SEARCHING FOR: {failed}")
    
    # Look for exact match
    if failed in geojson_names:
        print(f"  FOUND EXACT: {failed}")
    
    # Look for partial matches
    matches = []
    for geo_name in geojson_names:
        if failed.lower() in geo_name.lower() or geo_name.lower() in failed.lower():
            matches.append(geo_name)
    
    if matches:
        print(f"  PARTIAL MATCHES: {matches}")
    else:
        print(f"  NO MATCHES FOUND")
    
    print()

# Check which countries are in GeoJSON that start with these keywords
print("\n\nAll GeoJSON countries that might match the failed ones:")
print("="*70)

keywords = {
    "congo": [],
    "hong kong": [],
    "palestine": [],
    "bahrain": [],
    "comoros": [],
    "maldives": [],
    "malta": [],
    "mauritius": [],
    "cyprus": [],
    "singapore": []
}

for geo_name in sorted(geojson_names):
    for keyword in keywords.keys():
        if keyword in geo_name.lower():
            keywords[keyword].append(geo_name)

for keyword, names in keywords.items():
    if names:
        print(f"\n{keyword.upper()}:")
        for name in names:
            print(f"  - {name}")
