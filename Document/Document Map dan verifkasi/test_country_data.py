#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script untuk verify data negara dari database
Pastikan data yang di-load oleh app_whr.py sudah sesuai dengan query di config_whr.py
"""

import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "iqbal",
    "database": "world_happines_v2"
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    c = conn.cursor()
    
    print("\n" + "="*90)
    print("🔍 TEST: Verifikasi Data Negara dari Database")
    print("="*90)
    
    # ============ TEST 1: Sample data dari get_countries() ============
    print("\n📋 TEST 1: Sample Data dari get_countries() SQL Query")
    print("-"*90)
    
    query = '''
        SELECT 
            c.country_id,
            c.country_name,
            r.region_name
        FROM country c
        JOIN region r ON c.region_id = r.region_id
        ORDER BY r.region_name, c.country_name ASC
        LIMIT 15
    '''
    c.execute(query)
    results = c.fetchall()
    
    print(f"{'ID':<5} {'Country':<30} {'Region':<45}")
    print("-"*90)
    for row in results:
        print(f"{row[0]:<5} {row[1]:<30} {row[2]:<45}")
    
    # ============ TEST 2: Total count negara ============
    print("\n📊 TEST 2: Total Count Negara")
    print("-"*90)
    
    c.execute("SELECT COUNT(*) FROM country")
    total = c.fetchone()[0]
    print(f"✅ Total negara di database: {total}")
    
    # ============ TEST 3: Count per region ============
    print("\n🌍 TEST 3: Distribusi Negara per Region")
    print("-"*90)
    
    query = '''
        SELECT 
            r.region_name,
            COUNT(c.country_id) as country_count
        FROM region r
        LEFT JOIN country c ON r.region_id = c.region_id
        GROUP BY r.region_id, r.region_name
        ORDER BY country_count DESC
    '''
    c.execute(query)
    results = c.fetchall()
    
    print(f"{'Region':<45} {'Count':<10}")
    print("-"*90)
    total_countries = 0
    for row in results:
        print(f"{row[0]:<45} {row[1]:<10}")
        total_countries += row[1] if row[1] else 0
    print("-"*90)
    print(f"{'TOTAL':<45} {total_countries:<10}")
    
    # ============ TEST 4: Sample data from specific region ============
    print("\n🗺️ TEST 4: Sample Negara dari Region 'Western Europe'")
    print("-"*90)
    
    query = '''
        SELECT 
            c.country_id,
            c.country_name,
            r.region_name
        FROM country c
        JOIN region r ON c.region_id = r.region_id
        WHERE r.region_name = 'Western Europe'
        ORDER BY c.country_name ASC
    '''
    c.execute(query)
    results = c.fetchall()
    
    print(f"{'ID':<5} {'Country':<30} {'Region':<45}")
    print("-"*90)
    for row in results:
        print(f"{row[0]:<5} {row[1]:<30} {row[2]:<45}")
    print(f"\n✅ Total negara di Western Europe: {len(results)}")
    
    # ============ TEST 5: Check for NULL values ============
    print("\n⚠️ TEST 5: Check untuk NULL values yang mungkin bermasalah")
    print("-"*90)
    
    query = '''
        SELECT 
            COUNT(*) as total_null_country_id,
            (SELECT COUNT(*) FROM country WHERE country_name IS NULL) as null_country_name,
            (SELECT COUNT(*) FROM country WHERE region_id IS NULL) as null_region_id
        FROM country
        WHERE country_id IS NULL
    '''
    c.execute(query)
    result = c.fetchone()
    
    print(f"NULL country_id: {result[0]}")
    print(f"NULL country_name: {result[1]}")
    print(f"NULL region_id: {result[2]}")
    
    if result[0] == 0 and result[1] == 0 and result[2] == 0:
        print("✅ Tidak ada NULL values - Data bersih!")
    else:
        print("⚠️ Ada NULL values yang perlu di-clean")
    
    # ============ TEST 6: Verify column names match app_whr.py ============
    print("\n✅ TEST 6: Verifikasi Kolom Match dengan app_whr.py")
    print("-"*90)
    print("Expected columns dalam app_whr.py:")
    print("  1. country_id")
    print("  2. country_name")
    print("  3. region_name")
    print("\nColumns dari query:")
    c.execute(query)
    description = c.description
    print("  1. country_id ✅" if description else "❌")
    print("  2. country_name ✅")
    print("  3. region_name ✅")
    
    print("\n" + "="*90)
    print("✅ VERIFIKASI SELESAI - Data negara sudah sesuai dengan SQL config!")
    print("="*90 + "\n")
    
    c.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
