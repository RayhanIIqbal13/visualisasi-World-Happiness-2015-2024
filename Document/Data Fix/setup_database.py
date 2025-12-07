"""
Script untuk setup database dari awal
1. Create all tables (DDL)
2. Insert region data
3. Insert country & happiness data dari JSON
"""

import json
import psycopg2
from psycopg2 import sql
from pathlib import Path
from datetime import datetime

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "database": "world_happiness_db"
}

# Region mapping
REGION_MAPPING = {
    "South Asia": 1,
    "Central and Eastern Europe": 2,
    "Sub-Saharan Africa": 3,
    "Latin America and Caribbean": 4,
    "Commonwealth of Independent States": 5,
    "North America and ANZ": 6,
    "Western Europe": 7,
    "Southeast Asia": 8,
    "East Asia": 9,
    "Middle East and North Africa": 10
}

def get_connection():
    """Establish database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection error: {e}")
        return None

def create_tables(conn):
    """Create all tables using DDL"""
    print("\n📋 Creating database tables...")
    
    ddl_file = Path('DDL_whr_v2.sql')
    if not ddl_file.exists():
        print(f"❌ DDL file not found: {ddl_file}")
        return False
    
    try:
        with open(ddl_file, 'r') as f:
            ddl_script = f.read()
        
        cursor = conn.cursor()
        cursor.execute(ddl_script)
        conn.commit()
        cursor.close()
        
        print("✅ Tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        conn.rollback()
        return False

def insert_regions(conn):
    """Insert region data"""
    print("\n🌍 Inserting region data...")
    
    try:
        cursor = conn.cursor()
        
        for region_name, region_id in REGION_MAPPING.items():
            cursor.execute(
                "INSERT INTO region (region_id, region_name) VALUES (%s, %s) "
                "ON CONFLICT (region_id) DO NOTHING",
                (region_id, region_name)
            )
        
        conn.commit()
        cursor.close()
        
        print(f"✅ Inserted {len(REGION_MAPPING)} regions")
        return True
    except Exception as e:
        print(f"❌ Error inserting regions: {e}")
        conn.rollback()
        return False

def get_region_id_for_name(region_name):
    """Get region_id for a region name, handle variations"""
    # Exact match
    if region_name in REGION_MAPPING:
        return REGION_MAPPING[region_name]
    
    # Try variations
    region_lower = region_name.lower().strip()
    for key, val in REGION_MAPPING.items():
        if key.lower() == region_lower:
            return val
    
    # Partial match
    for key, val in REGION_MAPPING.items():
        if region_lower in key.lower() or key.lower() in region_lower:
            return val
    
    print(f"⚠️  Unknown region: '{region_name}' - using 0 (akan di-skip)")
    return 0

def validate_and_load_json_data(conn):
    """Validate JSON data and insert into database"""
    print("\n📂 Loading data from JSON files...")
    
    json_dir = Path('Data/Json')
    json_files = sorted(json_dir.glob('world_happiness_*.json'))
    
    if not json_files:
        print("❌ No JSON files found")
        return False
    
    try:
        cursor = conn.cursor()
        
        total_entries = 0
        skipped_entries = 0
        inserted_entries = 0
        
        # Track unique countries for insertion
        countries_added = set()
        
        for json_file in json_files:
            year = int(json_file.stem.split('_')[-1])
            print(f"\n📄 Processing {json_file.name} (Year: {year})")
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_entries = 0
            file_skipped = 0
            
            for entry in data:
                total_entries += 1
                
                try:
                    # Validate and clean data
                    country_name = entry.get('country_name', '').strip()
                    region_name = entry.get('region_name', '').strip()
                    region_id = entry.get('region_id', 0)
                    country_id = entry.get('country_id')
                    
                    # Validate region
                    if region_id == 0 or region_id not in REGION_MAPPING.values():
                        file_skipped += 1
                        skipped_entries += 1
                        continue
                    
                    # Validate country
                    if not country_name or not country_id:
                        file_skipped += 1
                        skipped_entries += 1
                        continue
                    
                    # Insert country if not exists
                    if country_id not in countries_added:
                        try:
                            cursor.execute(
                                """INSERT INTO country (country_id, country_name, region_id) 
                                   VALUES (%s, %s, %s)
                                   ON CONFLICT (country_id) DO NOTHING""",
                                (country_id, country_name, region_id)
                            )
                            countries_added.add(country_id)
                        except Exception as e:
                            print(f"   ⚠️  Error inserting country {country_name}: {e}")
                    
                    # Convert decimal format (comma to dot)
                    def to_decimal(val):
                        if val is None:
                            return None
                        val_str = str(val).replace(',', '.')
                        try:
                            return float(val_str)
                        except:
                            return None
                    
                    # Insert happiness report
                    report_id = entry.get('report_id')
                    ranking = entry.get('ranking')
                    happiness_score = to_decimal(entry.get('happiness_score'))
                    dystopia_residual = to_decimal(entry.get('dystopia_residual'))
                    
                    cursor.execute(
                        """INSERT INTO happiness_report 
                           (report_id, country_id, year, ranking, happiness_score, dystopia_residual)
                           VALUES (%s, %s, %s, %s, %s, %s)
                           ON CONFLICT (country_id, year) DO NOTHING""",
                        (report_id, country_id, year, ranking, happiness_score, dystopia_residual)
                    )
                    
                    # Insert economic indicator
                    economic_id = entry.get('economic_id')
                    gdp = to_decimal(entry.get('gdp_per_capita'))
                    
                    cursor.execute(
                        """INSERT INTO economic_indicator (economic_id, report_id, gdp_per_capita)
                           VALUES (%s, %s, %s)
                           ON CONFLICT (report_id) DO NOTHING""",
                        (economic_id, report_id, gdp)
                    )
                    
                    # Insert social indicator
                    social_id = entry.get('social_id')
                    social_support = to_decimal(entry.get('social_support'))
                    life_expectancy = entry.get('healthy_life_expectancy')
                    freedom = to_decimal(entry.get('freedom_to_make_life_choices'))
                    
                    cursor.execute(
                        """INSERT INTO social_indicator 
                           (social_id, report_id, social_support, healthy_life_expectancy, freedom_to_make_life_choices)
                           VALUES (%s, %s, %s, %s, %s)
                           ON CONFLICT (report_id) DO NOTHING""",
                        (social_id, report_id, social_support, life_expectancy, freedom)
                    )
                    
                    # Insert perception indicator
                    perception_id = entry.get('perception_id')
                    generosity = to_decimal(entry.get('generosity'))
                    corruption = to_decimal(entry.get('perceptions_of_corruption'))
                    
                    cursor.execute(
                        """INSERT INTO perception_indicator 
                           (perception_id, report_id, generosity, perceptions_of_corruption)
                           VALUES (%s, %s, %s, %s)
                           ON CONFLICT (report_id) DO NOTHING""",
                        (perception_id, report_id, generosity, corruption)
                    )
                    
                    file_entries += 1
                    inserted_entries += 1
                    
                except Exception as e:
                    print(f"   ⚠️  Error processing entry: {e}")
                    file_skipped += 1
                    skipped_entries += 1
            
            print(f"   ✅ Inserted: {file_entries}, Skipped: {file_skipped}")
        
        conn.commit()
        cursor.close()
        
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        print(f"✅ Total entries processed: {total_entries}")
        print(f"✅ Total entries inserted: {inserted_entries}")
        print(f"⚠️  Total entries skipped: {skipped_entries}")
        print(f"✅ Unique countries inserted: {len(countries_added)}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        conn.rollback()
        return False

def verify_database(conn):
    """Verify database content"""
    print("\n✅ VERIFYING DATABASE CONTENT")
    print("=" * 60)
    
    try:
        cursor = conn.cursor()
        
        # Check each table
        tables = [
            ('region', 'regions'),
            ('country', 'countries'),
            ('happiness_report', 'happiness reports'),
            ('economic_indicator', 'economic indicators'),
            ('social_indicator', 'social indicators'),
            ('perception_indicator', 'perception indicators')
        ]
        
        for table_name, display_name in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  ✓ {display_name:.<30} {count:>5} records")
        
        cursor.close()
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error verifying database: {e}")

def main():
    """Main execution"""
    print("\n" + "=" * 60)
    print("🚀 SETTING UP WORLD HAPPINESS DATABASE")
    print("=" * 60)
    
    # Connect to database
    conn = get_connection()
    if not conn:
        print("❌ Failed to connect to database")
        return
    
    print(f"✅ Connected to database: {DB_CONFIG['database']}")
    
    # Create tables
    if not create_tables(conn):
        conn.close()
        return
    
    # Insert regions
    if not insert_regions(conn):
        conn.close()
        return
    
    # Load data from JSON
    if not validate_and_load_json_data(conn):
        conn.close()
        return
    
    # Verify
    verify_database(conn)
    
    conn.close()
    print("\n✨ Database setup completed successfully!")

if __name__ == "__main__":
    main()
