# -*- coding: utf-8 -*-
# ================================================
# FILE: config_whr.py
# FUNGSI: Backend Database Configuration & Query Functions
# ================================================
#
# DESKRIPSI LENGKAP:
#   File ini adalah "BACKEND" dari dashboard World Happiness Report.
#   Semua interaksi dengan database PostgreSQL ada di file ini.
#   File ini di-import di app_whr.py dengan: from config_whr import *
#
# DATABASE INFO:
#   - Type: PostgreSQL 17.6+
#   - Host: localhost (IP address server)
#   - Port: 5432 (default PostgreSQL port)
#   - Database: world_happines_v2
#   - User: postgres
#   - Password: iqbal
#
# TABLE STRUCTURE (7 tables):
#   1. region: region_id, region_name (13 regions)
#   2. country: country_id, country_name, region_id (175+ countries)
#   3. happiness_report: report_id, country_id, year, ranking, happiness_score, dystopia_residual
#   4. economic_indicator: economic_id, report_id, gdp_per_capita
#   5. social_indicator: social_id, report_id, social_support, healthy_life_expectancy, freedom_to_make_life_choices
#   6. perception_indicator: perception_id, report_id, generosity, perceptions_of_corruption
#
# FOREIGN KEY RELATIONSHIPS:
#   happiness_report.country_id → country.country_id
#   country.region_id → region.region_id
#   economic_indicator.report_id → happiness_report.report_id
#   social_indicator.report_id → happiness_report.report_id
#   perception_indicator.report_id → happiness_report.report_id
#
# DATA PATTERN - DUAL FUNCTIONS:
#   Setiap indicator punya 2 function yang berbeda:
#   
#   1. get_*_all()
#      - Query semua data dari ALL YEARS
#      - Return column lebih banyak (include report_id, country_id, year, dst)
#      - Digunakan saat user pilih "Semua Tahun" di filter
#      Contoh: get_happiness_report_all()
#              columns: report_id, country_id, country_name, region_name, year, ranking, happiness_score, dystopia_residual (8 cols)
#   
#   2. get_*_by_year(year)
#      - Query data dari tahun SPESIFIK
#      - Return column lebih sedikit (hanya essential data)
#      - Digunakan saat user pilih tahun spesifik di filter
#      Contoh: get_happiness_report_by_year(2024)
#              columns: country_name, region_name, ranking, happiness_score, dystopia_residual (5 cols)
#
# PENTING - COLUMN MATCHING:
#   Di app_whr.py, ketika membuat DataFrame:
#   
#   if selected_year is None:
#       df = pd.DataFrame(data_all, columns=['...8 columns untuk _all()...'])
#   else:
#       df = pd.DataFrame(data_by_year, columns=['...5 columns untuk _by_year()...'])
#   
#   Jumlah columns HARUS SESUAI dengan jumlah kolom yang di-return function!
#   Jika tidak sesuai → ERROR: "5 columns passed, passed data had 8 columns"
#
# AGGREGATE FUNCTIONS:
#   - get_region_count(): Hitung jumlah region
#   - get_country_count(): Hitung jumlah country
#   - get_available_years(): List tahun-tahun tersedia
#   - get_*_count(): Hitung jumlah record untuk setiap indicator
#
# ERROR HANDLING:
#   Setiap function:
#   - Wrap dalam try-except
#   - Return [] (list kosong) jika error
#   - Print error message ke console untuk debug
#
# ================================================

import psycopg2  # Library untuk koneksi ke PostgreSQL
from psycopg2 import OperationalError, DatabaseError  # Exception handling
import sys  # Untuk keluar dari program jika koneksi gagal
import os  # Untuk akses environment variables
import streamlit as st  # Untuk akses Streamlit secrets

# ================================================
# KONFIGURASI KONEKSI DATABASE
# ================================================
# Variabel DB_CONFIG berisi informasi koneksi ke PostgreSQL
# Priority: Streamlit secrets > Environment variables > Local defaults

# Get database config from Streamlit secrets (for cloud deployment)
try:
    db_config_dict = st.secrets["database"]
    # Handle both dict and string types
    if isinstance(db_config_dict, dict):
        DB_CONFIG = {
            "host": db_config_dict.get("host", "localhost"),
            "port": int(db_config_dict.get("port", 5432)),
            "user": db_config_dict.get("user", "postgres"),
            "password": db_config_dict.get("password", ""),
            "database": db_config_dict.get("database", "world_happines_v2")
        }
    else:
        raise KeyError("database config is not a dict")
except (KeyError, FileNotFoundError, AttributeError, TypeError):
    # Fallback ke environment variables atau local config
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 5432)),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "iqbal"),
        "database": os.getenv("DB_NAME", "world_happines_v2")
    }

# ================================================
# KONEKSI KE DATABASE
# ================================================
# Blok try-except ini untuk menghubungkan ke database
# Jika berhasil: tampilkan pesan sukses + info database
# Jika gagal: tampilkan pesan error dan keluar dari program (sys.exit(1))

