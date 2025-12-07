import json
import os

json_folder = r"d:\Kampus ITK\ABD\Tugas Besar - ABD 8 v2\Data\Json"
output_file = r"d:\Kampus ITK\ABD\Tugas Besar - ABD 8 v2\COMPLETE_INSERT_DATA.sql"

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

def escape_sql_string(s):
    """Escape single quotes in SQL strings"""
    if s is None:
        return "NULL"
    return "'" + str(s).replace("'", "''") + "'"

def generate_insert_script():
    """Generate complete SQL insert script from JSON files"""
    
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
    
    # Collect all data
    regions_data = set()
    countries_data = set()
    happiness_reports = []
    economic_indicators = []
    social_indicators = []
    perception_indicators = []
    
    print("=" * 80)
    print("GENERATING COMPLETE SQL INSERT SCRIPT")
    print("=" * 80)
    print()
    
    total_entries = 0
    
    for filename, year in files_with_years:
        filepath = os.path.join(json_folder, filename)
        
        if not os.path.exists(filepath):
            print(f"✗ File not found: {filepath}")
            continue
        
        print(f"Processing {filename} (Year: {year})...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for entry in data:
            region_name = entry.get("region_name", "")
            country_name = entry.get("country_name", "")
            region_id = REGION_MAP.get(region_name, 0)
            country_id = entry.get("country_id", 0)
            report_id = entry.get("report_id", 0)
            
            # Collect region data
            regions_data.add((region_id, region_name))
            
            # Collect country data
            countries_data.add((country_id, country_name, region_id))
            
            # Collect report data
            ranking = entry.get("ranking", 0)
            happiness_score = convert_value(entry.get("happiness_score", 0))
            dystopia_residual = convert_value(entry.get("dystopia_residual", 0))
            happiness_reports.append({
                'report_id': report_id,
                'country_id': country_id,
                'year': year,
                'ranking': ranking,
                'happiness_score': happiness_score,
                'dystopia_residual': dystopia_residual
            })
            
            # Collect economic data
            gdp_per_capita = convert_value(entry.get("gdp_per_capita", 0))
            economic_id = entry.get("economic_id", 0)
            economic_indicators.append({
                'economic_id': economic_id,
                'report_id': report_id,
                'gdp_per_capita': gdp_per_capita
            })
            
            # Collect social data
            social_support = convert_value(entry.get("social_support", 0))
            healthy_life_expectancy = convert_value(entry.get("healthy_life_expectancy", 0))
            freedom_to_make_life_choices = convert_value(entry.get("freedom_to_make_life_choices", 0))
            social_id = entry.get("social_id", 0)
            social_indicators.append({
                'social_id': social_id,
                'report_id': report_id,
                'social_support': social_support,
                'healthy_life_expectancy': healthy_life_expectancy,
                'freedom_to_make_life_choices': freedom_to_make_life_choices
            })
            
            # Collect perception data
            generosity = convert_value(entry.get("generosity", 0))
            perceptions_of_corruption = convert_value(entry.get("perceptions_of_corruption", 0))
            perception_id = entry.get("perception_id", 0)
            perception_indicators.append({
                'perception_id': perception_id,
                'report_id': report_id,
                'generosity': generosity,
                'perceptions_of_corruption': perceptions_of_corruption
            })
        
        print(f"  ✓ {len(data)} entries processed for {year}")
        total_entries += len(data)
    
    print()
    print(f"Total entries collected: {total_entries}")
    print(f"Total unique regions: {len(regions_data)}")
    print(f"Total unique countries: {len(countries_data)}")
    print()
    
    # Write SQL script
    print(f"Writing SQL script to: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- ================================================\n")
        f.write("-- COMPLETE DATA LOAD FROM JSON FILES\n")
        f.write("-- World Happiness Report Database\n")
        f.write("-- ================================================\n")
        f.write("-- Generated automatically from JSON files\n")
        f.write("-- Total entries: " + str(total_entries) + "\n")
        f.write("-- ================================================\n\n")
        
        # Insert regions
        f.write("-- =============================\n")
        f.write("-- 1. INSERT REGIONS\n")
        f.write("-- =============================\n")
        f.write("INSERT INTO region (region_id, region_name) VALUES\n")
        
        regions_list = sorted(list(regions_data))
        for i, (region_id, region_name) in enumerate(regions_list):
            f.write(f"({region_id}, {escape_sql_string(region_name)})")
            if i < len(regions_list) - 1:
                f.write(",\n")
            else:
                f.write("\n")
        f.write("ON CONFLICT (region_id) DO NOTHING;\n\n")
        
        # Insert countries
        f.write("-- =============================\n")
        f.write("-- 2. INSERT COUNTRIES\n")
        f.write("-- =============================\n")
        f.write("INSERT INTO country (country_id, country_name, region_id) VALUES\n")
        
        countries_list = sorted(list(countries_data))
        for i, (country_id, country_name, region_id) in enumerate(countries_list):
            f.write(f"({country_id}, {escape_sql_string(country_name)}, {region_id})")
            if i < len(countries_list) - 1:
                f.write(",\n")
            else:
                f.write("\n")
        f.write("ON CONFLICT (country_name) DO NOTHING;\n\n")
        
        # Insert happiness reports
        f.write("-- =============================\n")
        f.write("-- 3. INSERT HAPPINESS REPORTS\n")
        f.write("-- =============================\n")
        f.write("INSERT INTO happiness_report (report_id, country_id, year, ranking, happiness_score, dystopia_residual) VALUES\n")
        
        for i, report in enumerate(happiness_reports):
            f.write(f"({report['report_id']}, {report['country_id']}, {report['year']}, {report['ranking']}, {report['happiness_score']}, {report['dystopia_residual']})")
            if i < len(happiness_reports) - 1:
                f.write(",\n")
            else:
                f.write("\n")
        f.write("ON CONFLICT DO NOTHING;\n\n")
        
        # Insert economic indicators
        f.write("-- =============================\n")
        f.write("-- 4. INSERT ECONOMIC INDICATORS\n")
        f.write("-- =============================\n")
        f.write("INSERT INTO economic_indicator (economic_id, report_id, gdp_per_capita) VALUES\n")
        
        for i, econ in enumerate(economic_indicators):
            f.write(f"({econ['economic_id']}, {econ['report_id']}, {econ['gdp_per_capita']})")
            if i < len(economic_indicators) - 1:
                f.write(",\n")
            else:
                f.write("\n")
        f.write("ON CONFLICT DO NOTHING;\n\n")
        
        # Insert social indicators
        f.write("-- =============================\n")
        f.write("-- 5. INSERT SOCIAL INDICATORS\n")
        f.write("-- =============================\n")
        f.write("INSERT INTO social_indicator (social_id, report_id, social_support, healthy_life_expectancy, freedom_to_make_life_choices) VALUES\n")
        
        for i, social in enumerate(social_indicators):
            f.write(f"({social['social_id']}, {social['report_id']}, {social['social_support']}, {social['healthy_life_expectancy']}, {social['freedom_to_make_life_choices']})")
            if i < len(social_indicators) - 1:
                f.write(",\n")
            else:
                f.write("\n")
        f.write("ON CONFLICT DO NOTHING;\n\n")
        
        # Insert perception indicators
        f.write("-- =============================\n")
        f.write("-- 6. INSERT PERCEPTION INDICATORS\n")
        f.write("-- =============================\n")
        f.write("INSERT INTO perception_indicator (perception_id, report_id, generosity, perceptions_of_corruption) VALUES\n")
        
        for i, perception in enumerate(perception_indicators):
            f.write(f"({perception['perception_id']}, {perception['report_id']}, {perception['generosity']}, {perception['perceptions_of_corruption']})")
            if i < len(perception_indicators) - 1:
                f.write(",\n")
            else:
                f.write("\n")
        f.write("ON CONFLICT DO NOTHING;\n\n")
        
        # Add verification queries
        f.write("-- =============================\n")
        f.write("-- VERIFICATION QUERIES\n")
        f.write("-- =============================\n\n")
        
        f.write("-- Count all records\n")
        f.write("SELECT 'SUMMARY' as check_name,\n")
        f.write("       'Regions' as item,\n")
        f.write("       COUNT(*) as count FROM region\n")
        f.write("UNION ALL\n")
        f.write("SELECT 'SUMMARY', 'Countries', COUNT(*) FROM country\n")
        f.write("UNION ALL\n")
        f.write("SELECT 'SUMMARY', 'Happiness Reports', COUNT(*) FROM happiness_report\n")
        f.write("UNION ALL\n")
        f.write("SELECT 'SUMMARY', 'Economic Indicators', COUNT(*) FROM economic_indicator\n")
        f.write("UNION ALL\n")
        f.write("SELECT 'SUMMARY', 'Social Indicators', COUNT(*) FROM social_indicator\n")
        f.write("UNION ALL\n")
        f.write("SELECT 'SUMMARY', 'Perception Indicators', COUNT(*) FROM perception_indicator;\n\n")
        
        f.write("-- Sample data\n")
        f.write("SELECT \n")
        f.write("    c.country_name,\n")
        f.write("    r.region_name,\n")
        f.write("    hr.year,\n")
        f.write("    hr.ranking,\n")
        f.write("    ROUND(CAST(hr.happiness_score AS NUMERIC), 3) as happiness_score,\n")
        f.write("    ROUND(CAST(ei.gdp_per_capita AS NUMERIC), 3) as gdp_per_capita,\n")
        f.write("    ROUND(CAST(si.social_support AS NUMERIC), 3) as social_support,\n")
        f.write("    ROUND(CAST(si.healthy_life_expectancy AS NUMERIC), 3) as life_expectancy,\n")
        f.write("    ROUND(CAST(si.freedom_to_make_life_choices AS NUMERIC), 3) as freedom,\n")
        f.write("    ROUND(CAST(pi.generosity AS NUMERIC), 3) as generosity,\n")
        f.write("    ROUND(CAST(pi.perceptions_of_corruption AS NUMERIC), 3) as corruption\n")
        f.write("FROM happiness_report hr\n")
        f.write("JOIN country c ON hr.country_id = c.country_id\n")
        f.write("JOIN region r ON c.region_id = r.region_id\n")
        f.write("JOIN economic_indicator ei ON hr.report_id = ei.report_id\n")
        f.write("JOIN social_indicator si ON hr.report_id = si.report_id\n")
        f.write("JOIN perception_indicator pi ON hr.report_id = pi.report_id\n")
        f.write("ORDER BY hr.year DESC, hr.ranking ASC\n")
        f.write("LIMIT 50;\n")
    
    print()
    print("=" * 80)
    print(f"✓ SQL script generated successfully!")
    print("=" * 80)
    print(f"File: {output_file}")
    print()
    print("Summary:")
    print(f"  - Regions: {len(regions_data)}")
    print(f"  - Countries: {len(countries_data)}")
    print(f"  - Happiness Reports: {len(happiness_reports)}")
    print(f"  - Economic Indicators: {len(economic_indicators)}")
    print(f"  - Social Indicators: {len(social_indicators)}")
    print(f"  - Perception Indicators: {len(perception_indicators)}")
    print()
    print("Next steps:")
    print("1. Connect to PostgreSQL: psql -U postgres -d world_happiness_db")
    print("2. Execute the script: \\i COMPLETE_INSERT_DATA.sql")
    print("   OR: psql -U postgres -d world_happiness_db -f COMPLETE_INSERT_DATA.sql")

if __name__ == "__main__":
    generate_insert_script()
