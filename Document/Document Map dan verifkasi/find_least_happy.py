#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script untuk mencari negara yang PALING TIDAK BAHAGIA
(Negara dengan happiness score terendah)
"""

import pandas as pd
from config_whr import *

print("=" * 80)
print("😢 PENCARIAN NEGARA YANG PALING TIDAK BAHAGIA")
print("=" * 80)

# Ambil data happiness report untuk semua tahun
print("\n📊 Mengambil data happiness report...")
data = get_happiness_report_all_aggregated()

if not data:
    print("❌ Tidak ada data yang ditemukan!")
    exit()

# Convert ke DataFrame
df = pd.DataFrame(data, columns=[
    'country_name', 'region_name', 'avg_ranking', 'avg_happiness_score'
])

# Convert to numeric
df['avg_happiness_score'] = pd.to_numeric(df['avg_happiness_score'], errors='coerce')
df['avg_ranking'] = pd.to_numeric(df['avg_ranking'], errors='coerce')

print(f"✅ Total negara: {len(df)}")

# ===== ANALISIS 1: TOP 20 NEGARA PALING TIDAK BAHAGIA (SCORE TERENDAH) =====
print("\n" + "=" * 80)
print("😢 TOP 20 NEGARA DENGAN HAPPINESS SCORE TERENDAH (PALING TIDAK BAHAGIA)")
print("=" * 80)
print("\nData aggregate dari tahun 2015-2024 (rata-rata):\n")

# Sort by happiness score ascending (terendah = paling tidak bahagia)
least_happy = df.nsmallest(20, 'avg_happiness_score')[
    ['country_name', 'region_name', 'avg_ranking', 'avg_happiness_score']
].reset_index(drop=True)

for idx, row in least_happy.iterrows():
    rank_badge = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else "  "
    print(f"{rank_badge} {idx+1:2d}. {row['country_name']:30s} | Score: {row['avg_happiness_score']:.4f} | Ranking: {int(row['avg_ranking']):3d} | {row['region_name']}")

# ===== ANALISIS 2: NEGARA PALING TIDAK BAHAGIA TAHUN 2024 =====
print("\n" + "=" * 80)
print("📊 NEGARA PALING TIDAK BAHAGIA TAHUN 2024")
print("=" * 80)

data_2024 = get_happiness_report_by_year(2024)
if data_2024:
    df_2024 = pd.DataFrame(data_2024, columns=[
        'country_name', 'region_name', 'ranking', 'happiness_score', 'dystopia_residual'
    ])
    df_2024['happiness_score'] = pd.to_numeric(df_2024['happiness_score'], errors='coerce')
    df_2024['ranking'] = pd.to_numeric(df_2024['ranking'], errors='coerce')
    
    least_happy_2024 = df_2024.nsmallest(20, 'happiness_score')[
        ['country_name', 'region_name', 'ranking', 'happiness_score']
    ].reset_index(drop=True)
    
    print("\nTop 20 negara paling tidak bahagia tahun 2024:\n")
    for idx, row in least_happy_2024.iterrows():
        print(f"{idx+1:2d}. {row['country_name']:30s} | Score: {row['happiness_score']:.4f} | Ranking: {int(row['ranking']):3d} | {row['region_name']}")

# ===== ANALISIS 3: PERBANDINGAN REGIONAL =====
print("\n" + "=" * 80)
print("🌍 RATA-RATA HAPPINESS SCORE PER REGION")
print("=" * 80)

regional_avg = df.groupby('region_name').agg({
    'avg_happiness_score': ['mean', 'min', 'max', 'count']
}).round(4)

regional_avg.columns = ['Rata-rata', 'Terendah', 'Tertinggi', 'Jumlah Negara']
regional_avg = regional_avg.sort_values('Rata-rata', ascending=True)

print("\nRegion dengan rata-rata happiness score terendah:\n")
for idx, (region, row) in enumerate(regional_avg.iterrows(), 1):
    print(f"{idx:2d}. {region:40s} | Rata-rata: {row['Rata-rata']:.4f} | Min: {row['Terendah']:.4f} | Max: {row['Tertinggi']:.4f} | {int(row['Jumlah Negara'])} negara")

# ===== ANALISIS 4: TOP 10 NEGARA PALING TIDAK BAHAGIA DI SETIAP REGION =====
print("\n" + "=" * 80)
print("📍 NEGARA PALING TIDAK BAHAGIA DI SETIAP REGION")
print("=" * 80)

for region in df['region_name'].unique():
    df_region = df[df['region_name'] == region]
    least_in_region = df_region.nsmallest(3, 'avg_happiness_score')
    
    print(f"\n🔸 {region}:")
    for idx, row in least_in_region.iterrows():
        print(f"   • {row['country_name']:30s} (Score: {row['avg_happiness_score']:.4f})")

# ===== KESIMPULAN =====
print("\n" + "=" * 80)
print("📋 KESIMPULAN")
print("=" * 80)

most_unhappy = df.loc[df['avg_happiness_score'].idxmin()]
print(f"\n🔴 NEGARA PALING TIDAK BAHAGIA (2015-2024 rata-rata):")
print(f"   Negara: {most_unhappy['country_name']}")
print(f"   Happiness Score: {most_unhappy['avg_happiness_score']:.4f}")
print(f"   Rata-rata Ranking: {int(most_unhappy['avg_ranking'])}")
print(f"   Region: {most_unhappy['region_name']}")

most_unhappy_region = regional_avg.index[0]
print(f"\n🌏 REGION PALING TIDAK BAHAGIA:")
print(f"   Region: {most_unhappy_region}")
print(f"   Rata-rata Score: {regional_avg.loc[most_unhappy_region, 'Rata-rata']:.4f}")

print("\n" + "=" * 80)