try:
    # Membuat koneksi ke database PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)  # ** berarti unpack dictionary ke parameter
    c = conn.cursor()  # Membuat cursor untuk menjalankan SQL query
    
    # Test koneksi dengan menjalankan query sederhana
    c.execute("SELECT version();")
    db_version = c.fetchone()  # Ambil 1 hasil dari query
    
    # Tampilkan pesan koneksi berhasil
    print("[OK] Koneksi PostgreSQL berhasil!")
    print(f"[DB] Database: {DB_CONFIG['database']}")
    print(f"[VER] PostgreSQL Version: {db_version[0].split(',')[0]}")
    
# Tangani error jika koneksi ke database gagal
except OperationalError as e:
    print("[ERROR] Gagal terhubung ke database PostgreSQL!")
    print(f"   Detail Error: {str(e)}")
    print("\n[INFO] Tips untuk memperbaiki:")
    print("   1. Pastikan PostgreSQL sudah berjalan")
    print("   2. Periksa host, port, user, password, dan database di config_whr.py")
    print("   3. Pastikan database 'world_happines_v2' sudah dibuat")
    sys.exit(1)  # Keluar dari program dengan kode error 1

# Tangani error lainnya
except Exception as e:
    print("[ERROR] Terjadi kesalahan tidak terduga!")
    print(f"   Detail Error: {str(e)}")
    sys.exit(1)

# ============================
# FUNGSI-FUNGSI UNTUK REGION
# ============================
# Region = Wilayah geografis dunia (Asia, Eropa, Afrika, dll)
# Database table: region (region_id, region_name)

def get_regions():
    """
    FUNGSI: Mengambil daftar semua region dari database
    
    RETURN: List of tuples
      Setiap tuple berisi: (region_id, region_name)
      Contoh: [(1, 'Western Europe'), (2, 'Central and Eastern Europe'), ...]
    
    PENGGUNAAN:
      region_list = get_regions()
      for region_id, region_name in region_list:
          print(region_name)
    """
    try:
        query = '''
            SELECT region_id, region_name
            FROM region
            ORDER BY region_name ASC
        '''
        c.execute(query)
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_regions: {str(e)}")
        return []

def get_region_count():
    """
    FUNGSI: Menghitung jumlah total region di database
    
    RETURN: Integer (jumlah region)
      Contoh: 13
    
    PENGGUNAAN:
      total = get_region_count()  # hasil: 13
    """
    try:
        query = 'SELECT COUNT(*) FROM region'
        c.execute(query)
        return c.fetchone()[0]
    except Exception as e:
        print(f"❌ ERROR get_region_count: {str(e)}")
        return 0

def get_region_with_countries_count():
    """
    FUNGSI: Mengambil semua region beserta jumlah negara di setiap region
    
    RETURN: List of tuples
      Setiap tuple: (region_id, region_name, country_count)
      Contoh: [(1, 'Western Europe', 10), (2, 'Central and Eastern Europe', 8), ...]
    
    SQL LOGIC:
      - LEFT JOIN = include region bahkan jika tidak ada country
      - COUNT(c.country_id) = hitung jumlah country per region
      - GROUP BY = kelompokkan hasil berdasarkan region
      - ORDER BY country_count DESC = urutkan dari terbanyak ke paling sedikit
    
    PENGGUNAAN:
      regions = get_region_with_countries_count()
      for region_id, name, count in regions:
          print(f"{name}: {count} negara")
    """
    try:
        query = '''
            SELECT 
                r.region_id,
                r.region_name,
                COUNT(c.country_id) as country_count
            FROM region r
            LEFT JOIN country c ON r.region_id = c.region_id
            GROUP BY r.region_id, r.region_name
            ORDER BY country_count DESC, r.region_name ASC
        '''
        c.execute(query)
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_region_with_countries_count: {str(e)}")
        return []

# ============================
# FUNGSI-FUNGSI UNTUK COUNTRY
# ============================
# Country = Negara-negara di dunia
# Database table: country (country_id, country_name, region_id)

def get_countries():
    """
    FUNGSI: Mengambil daftar semua negara beserta region masing-masing
    
    RETURN: List of tuples
      Setiap tuple: (country_id, country_name, region_name)
      Contoh: [(1, 'Denmark', 'Western Europe'), (2, 'Iceland', 'Northern Europe'), ...]
    
    PENGGUNAAN:
      countries = get_countries()
      for country_id, name, region in countries:
          print(f"{name} adalah bagian dari {region}")
    """
    try:
        query = '''
            SELECT 
                c.country_id,
                c.country_name,
                r.region_name
            FROM country c
            JOIN region r ON c.region_id = r.region_id
            ORDER BY r.region_name, c.country_name ASC
        '''
        c.execute(query)
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_countries: {str(e)}")
        return []

