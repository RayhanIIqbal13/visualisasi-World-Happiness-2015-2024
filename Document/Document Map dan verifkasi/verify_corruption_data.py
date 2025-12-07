#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script untuk verifikasi data corruption perception
Cek apakah Singapore benar-benar paling korupsi atau ada yang lebih tinggi
"""

import pandas as pd
from config_whr import *

print("=" * 80)
print("🔍 VERIFIKASI DATA CORRUPTION PERCEPTION")
print("=" * 80)

# Ambil data perception indicators semua tahun
print("\n📊 Mengambil data perception indicators...")
data = get_perception_indicators_all()

if not data:
    print("❌ Tidak ada data yang ditemukan!")
    exit()

# Convert ke DataFrame untuk analisis lebih mudah
df = pd.DataFrame(data, columns=[
    'perception_id', 'report_id', 'country_name', 'region_name', 
    'year', 'happiness_score', 'generosity', 'perceptions_of_corruption'
])

# Convert column to numeric
df['perceptions_of_corruption'] = pd.to_numeric(df['perceptions_of_corruption'], errors='coerce')

print(f"✅ Total records: {len(df)}")
print(f"✅ Countries: {df['country_name'].nunique()}")
print(f"✅ Years: {sorted(df['year'].unique())}")

# ===== ANALISIS 1: TOP 15 NEGARA DENGAN CORRUPTION PERCEPTION TERTINGGI (PALING KORUPSI) =====
print("\n" + "=" * 80)
print("🔴 TOP 15 NEGARA DENGAN CORRUPTION PERCEPTION TERTINGGI (PALING KORUPSI)")
print("=" * 80)

# Filter data yang punya nilai corruption perception
df_corruption_valid = df[df['perceptions_of_corruption'].notna()]

# Sort dan ambil top 15
top_corruption = df_corruption_valid.nlargest(15, 'perceptions_of_corruption')[
    ['country_name', 'region_name', 'year', 'perceptions_of_corruption', 'generosity']
].reset_index(drop=True)

print("\nRanking (semakin tinggi = semakin korupsi):")
print("-" * 80)
for idx, row in top_corruption.iterrows():
    print(f"{idx+1:2d}. {row['country_name']:30s} | Corruption: {row['perceptions_of_corruption']:6.4f} | Year: {int(row['year'])} | Region: {row['region_name']}")

# ===== ANALISIS 2: FOKUS SINGAPORE =====
print("\n" + "=" * 80)
print("🏙️  ANALISIS SINGAPORE")
print("=" * 80)

sg_data = df[df['country_name'] == 'Singapore'].sort_values('year', ascending=False)
print(f"\nData Singapore ({len(sg_data)} records):")
print("-" * 80)
for idx, row in sg_data.iterrows():
    print(f"Year {int(row['year'])}: Corruption Perception = {row['perceptions_of_corruption']:.4f}, Generosity = {row['generosity']:.4f}")

if len(sg_data) > 0:
    avg_sg_corruption = sg_data['perceptions_of_corruption'].mean()
    print(f"\n📊 Rata-rata Singapore Corruption Perception: {avg_sg_corruption:.4f}")

# ===== ANALISIS 3: PERBANDINGAN DENGAN NEGARA LAIN DI SOUTHEAST ASIA =====
print("\n" + "=" * 80)
print("🌏 PERBANDINGAN DENGAN NEGARA SOUTHEAST ASIA")
print("=" * 80)

sea_countries = ['Singapore', 'Thailand', 'Vietnam', 'Philippines', 'Malaysia', 'Cambodia', 'Indonesia', 'Laos', 'Myanmar']
df_sea = df[df['country_name'].isin(sea_countries)]

sea_comparison = df_sea.groupby('country_name')['perceptions_of_corruption'].agg(['mean', 'min', 'max', 'count']).sort_values('mean', ascending=False)
print("\nRata-rata Corruption Perception di Southeast Asia:")
print("-" * 80)
for country, row in sea_comparison.iterrows():
    print(f"{country:20s} | Rata-rata: {row['mean']:.4f} | Min: {row['min']:.4f} | Max: {row['max']:.4f} | Records: {int(row['count'])}")

# ===== KESIMPULAN =====
print("\n" + "=" * 80)
print("📋 KESIMPULAN")
print("=" * 80)

max_corruption_country = df_corruption_valid.loc[df_corruption_valid['perceptions_of_corruption'].idxmax()]
print(f"\n✓ Negara dengan Corruption Perception TERTINGGI: {max_corruption_country['country_name']}")
print(f"  Nilai: {max_corruption_country['perceptions_of_corruption']:.4f}")
print(f"  Tahun: {int(max_corruption_country['year'])}")
print(f"  Region: {max_corruption_country['region_name']}")

sg_rank = (df_corruption_valid['perceptions_of_corruption'] >= avg_sg_corruption).sum()
print(f"\n✓ Singapore ranking: #{sg_rank} dari {len(df_corruption_valid['country_name'].unique())} negara unik")
print(f"  (Negara dengan corruption perception ≥ Singapore's average: {sg_rank})")

print("\n" + "=" * 80)
