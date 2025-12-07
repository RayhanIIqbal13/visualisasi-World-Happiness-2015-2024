#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Debug: Check what GeoJSON actually returns for country names
"""

import requests
import json

geojson_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
response = requests.get(geojson_url)
geojson_data = response.json()

print("First 10 GeoJSON features:")
print("="*70)

for i, feature in enumerate(geojson_data['features'][:10]):
    props = feature['properties']
    print(f"\n{i+1}. Name: {props.get('name', 'NO NAME')}")
    print(f"   Keys: {list(props.keys())}")
    print(f"   All props: {props}")

print("\n\nAll unique property keys in GeoJSON:")
all_keys = set()
for feature in geojson_data['features']:
    all_keys.update(feature['properties'].keys())
print(all_keys)

print("\n\nSearching for Russia:")
for feature in geojson_data['features']:
    if 'russia' in str(feature['properties']).lower():
        print(f"Found: {feature['properties']}")