def get_countries_by_region(region_id):
    """
    FUNGSI: Mengambil negara-negara yang ada di region tertentu
    
    PARAMETER:
      region_id (int): ID region yang ingin diambil negaranya
        Contoh: 1 (Western Europe)
    
    RETURN: List of tuples
      Setiap tuple: (country_id, country_name, region_name)
    
    PENGGUNAAN:
      countries = get_countries_by_region(1)  # Ambil negara di Western Europe
      for country_id, name, region in countries:
          print(name)
    """
    try:
        query = '''
            SELECT 
                c.country_id,
                c.country_name,
                r.region_name
            FROM country c
            JOIN region r ON c.region_id = r.region_id
            WHERE c.region_id = %s
            ORDER BY c.country_name ASC
        '''
        c.execute(query, (region_id,))  # %s adalah parameter placeholder untuk keamanan
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_countries_by_region: {str(e)}")
        return []

def get_country_count():
    """
    FUNGSI: Menghitung jumlah total negara di database
    
    RETURN: Integer (jumlah negara)
      Contoh: 175
    """
    try:
        query = 'SELECT COUNT(*) FROM country'
        c.execute(query)
        return c.fetchone()[0]
    except Exception as e:
        print(f"❌ ERROR get_country_count: {str(e)}")
        return 0

# ============================
# FUNGSI-FUNGSI UNTUK HAPPINESS REPORT
# ============================
# Happiness Report = Data skor kebahagiaan negara per tahun
# Database table: happiness_report (report_id, country_id, year, ranking, happiness_score, dystopia_residual)
#
# SKEMA DATA:
#   - report_id: Unique identifier untuk setiap record
#   - country_id: ID negara (foreign key ke tabel country)
#   - year: Tahun pengumpulan data (2015-2024)
#   - ranking: Ranking kebahagiaan negara di tahun itu (1 = paling bahagia)
#   - happiness_score: Skor kebahagiaan (0-10, semakin tinggi = semakin bahagia)
#   - dystopia_residual: Residual dari dystopia index

def get_happiness_report_all():
    """
    FUNGSI: Mengambil SEMUA data happiness report dari ALL YEARS
    
    RETURN: List of tuples
      Setiap tuple: (report_id, country_id, country_name, region_name, year, ranking, happiness_score, dystopia_residual)
    
    SQL LOGIC:
      - JOIN happiness_report dengan country untuk mendapat country_name dan region_name
      - Menggabungkan data dari 3 tabel: happiness_report, country, region
      - Urutkan by year DESC (terbaru dulu), ranking ASC (ranking terbaik dulu)
    
    KAPAN DIGUNAKAN:
      - Saat user memilih "Semua Tahun" di filter
      - Menampilkan semua data tanpa filter tahun
    
    PENGGUNAAN:
      data = get_happiness_report_all()
      df = pd.DataFrame(data, columns=['report_id', 'country_id', 'country_name', 'region_name', 
                                       'year', 'ranking', 'happiness_score', 'dystopia_residual'])
    """
    try:
        query = '''
            SELECT 
                hr.report_id,
                hr.country_id,
                c.country_name,
                r.region_name,
                hr.year,
                hr.ranking,
                hr.happiness_score,
                hr.dystopia_residual
            FROM happiness_report hr
            JOIN country c ON hr.country_id = c.country_id
            JOIN region r ON c.region_id = r.region_id
            ORDER BY hr.year DESC, hr.ranking ASC
        '''
        c.execute(query)
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_happiness_report_all: {str(e)}")
        return []

def get_happiness_report_by_country(country_id):
    """
    FUNGSI: Mengambil data happiness report untuk 1 negara across ALL YEARS
    
    PARAMETER:
      country_id (int): ID negara yang ingin dianalisis
    
    RETURN: List of tuples
      Setiap tuple: (year, ranking, happiness_score, dystopia_residual)
    
    PENGGUNAAN:
      data = get_happiness_report_by_country(1)  # Data Denmark dari 2015-2024
      # Berguna untuk tracking trend kebahagiaan 1 negara seiring waktu
    """
    try:
        query = '''
            SELECT 
                hr.year,
                hr.ranking,
                hr.happiness_score,
                hr.dystopia_residual
            FROM happiness_report hr
            WHERE hr.country_id = %s
            ORDER BY hr.year ASC
        '''
        c.execute(query, (country_id,))
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_happiness_report_by_country: {str(e)}")
        return []

