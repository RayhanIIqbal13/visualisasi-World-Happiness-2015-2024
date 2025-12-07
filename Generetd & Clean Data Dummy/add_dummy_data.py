import json
import os

# Mapping Regional Indicator ke Region ID dan Region Name
region_mapping = {
    "South Asia": {"region_id": 1, "region_name": "South Asia"},
    "Central and Eastern Europe": {"region_id": 2, "region_name": "Central and Eastern Europe"},
    "Sub-Saharan Africa": {"region_id": 3, "region_name": "Sub-Saharan Africa"},
    "Latin America and Caribbean": {"region_id": 4, "region_name": "Latin America and Caribbean"},
    "Commonwealth of Independent States": {"region_id": 5, "region_name": "Commonwealth of Independent States"},
    "North America and ANZ": {"region_id": 6, "region_name": "North America and ANZ"},
    "Western Europe": {"region_id": 7, "region_name": "Western Europe"},
    "Southeast Asia": {"region_id": 8, "region_name": "Southeast Asia"},
    "East Asia": {"region_id": 9, "region_name": "East Asia"},
    "Middle East and North Africa": {"region_id": 10, "region_name": "Middle East and North Africa"},
}

# Path ke folder JSON
json_folder = r"d:\Kampus ITK\ABD\Tugas Besar - ABD 8 v2\Data\Json"

# List file yang akan di-update
files_to_update = [
    "world_happiness_2015.json",
    "world_happiness_2016.json",
    "world_happiness_2017.json",
    "world_happiness_2018.json",
    "world_happiness_2019.json",
    "world_happiness_2020.json",
    "world_happiness_2021.json",
    "world_happiness_2022.json",
    "world_happiness_2023.json",
    "world_happiness_2024.json",
]

# Buat dictionary untuk menyimpan country_id
country_dict = {}
current_country_id = 1

def add_dummy_data_to_entry(entry, country_dict, current_country_id):
    """Tambahkan dummy data ke setiap entry"""
    
    # Get region info
    regional_indicator = entry.get("Regional indicator", "")
    region_info = region_mapping.get(regional_indicator, {"region_id": 11, "region_name": "Other"})
    
    # Get or create country_id
    country_name = entry.get("Country", "")
    if country_name not in country_dict:
        country_dict[country_name] = current_country_id
        current_country_id += 1
    
    country_id = country_dict[country_name]
    
    # Generate report_id (kombinasi country_id dan year/ranking untuk unique)
    # Untuk saat ini, gunakan counter sederhana
    report_id = (country_id * 1000) + entry.get("Ranking", 1)
    
    # Generate economic_id, social_id, perception_id
    economic_id = report_id * 10 + 1
    social_id = report_id * 10 + 2
    perception_id = report_id * 10 + 3
    
    # Hitung dystopia_residual (approximation)
    # dystopia_residual = happiness_score - (sum of contributions)
    try:
        happiness_score = float(str(entry.get("Happiness score", "0")).replace(",", "."))
        gdp = float(str(entry.get("GDP per capita", "0")).replace(",", "."))
        social_support = float(str(entry.get("Social support", "0")).replace(",", "."))
        life_expectancy = float(entry.get("Healthy life expectancy", 0))
        freedom = float(str(entry.get("Freedom to make life choices", "0")).replace(",", "."))
        generosity = float(str(entry.get("Generosity", "0")).replace(",", "."))
        corruption = float(str(entry.get("Perceptions of corruption", "0")).replace(",", "."))
        
        # Dystopia residual = happiness score - (sum of indicators)
        dystopia_residual = round(happiness_score - (gdp + social_support + (life_expectancy/100) + freedom + generosity + corruption), 3)
        if dystopia_residual < 0:
            dystopia_residual = 0
    except:
        dystopia_residual = 0.5
    
    # Tambahkan field dummy
    entry["dystopia_residual"] = f"{dystopia_residual:.3f}".replace(".", ",")
    entry["region_id"] = region_info["region_id"]
    entry["country_id"] = country_id
    entry["report_id"] = report_id
    entry["economic_id"] = economic_id
    entry["social_id"] = social_id
    entry["perception_id"] = perception_id
    entry["region_name"] = region_info["region_name"]
    entry["country_name"] = country_name
    
    return entry, country_dict, current_country_id

def process_json_files():
    """Process semua file JSON"""
    country_dict = {}
    current_country_id = 1
    
    for filename in files_to_update:
        filepath = os.path.join(json_folder, filename)
        
        if not os.path.exists(filepath):
            print(f"File tidak ditemukan: {filepath}")
            continue
        
        try:
            # Baca file JSON
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Update setiap entry
            for entry in data:
                entry, country_dict, current_country_id = add_dummy_data_to_entry(
                    entry, country_dict, current_country_id
                )
            
            # Simpan file JSON dengan format yang rapi
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=1, ensure_ascii=False)
            
            print(f"✓ {filename} berhasil diupdate ({len(data)} entries)")
        
        except Exception as e:
            print(f"✗ Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("Adding Dummy Data to JSON Files")
    print("=" * 60)
    
    process_json_files()
    
    print("\n" + "=" * 60)
    print("Process completed!")
    print("=" * 60)
