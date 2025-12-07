#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script untuk check nama negara di GeoJSON dan database
Cari nama yang tidak match (seperti Russia, USA, dll)
"""

import requests
import psycopg2
import sys
import io

# Set UTF-8 encoding untuk print
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============ DOWNLOAD GEOJSON ============
print("=" * 90)
print("CHECKING GEOJSON COUNTRY NAMES")
print("=" * 90)

geojson_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
response = requests.get(geojson_url)
geojson_data = response.json()

# Extract nama negara dari GeoJSON
geojson_countries = set()
for feature in geojson_data['features']:
    country_name = feature['properties'].get('name', '')
    if country_name:
        geojson_countries.add(country_name)

print(f"\nTotal negara di GeoJSON: {len(geojson_countries)}")
print("\nContoh negara di GeoJSON:")
for i, country in enumerate(sorted(list(geojson_countries))[:30], 1):
    print(f"  {i:2}. {country}")

# ============ AMBIL NEGARA DARI DATABASE ============
print("\n" + "=" * 90)
print("CHECKING DATABASE COUNTRY NAMES")
print("=" * 90)

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "iqbal",
    "database": "world_happines_v2"
}

conn = psycopg2.connect(**DB_CONFIG)
c = conn.cursor()

c.execute("SELECT country_name FROM country ORDER BY country_name")
db_countries = set([row[0] for row in c.fetchall()])

print(f"\nTotal negara di Database: {len(db_countries)}")
print("\nContoh negara di Database:")
for i, country in enumerate(sorted(list(db_countries))[:30], 1):
    print(f"  {i:2}. {country}")

# ============ CARI MISMATCHES ============
print("\n" + "=" * 90)
print("FINDING MISMATCHES")
print("=" * 90)

matched = db_countries & geojson_countries
not_in_geojson = db_countries - geojson_countries
not_in_db = geojson_countries - db_countries

print(f"\nNegara yang match: {len(matched)}")
print(f"Negara di DB tapi tidak di GeoJSON: {len(not_in_geojson)}")
print(f"Negara di GeoJSON tapi tidak di DB: {len(not_in_db)}")

if not_in_geojson:
    print("\n" + "=" * 90)
    print("NEGARA DI DATABASE TAPI TIDAK DI GEOJSON (Perlu Mapping):")
    print("=" * 90)
    for i, country in enumerate(sorted(list(not_in_geojson)), 1):
        print(f"{i:3}. {country}")
        
        # Cari similar names di GeoJSON
        similar = [g for g in geojson_countries if country.lower() in g.lower() or g.lower() in country.lower()]
        if similar:
            print(f"      => Mungkin cocok dengan: {similar}")

# ============ BUAT MAPPING UNTUK MISMATCHES ============
print("\n" + "=" * 90)
print("SUGGESTED MAPPING (Copy paste ke app_whr.py):")
print("=" * 90)

print("""
# Country name mapping dari database ke GeoJSON
COUNTRY_NAME_MAPPING = {
""")

# Manual mapping untuk yang populer
manual_mapping = {
    'Russia': 'Russia',
    'United States': 'United States of America',
    'Czechia': 'Czech Republic',
    'Czech Republic': 'Czech Republic',
    'Ivory Coast': "Côte d'Ivoire",
    'Congo (Kinshasa)': 'Dem. Rep. Congo',
    'Congo (Brazzaville)': 'Congo',
}

for db_name, geojson_name in manual_mapping.items():
    if db_name in db_countries:
        print(f"    '{db_name}': '{geojson_name}',")

print("}")

c.close()
conn.close()