def get_happiness_report_by_year(year):
    """
    FUNGSI: Mengambil data happiness report untuk TAHUN TERTENTU
    
    PARAMETER:
      year (int): Tahun yang ingin diambil datanya
        Contoh: 2024
    
    RETURN: List of tuples
      Setiap tuple: (country_name, region_name, ranking, happiness_score, dystopia_residual)
      PERHATIAN: Tidak ada report_id dan country_id (berbeda dengan _all())
    
    SQL LOGIC:
      - WHERE hr.year = %s: Filter hanya data tahun tertentu
      - ORDER BY ranking ASC: Urutkan dari ranking terbaik (1) ke terburuk
    
    KAPAN DIGUNAKAN:
      - Saat user memilih TAHUN SPESIFIK di filter (bukan "Semua Tahun")
      - Menampilkan ranking dan skor kebahagiaan untuk tahun itu saja
    
    PENGGUNAAN:
      data = get_happiness_report_by_year(2024)
      df = pd.DataFrame(data, columns=['country_name', 'region_name', 'ranking', 'happiness_score', 'dystopia_residual'])
    """
    try:
        query = '''
            SELECT 
                c.country_name,
                r.region_name,
                hr.ranking,
                hr.happiness_score,
                hr.dystopia_residual
            FROM happiness_report hr
            JOIN country c ON hr.country_id = c.country_id
            JOIN region r ON c.region_id = r.region_id
            WHERE hr.year = %s
            ORDER BY hr.ranking ASC
        '''
        c.execute(query, (year,))
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_happiness_report_by_year: {str(e)}")
        return []

def get_happiness_report_all_aggregated():
    """
    FUNGSI: Mengambil happiness report SEMUA TAHUN dengan AVERAGE ranking dan score per negara
    
    RETURN: List of tuples
      Setiap tuple: (country_name, region_name, avg_ranking, avg_happiness_score)
      - 4 kolom total (AGGREGATED across all years 2015-2024)
    
    SQL LOGIC:
      - GROUP BY country_id
      - Hitung AVG(ranking) untuk rata-rata peringkat kebahagiaan
      - Hitung AVG(happiness_score) untuk rata-rata skor kebahagiaan
      - Bermanfaat untuk melihat performa keseluruhan negara dalam 10 tahun terakhir
    
    PENGGUNAAN:
      data = get_happiness_report_all_aggregated()
      df = pd.DataFrame(data, columns=['country_name', 'region_name', 'avg_ranking', 'avg_happiness_score'])
      # Data siap untuk visualisasi dengan rata-rata across all years
    
    CONTOH HASIL:
      ('Denmark', 'Europe', 1.5, 7.456)
      ('Qatar', 'Middle East', 25.3, 6.374)
    """
    try:
        query = '''
            SELECT 
                c.country_name,
                r.region_name,
                AVG(hr.ranking) as avg_ranking,
                AVG(hr.happiness_score) as avg_happiness_score
            FROM happiness_report hr
            JOIN country c ON hr.country_id = c.country_id
            JOIN region r ON c.region_id = r.region_id
            GROUP BY c.country_id, c.country_name, r.region_name
            ORDER BY avg_happiness_score DESC NULLS LAST
        '''
        c.execute(query)
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_happiness_report_all_aggregated: {str(e)}")
        return []

def get_available_years():
    """
    FUNGSI: Mengambil daftar tahun-tahun apa saja yang ada di database
    
    RETURN: List of integers
      Contoh: [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015]
    
    PENGGUNAAN:
      years = get_available_years()
      # Untuk populate dropdown filter tahun di sidebar
      for year in years:
          st.button(f"Tahun {year}")
    """
    try:
        query = '''
            SELECT DISTINCT year
            FROM happiness_report
            ORDER BY year DESC
        '''
        c.execute(query)
        return [row[0] for row in c.fetchall()]  # Extract year dari setiap tuple
    except Exception as e:
        print(f"❌ ERROR get_available_years: {str(e)}")
        return []

def get_happiness_count():
    """
    FUNGSI: Menghitung jumlah total record happiness report di database
    
    RETURN: Integer (total records)
      Contoh: 1289 (175 negara × 10 tahun ≈ 1289 records)
    """
    try:
        query = 'SELECT COUNT(*) FROM happiness_report'
        c.execute(query)
        return c.fetchone()[0]
    except Exception as e:
        print(f"❌ ERROR get_happiness_count: {str(e)}")
        return 0

# ============================
# FUNGSI-FUNGSI UNTUK ECONOMIC INDICATOR
# ============================
# Economic Indicator = Data indikator ekonomi (GDP per Capita) negara
# Database table: economic_indicator (economic_id, report_id, gdp_per_capita)
#
# PENJELASAN:
#   - economic_id: Unique identifier untuk setiap record
#   - report_id: Foreign key ke happiness_report (menghubungkan ke negara dan tahun)
#   - gdp_per_capita: Nilai GDP per kapita negara (dalam USD)
#   - Berguna untuk melihat hubungan antara kesejahteraan ekonomi dan kebahagiaan

