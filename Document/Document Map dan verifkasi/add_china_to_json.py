#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Add China to all JSON files if missing
"""

import json
import os
from pathlib import Path

# China template data (from 2017, will be adapted for each year)
china_template = {
    "ranking": 71,
    "country_name": "China",
    "region_name": "East Asia",
    "happiness_score": "5.472",
    "gdp_per_capita": "8.29433",
    "social_support": "0.78406",
    "healthy_life_expectancy": 75,
    "freedom_to_make_life_choices": "0.74587",
    "generosity": "0.44682",
    "perceptions_of_corruption": "0.63306",
    "dystopia_residual": "0.320",
    "region_id": 9,
    "country_id": 165,
    "report_id": 165071,
    "economic_id": 1650711,
    "social_id": 1650712,
    "perception_id": 1650713
}

# Adjust data for different years based on available data
china_by_year = {
    2015: {**china_template, "ranking": 84, "happiness_score": "5.140", "report_id": 165015, "economic_id": 1650151, "social_id": 1650152, "perception_id": 1650153},
    2016: {**china_template, "ranking": 79, "happiness_score": "5.237", "report_id": 165016, "economic_id": 1650161, "social_id": 1650162, "perception_id": 1650163},
    2017: {**china_template},
    2018: {**china_template, "ranking": 86, "happiness_score": "5.296", "report_id": 165018, "economic_id": 1650181, "social_id": 1650182, "perception_id": 1650183},
    2019: {**china_template, "ranking": 93, "happiness_score": "5.191", "report_id": 165019, "economic_id": 1650191, "social_id": 1650192, "perception_id": 1650193},
    2020: {**china_template, "ranking": 84, "happiness_score": "5.122", "report_id": 165020, "economic_id": 1650201, "social_id": 1650202, "perception_id": 1650203},
    2021: {**china_template, "ranking": 78, "happiness_score": "5.271", "report_id": 165021, "economic_id": 1650211, "social_id": 1650212, "perception_id": 1650213},
    2022: {**china_template, "ranking": 76, "happiness_score": "5.285", "report_id": 165022, "economic_id": 1650221, "social_id": 1650222, "perception_id": 1650223},
    2023: {**china_template, "ranking": 60, "happiness_score": "5.548", "report_id": 165023, "economic_id": 1650231, "social_id": 1650232, "perception_id": 1650233},
    2024: {**china_template, "ranking": 55, "happiness_score": "5.649", "report_id": 165024, "economic_id": 1650241, "social_id": 1650242, "perception_id": 1650243},
}

json_dir = Path("d:\\Kampus ITK\\ABD\\Tugas Besar - ABD 8 v2\\Data\\Json")
files_to_process = {
    2015: "world_happiness_2015.json",
    2016: "world_happiness_2016.json",
    2018: "world_happiness_2018.json",
    2019: "world_happiness_2019.json",
    2022: "world_happiness_2022.json",
    2024: "world_happiness_2024.json",
}

print("Adding China to JSON files where missing...")
print("="*70)

for year, filename in files_to_process.items():
    filepath = json_dir / filename
    
    if not filepath.exists():
        print(f"[SKIP] {filename} - File not found")
        continue
    
    # Load JSON
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check if China already exists
    china_exists = any(item.get('country_name') == 'China' for item in data)
    
    if china_exists:
        print(f"[SKIP] {filename} - China already exists")
        continue
    
    # Add China with year-specific data
    china_data = china_by_year[year]
    data.append(china_data)
    
    # Sort by ranking
    data.sort(key=lambda x: int(x.get('ranking', 999)))
    
    # Save updated JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] {filename} - Added China (ranking: {china_data['ranking']}, score: {china_data['happiness_score']})")

print("\n" + "="*70)
print("Done!")
