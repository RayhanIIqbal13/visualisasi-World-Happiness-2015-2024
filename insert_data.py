import json
import os
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'world_happines_v2',
    'user': 'postgres',
    'password': 'iqbal',
    'port': '5432'
}

JSON_FOLDER = r"d:\Kampus ITK\ABD\Tugas Besar - ABD 8 v2\Data\Json"

# Region mapping
REGION_MAP = {
    "South Asia": 1,
    "Central and Eastern Europe": 2,
    "Sub-Saharan Africa": 3,
    "Latin America and Caribbean": 4,
    "Commonwealth of Independent States": 5,
    "North America and ANZ": 6,
    "Western Europe": 7,
    "Southeast Asia": 8,
    "East Asia": 9,
    "Middle East and North Africa": 10,
}

def convert_value(value):
    """Convert value from string format (with comma) to float"""
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.replace(",", "."))
        except:
            return None
    return None

def insert_data():
    """Insert all data dari JSON files ke database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("=" * 80)
        print("INSERTING DATA INTO WORLD HAPPINESS REPORT DATABASE")
        print("=" * 80)
        print()
        
        # Step 1: Insert Regions
        print("Step 1: Inserting Regions...")
        regions_data = [(v, k) for k, v in REGION_MAP.items()]
        
        for region_id, region_name in sorted(regions_data):
            cursor.execute(
                "INSERT INTO region (region_id, region_name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (region_id, region_name)
            )
        
        conn.commit()
        cursor.execute("SELECT COUNT(*) FROM region")
        region_count = cursor.fetchone()[0]
        print(f"✓ {region_count} regions inserted/verified")
        print()
        
        # Step 2: Process JSON files
        files_with_years = [
            ("world_happiness_2015.json", 2015),
            ("world_happiness_2016.json", 2016),
            ("world_happiness_2017.json", 2017),
            ("world_happiness_2018.json", 2018),
            ("world_happiness_2019.json", 2019),
            ("world_happiness_2020.json", 2020),
            ("world_happiness_2021.json", 2021),
            ("world_happiness_2022.json", 2022),
            ("world_happiness_2023.json", 2023),
            ("world_happiness_2024.json", 2024),
        ]
        
        total_countries = 0
        total_reports = 0
        total_economic = 0
        total_social = 0
        total_perception = 0
        
        for filename, year in files_with_years:
            filepath = os.path.join(JSON_FOLDER, filename)
            
            if not os.path.exists(filepath):
                print(f"✗ File not found: {filepath}")
                continue
            
            print(f"Processing {filename} (Year: {year})...")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Step 2a: Insert Countries
            countries_data = []
            for entry in data:
                country_name = entry.get("country_name", "")
                region_name = entry.get("region_name", "")
                country_id = entry.get("country_id", 0)
                region_id = REGION_MAP.get(region_name, 0)
                
                countries_data.append((country_id, country_name, region_id))
            
            # Remove duplicates
            countries_data = list(set(countries_data))
            
            for country_id, country_name, region_id in countries_data:
                cursor.execute(
                    "INSERT INTO country (country_id, country_name, region_id) VALUES (%s, %s, %s) ON CONFLICT (country_name) DO NOTHING",
                    (country_id, country_name, region_id)
                )
            
            total_countries += len(countries_data)
            
            # Step 2b: Insert Reports dan Indicators
            reports_data = []
            economic_data = []
            social_data = []
            perception_data = []
            
            for entry in data:
                report_id = entry.get("report_id", 0)
                country_id = entry.get("country_id", 0)
                ranking = entry.get("ranking", 0)
                happiness_score = convert_value(entry.get("happiness_score", 0))
                dystopia_residual = convert_value(entry.get("dystopia_residual", 0))
                
                gdp_per_capita = convert_value(entry.get("gdp_per_capita", 0))
                social_support = convert_value(entry.get("social_support", 0))
                healthy_life_expectancy = convert_value(entry.get("healthy_life_expectancy", 0))
                freedom_to_make_life_choices = convert_value(entry.get("freedom_to_make_life_choices", 0))
                generosity = convert_value(entry.get("generosity", 0))
                perceptions_of_corruption = convert_value(entry.get("perceptions_of_corruption", 0))
                
                economic_id = entry.get("economic_id", 0)
                social_id = entry.get("social_id", 0)
                perception_id = entry.get("perception_id", 0)
                
                # Add to lists
                reports_data.append((report_id, country_id, year, ranking, happiness_score, dystopia_residual))
                economic_data.append((economic_id, report_id, gdp_per_capita))
                social_data.append((social_id, report_id, social_support, healthy_life_expectancy, freedom_to_make_life_choices))
                perception_data.append((perception_id, report_id, generosity, perceptions_of_corruption))
            
            # Insert Reports
            for report_id, country_id, report_year, ranking, happiness_score, dystopia_residual in reports_data:
                cursor.execute(
                    "INSERT INTO happiness_report (report_id, country_id, year, ranking, happiness_score, dystopia_residual) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                    (report_id, country_id, report_year, ranking, happiness_score, dystopia_residual)
                )
            
            total_reports += len(reports_data)
            
            # Insert Economic Indicators
            for economic_id, report_id, gdp_per_capita in economic_data:
                cursor.execute(
                    "INSERT INTO economic_indicator (economic_id, report_id, gdp_per_capita) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (economic_id, report_id, gdp_per_capita)
                )
            
            total_economic += len(economic_data)
            
            # Insert Social Indicators
            for social_id, report_id, social_support, healthy_life_expectancy, freedom_to_make_life_choices in social_data:
                cursor.execute(
                    "INSERT INTO social_indicator (social_id, report_id, social_support, healthy_life_expectancy, freedom_to_make_life_choices) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                    (social_id, report_id, social_support, healthy_life_expectancy, freedom_to_make_life_choices)
                )
            
            total_social += len(social_data)
            
            # Insert Perception Indicators
            for perception_id, report_id, generosity, perceptions_of_corruption in perception_data:
                cursor.execute(
                    "INSERT INTO perception_indicator (perception_id, report_id, generosity, perceptions_of_corruption) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                    (perception_id, report_id, generosity, perceptions_of_corruption)
                )
            
            total_perception += len(perception_data)
            
            conn.commit()
            print(f"  ✓ {len(data)} entries processed for {year}")
        
        print()
        print("=" * 80)
        print("INSERT SUMMARY")
        print("=" * 80)
        print(f"Regions inserted:              {region_count}")
        print(f"Countries inserted:            {total_countries}")
        print(f"Happiness Reports inserted:    {total_reports}")
        print(f"Economic Indicators inserted:  {total_economic}")
        print(f"Social Indicators inserted:    {total_social}")
        print(f"Perception Indicators inserted: {total_perception}")
        print()
        
        # Verify counts
        cursor.execute("SELECT COUNT(*) FROM country")
        country_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM happiness_report")
        report_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM economic_indicator")
        econ_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM social_indicator")
        social_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM perception_indicator")
        perception_count = cursor.fetchone()[0]
        
        print("VERIFICATION FROM DATABASE")
        print("=" * 80)
        print(f"Regions in DB:                 {region_count}")
        print(f"Countries in DB:               {country_count}")
        print(f"Happiness Reports in DB:       {report_count}")
        print(f"Economic Indicators in DB:     {econ_count}")
        print(f"Social Indicators in DB:       {social_count}")
        print(f"Perception Indicators in DB:   {perception_count}")
        print("=" * 80)
        print()
        print("✓ Data insertion completed successfully!")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"✗ Database error: {e}")
        if conn:
            conn.rollback()
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    insert_data()