def get_economic_indicators_all():
    """
    FUNGSI: Mengambil SEMUA data economic indicators dari ALL YEARS
    
    RETURN: List of tuples
      Setiap tuple: (economic_id, report_id, country_name, region_name, year, happiness_score, gdp_per_capita)
      - 7 kolom total
    
    SQL LOGIC:
      - JOIN economic_indicator dengan happiness_report, country, region
      - Menggabungkan data indikator ekonomi dengan info negara dan kebahagiaan
    
    PENGGUNAAN:
      data = get_economic_indicators_all()
      df = pd.DataFrame(data, columns=['economic_id', 'report_id', 'country_name', 'region_name',
                                       'year', 'happiness_score', 'gdp_per_capita'])
    """
    try:
        query = '''
            SELECT 
                ei.economic_id,
                hr.report_id,
                c.country_name,
                r.region_name,
                hr.year,
                hr.happiness_score,
                ei.gdp_per_capita
            FROM economic_indicator ei
            JOIN happiness_report hr ON ei.report_id = hr.report_id
            JOIN country c ON hr.country_id = c.country_id
            JOIN region r ON c.region_id = r.region_id
            ORDER BY hr.year DESC, c.country_name ASC
        '''
        c.execute(query)
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_economic_indicators_all: {str(e)}")
        return []

def get_economic_indicators_by_year(year):
    """
    FUNGSI: Mengambil economic indicators untuk TAHUN TERTENTU (dengan filter GDP valid)
    
    PARAMETER:
      year (int): Tahun yang ingin diambil datanya
    
    RETURN: List of tuples
      Setiap tuple: (country_name, region_name, happiness_score, gdp_per_capita)
      - 4 kolom total (berbeda dengan _all())
    
    SQL LOGIC:
      - WHERE hr.year = %s: Filter tahun spesifik
      - AND ei.gdp_per_capita > 0 AND ei.gdp_per_capita IS NOT NULL: Hanya GDP yang valid
        (Ada beberapa negara tanpa data GDP, maka difilter out)
      - ORDER BY gdp_per_capita DESC: Urutkan dari GDP terbesar (negara kaya) ke terkecil
    
    PENGGUNAAN:
      data = get_economic_indicators_by_year(2024)
      df = pd.DataFrame(data, columns=['country_name', 'region_name', 'happiness_score', 'gdp_per_capita'])
      # Data siap untuk visualisasi scatter plot (GDP vs Happiness)
    """
    try:
        query = '''
            SELECT 
                c.country_name,
                r.region_name,
                hr.happiness_score,
                ei.gdp_per_capita
            FROM economic_indicator ei
            JOIN happiness_report hr ON ei.report_id = hr.report_id
            JOIN country c ON hr.country_id = c.country_id
            JOIN region r ON c.region_id = r.region_id
            WHERE hr.year = %s AND ei.gdp_per_capita > 0 AND ei.gdp_per_capita IS NOT NULL
            ORDER BY ei.gdp_per_capita DESC NULLS LAST
        '''
        c.execute(query, (year,))
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_economic_indicators_by_year: {str(e)}")
        return []

def get_economic_indicators_all_aggregated():
    """
    FUNGSI: Mengambil economic indicators SEMUA TAHUN dengan TOTAL GDP per negara
    
    DESKRIPSI:
      Ketika user filter "Semua Tahun", data di-aggregate (dijumlahkan) per negara.
      Ini memberikan gambaran total economic output setiap negara across all years.
    
    RETURN: List of tuples
      Setiap tuple: (country_name, region_name, total_gdp, avg_happiness_score)
      - 4 kolom total
      - total_gdp: SUM dari GDP per capita across all years
      - avg_happiness_score: AVERAGE dari happiness score
    
    SQL LOGIC:
      - GROUP BY c.country_id, c.country_name, r.region_name: Aggregate per negara
      - SUM(ei.gdp_per_capita): Total GDP across all years
      - AVG(hr.happiness_score): Rata-rata kebahagiaan
      - WHERE ei.gdp_per_capita > 0: Filter hanya data GDP valid
      - ORDER BY total_gdp DESC: Urutkan dari total terbesar
    
    PENGGUNAAN:
      data = get_economic_indicators_all_aggregated()
      df = pd.DataFrame(data, columns=['country_name', 'region_name', 'total_gdp', 'avg_happiness_score'])
      # Data siap untuk visualisasi top 15 negara by total GDP
    
    CONTOH HASIL:
      ('Qatar', 'Western Asia', 550.50, 6.374)  ← Total GDP dari 2015-2024, avg happiness
      ('Luxembourg', 'Western Europe', 480.25, 7.081)
      ('Singapura', 'Southeast Asia', 430.15, 6.480)
    """
    try:
        query = '''
            SELECT 
                c.country_name,
                r.region_name,
                SUM(ei.gdp_per_capita) as total_gdp,
                AVG(hr.happiness_score) as avg_happiness_score
            FROM economic_indicator ei
            JOIN happiness_report hr ON ei.report_id = hr.report_id
            JOIN country c ON hr.country_id = c.country_id
            JOIN region r ON c.region_id = r.region_id
            WHERE ei.gdp_per_capita > 0 AND ei.gdp_per_capita IS NOT NULL
            GROUP BY c.country_id, c.country_name, r.region_name
            ORDER BY total_gdp DESC NULLS LAST
        '''
        c.execute(query)
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_economic_indicators_all_aggregated: {str(e)}")
        return []

def get_economic_count():
    """
    FUNGSI: Menghitung jumlah total economic indicator records
    
    RETURN: Integer (total records dengan GDP data)
    """
    try:
        query = 'SELECT COUNT(*) FROM economic_indicator'
        c.execute(query)
        return c.fetchone()[0]
    except Exception as e:
        print(f"❌ ERROR get_economic_count: {str(e)}")
        return 0

# ============================
# FUNGSI-FUNGSI UNTUK SOCIAL INDICATOR
# ============================
# Social Indicator = Data indikator sosial negara
# Database table: social_indicator (social_id, report_id, social_support, healthy_life_expectancy, freedom_to_make_life_choices)
#
# KOMPONEN INDIKATOR SOSIAL:
#   1. social_support: Dukungan sosial dari keluarga/teman (0-1, semakin tinggi semakin baik)
#   2. healthy_life_expectancy: Harapan hidup sehat dalam tahun (0-100)
#   3. freedom_to_make_life_choices: Kebebasan membuat pilihan hidup (0-1, semakin tinggi semakin bebas)

def get_social_indicators_all():
    """
    FUNGSI: Mengambil SEMUA data social indicators dari ALL YEARS
    
    RETURN: List of tuples
      Setiap tuple: (social_id, report_id, country_name, region_name, year, happiness_score, 
                     social_support, healthy_life_expectancy, freedom_to_make_life_choices)
      - 9 kolom total
    
    PENGGUNAAN:
      data = get_social_indicators_all()
      df = pd.DataFrame(data, columns=['social_id', 'report_id', 'country_name', 'region_name', 'year',
                                       'happiness_score', 'social_support', 'healthy_life_expectancy', 
                                       'freedom_to_make_life_choices'])
    """
    try:
        query = '''
            SELECT 
                si.social_id,
                hr.report_id,
                c.country_name,
                r.region_name,
                hr.year,
                hr.happiness_score,
                si.social_support,
                si.healthy_life_expectancy,
                si.freedom_to_make_life_choices
            FROM social_indicator si
            JOIN happiness_report hr ON si.report_id = hr.report_id
            JOIN country c ON hr.country_id = c.country_id
            JOIN region r ON c.region_id = r.region_id
            ORDER BY hr.year DESC, c.country_name ASC
        '''
        c.execute(query)
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_social_indicators_all: {str(e)}")
        return []

def get_social_indicators_by_year(year):
    """
    FUNGSI: Mengambil social indicators untuk TAHUN TERTENTU
    
    PARAMETER:
      year (int): Tahun yang ingin diambil
    
    RETURN: List of tuples
      Setiap tuple: (country_name, region_name, happiness_score, social_support, 
                     healthy_life_expectancy, freedom_to_make_life_choices)
      - 6 kolom total (berbeda dengan _all())
    
    SQL LOGIC:
      - Ambil 3 indikator sosial untuk tahun spesifik
      - Social_support dan freedom 0-1 scale, healthy_life_expectancy 0-100 scale
    
    PENGGUNAAN:
      data = get_social_indicators_by_year(2024)
      df = pd.DataFrame(data, columns=['country_name', 'region_name', 'happiness_score',
                                       'social_support', 'healthy_life_expectancy', 
                                       'freedom_to_make_life_choices'])
      # Data siap untuk visualisasi: Grouped Bar Chart + Heatmap
    """
    try:
        query = '''
            SELECT 
                c.country_name,
                r.region_name,
                hr.happiness_score,
                si.social_support,
                si.healthy_life_expectancy,
                si.freedom_to_make_life_choices
            FROM social_indicator si
            JOIN happiness_report hr ON si.report_id = hr.report_id
            JOIN country c ON hr.country_id = c.country_id
            JOIN region r ON c.region_id = r.region_id
            WHERE hr.year = %s
            ORDER BY c.country_name ASC
        '''
        c.execute(query, (year,))
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_social_indicators_by_year: {str(e)}")
        return []

def get_social_indicators_all_aggregated():
    """
    FUNGSI: Mengambil social indicators SEMUA TAHUN dengan AVERAGE per negara
    
    DESKRIPSI:
      Ketika user filter "Semua Tahun", data di-aggregate (di-rata-rata) per negara.
      Ini memberikan gambaran rata-rata social indicators setiap negara across all years.
    
    RETURN: List of tuples
      Setiap tuple: (country_name, region_name, avg_social_support, avg_life_expectancy, avg_freedom, avg_happiness_score)
      - 6 kolom total
      - avg_social_support: AVERAGE dari social_support across all years
      - avg_life_expectancy: AVERAGE dari healthy_life_expectancy
      - avg_freedom: AVERAGE dari freedom_to_make_life_choices
      - avg_happiness_score: AVERAGE dari happiness score
    
    SQL LOGIC:
      - GROUP BY c.country_id, c.country_name, r.region_name: Aggregate per negara
      - AVG(): Rata-rata untuk setiap indicator across all years
      - ORDER BY avg_happiness_score DESC: Urutkan dari kebahagiaan tertinggi
    
    PENGGUNAAN:
      data = get_social_indicators_all_aggregated()
      df = pd.DataFrame(data, columns=['country_name', 'region_name', 
                                       'avg_social_support', 'avg_life_expectancy', 
                                       'avg_freedom', 'avg_happiness_score'])
    """
    try:
        query = '''
            SELECT 
                c.country_name,
                r.region_name,
                AVG(si.social_support) as avg_social_support,
                AVG(si.healthy_life_expectancy) as avg_life_expectancy,
                AVG(si.freedom_to_make_life_choices) as avg_freedom,
                AVG(hr.happiness_score) as avg_happiness_score
            FROM social_indicator si
            JOIN happiness_report hr ON si.report_id = hr.report_id
            JOIN country c ON hr.country_id = c.country_id
            JOIN region r ON c.region_id = r.region_id
            GROUP BY c.country_id, c.country_name, r.region_name
            ORDER BY avg_happiness_score DESC NULLS LAST
        '''
        c.execute(query)
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_social_indicators_all_aggregated: {str(e)}")
        return []

def get_social_count():
    """
    FUNGSI: Menghitung jumlah total social indicator records
    
    RETURN: Integer (total records)
    """
    try:
        query = 'SELECT COUNT(*) FROM social_indicator'
        c.execute(query)
        return c.fetchone()[0]
    except Exception as e:
        print(f"❌ ERROR get_social_count: {str(e)}")
        return 0

# ============================
# FUNGSI-FUNGSI UNTUK PERCEPTION INDICATOR
# ============================
# Perception Indicator = Data indikator persepsi publik negara
# Database table: perception_indicator (perception_id, report_id, generosity, perceptions_of_corruption)
#
# KOMPONEN INDIKATOR PERSEPSI:
#   1. generosity: Tingkat kemurahan hati di negara (0-1, semakin tinggi semakin dermawan)
#   2. perceptions_of_corruption: Persepsi korupsi publik (0-1, semakin rendah semakin dipercaya)

def get_perception_indicators_all():
    """
    FUNGSI: Mengambil SEMUA data perception indicators dari ALL YEARS
    
    RETURN: List of tuples
      Setiap tuple: (perception_id, report_id, country_name, region_name, year, happiness_score,
                     generosity, perceptions_of_corruption)
      - 8 kolom total
    
    PENGGUNAAN:
      data = get_perception_indicators_all()
      df = pd.DataFrame(data, columns=['perception_id', 'report_id', 'country_name', 'region_name',
                                       'year', 'happiness_score', 'generosity', 'perceptions_of_corruption'])
    """
    try:
        query = '''
            SELECT 
                pi.perception_id,
                hr.report_id,
                c.country_name,
                r.region_name,
                hr.year,
                hr.happiness_score,
                pi.generosity,
                pi.perceptions_of_corruption
            FROM perception_indicator pi
            JOIN happiness_report hr ON pi.report_id = hr.report_id
            JOIN country c ON hr.country_id = c.country_id
            JOIN region r ON c.region_id = r.region_id
            ORDER BY hr.year DESC, c.country_name ASC
        '''
        c.execute(query)
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_perception_indicators_all: {str(e)}")
        return []

def get_perception_indicators_by_year(year):
    """
    FUNGSI: Mengambil perception indicators untuk TAHUN TERTENTU
    
    PARAMETER:
      year (int): Tahun yang ingin diambil
    
    RETURN: List of tuples
      Setiap tuple: (country_name, region_name, happiness_score, generosity, perceptions_of_corruption)
      - 5 kolom total (berbeda dengan _all())
    
    SQL LOGIC:
      - Ambil data generosity dan perceptions_of_corruption untuk tahun spesifik
      - Scale: 0-1 untuk kedua indikator
    
    PENGGUNAAN:
      data = get_perception_indicators_by_year(2024)
      df = pd.DataFrame(data, columns=['country_name', 'region_name', 'happiness_score',
                                       'generosity', 'perceptions_of_corruption'])
      # Data siap untuk visualisasi: Bar charts + Scatter plot korelasi
    """
    try:
        query = '''
            SELECT 
                c.country_name,
                r.region_name,
                hr.happiness_score,
                pi.generosity,
                pi.perceptions_of_corruption
            FROM perception_indicator pi
            JOIN happiness_report hr ON pi.report_id = hr.report_id
            JOIN country c ON hr.country_id = c.country_id
            JOIN region r ON c.region_id = r.region_id
            WHERE hr.year = %s
            ORDER BY c.country_name ASC
        '''
        c.execute(query, (year,))
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_perception_indicators_by_year: {str(e)}")
        return []

def get_perception_indicators_all_aggregated():
    """
    FUNGSI: Mengambil perception indicators SEMUA TAHUN dengan AVERAGE per negara
    
    RETURN: List of tuples
      Setiap tuple: (country_name, region_name, avg_generosity, avg_perceptions_of_corruption, avg_happiness_score)
      - 5 kolom total (AGGREGATED across all years 2015-2024)
    
    SQL LOGIC:
      - GROUP BY country_id
      - Hitung AVG(generosity) untuk rata-rata kemurahhatian
      - Hitung AVG(perceptions_of_corruption) untuk rata-rata persepsi korupsi
      - Hitung AVG(happiness_score) untuk rata-rata happiness score
      - Bermanfaat untuk melihat rata-rata "kemurahhatian" dan "persepsi korupsi" negara dalam 10 tahun
    
    PENGGUNAAN:
      data = get_perception_indicators_all_aggregated()
      df = pd.DataFrame(data, columns=['country_name', 'region_name', 'avg_generosity',
                                       'avg_perceptions_of_corruption', 'avg_happiness_score'])
      # Data siap untuk visualisasi dengan total/rata-rata across all years
    
    CONTOH HASIL:
      ('Denmark', 'Europe', 0.4821, 0.1234, 7.456)
      ('Qatar', 'Middle East', 0.3421, 0.5623, 6.374)
    """
    try:
        query = '''
            SELECT 
                c.country_name,
                r.region_name,
                AVG(pi.generosity) as avg_generosity,
                AVG(pi.perceptions_of_corruption) as avg_perceptions_of_corruption,
                AVG(hr.happiness_score) as avg_happiness_score
            FROM perception_indicator pi
            JOIN happiness_report hr ON pi.report_id = hr.report_id
            JOIN country c ON hr.country_id = c.country_id
            JOIN region r ON c.region_id = r.region_id
            GROUP BY c.country_id, c.country_name, r.region_name
            ORDER BY avg_happiness_score DESC NULLS LAST
        '''
        c.execute(query)
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_perception_indicators_all_aggregated: {str(e)}")
        return []

def get_perception_count():
    """
    FUNGSI: Menghitung jumlah total perception indicator records
    
    RETURN: Integer (total records)
    """
    try:
        query = 'SELECT COUNT(*) FROM perception_indicator'
        c.execute(query)
        return c.fetchone()[0]
    except Exception as e:
        print(f"❌ ERROR get_perception_count: {str(e)}")
        return 0

# ============================
# FUNGSI UTILITY
# ============================

def close_connection():
    """
    FUNGSI: Menutup koneksi ke database PostgreSQL (opsional)
    
    DESKRIPSI:
      - Menutup cursor (c.close())
      - Menutup connection (conn.close())
      - Menampilkan pesan sukses jika berhasil
    
    PENGGUNAAN:
      # Biasanya tidak dipanggil karena Streamlit menangani connection lifecycle
      # Tapi bisa dipakai jika perlu cleanup manual
      close_connection()
    
    PERHATIAN:
      - Jangan panggil di dalam Streamlit app, karena akan menutup semua koneksi
      - Hanya gunakan untuk debug atau cleanup
    """
    global conn, c
    try:
        if c:
            c.close()
            print("✅ Cursor ditutup")
        if conn:
            conn.close()
            print("✅ Koneksi database ditutup")
    except Exception as e:
        print(f"❌ ERROR saat menutup koneksi: {str(e)}")


# ============================
# SUMMARY PENGGUNAAN CONFIG_WRH.PY
# ============================
# File ini adalah "backend" dari dashboard
# Di-import di app_whr.py dengan: from config_whr import *
# Sehingga semua function dan variable global (conn, c, DB_CONFIG) tersedia di app
#
# ALUR DATA:
#   1. Streamlit User membuka dashboard → Jalankan app_whr.py
#   2. app_whr.py import config_whr → Koneksi ke database PostgreSQL
#   3. User memilih filter (tahun, region, dsb) → app_whr.py panggil function dari config_whr
#   4. Function query database dan return data sebagai list of tuples
#   5. app_whr.py convert tuples ke DataFrame (pandas) → Visualisasi dengan Plotly
#   6. Streamlit menampilkan chart dan tabel di browser
#
# QUERY PATTERN:
#   - get_*_all() = Return data dari ALL YEARS dengan lebih banyak kolom
#   - get_*_by_year(year) = Return data dari TAHUN SPESIFIK dengan kolom lebih sedikit
#   - Ini penting karena app_whr.py membuat DataFrame dengan jumlah kolom berbeda
#
# ERROR HANDLING:
#   - Setiap function punya try-except
#   - Jika error, print pesan error dan return [] (list kosong) atau 0
#   - Streamlit app akan menampilkan "Data tidak ditemukan" jika dapat list kosong
