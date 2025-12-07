# 🌍 World Happiness Report Dashboard

Dashboard interaktif untuk analisis World Happiness Report (2015-2024) menggunakan Streamlit dan PostgreSQL.

## 📊 Fitur Utama

- **🏠 Beranda** - Overview statistik global dan trend kebahagiaan
- **🌍 Overview Global** - Analisis perbandingan antar region
- **💰 Indikator Ekonomi** - Analisis GDP per Capita dan korelasi dengan kebahagiaan
- **👥 Indikator Sosial** - Dukungan sosial, harapan hidup, dan kebebasan
- **🔍 Indikator Persepsi** - Kemurahan hati dan persepsi korupsi
- **🏆 Ranking & Negara** - Ranking lengkap negara per tahun

## 🗄️ Database Schema

Database menggunakan 6 tabel yang terstruktur:

```
region
├── region_id (PK)
└── region_name

country
├── country_id (PK)
├── country_name
└── region_id (FK)

happiness_report
├── report_id (PK)
├── country_id (FK)
├── year
├── ranking
├── happiness_score
└── dystopia_residual

economic_indicator
├── economic_id (PK)
├── report_id (FK, UNIQUE)
└── gdp_per_capita

social_indicator
├── social_id (PK)
├── report_id (FK, UNIQUE)
├── social_support
├── healthy_life_expectancy
└── freedom_to_make_life_choices

perception_indicator
├── perception_id (PK)
├── report_id (FK, UNIQUE)
├── generosity
└── perceptions_of_corruption
```

## 📁 File Structure

```
Tugas Besar - ABD 8 v2/
├── app.py                      # Main Streamlit application
├── config.py                   # Database configuration
├── requirements.txt            # Python dependencies
├── DDL_whr_v2.sql             # Database schema (CREATE TABLE)
├── COMPLETE_INSERT_DATA.sql   # Complete data (1,502 records)
├── generate_insert_sql.py      # Script untuk generate insert SQL
├── add_ids.py                  # Script untuk add ID fields
├── clean_and_reorder.py        # Script untuk cleanup JSON
├── Data/
│   ├── Csv/                   # CSV files (2015-2024)
│   └── Json/                  # JSON files (2015-2024, cleaned)
└── README.md                   # This file
```

## 🚀 Instalasi

### 1. Prerequisite
- Python 3.8+
- PostgreSQL 12+
- pip package manager

### 2. Setup Database

```bash
# 1. Buat database baru
createdb -U postgres world_happiness_db

# 2. Jalankan DDL script
psql -U postgres -d world_happiness_db -f DDL_whr_v2.sql

# 3. Load data
psql -U postgres -d world_happiness_db -f COMPLETE_INSERT_DATA.sql

# 4. Verifikasi
psql -U postgres -d world_happiness_db -c "SELECT COUNT(*) FROM happiness_report;"
```

Atau gunakan GUI pgAdmin:
1. Buat database baru `world_happiness_db`
2. Buka query tool dan copy-paste isi `DDL_whr_v2.sql`
3. Run DDL script
4. Buka query tool baru dan copy-paste `COMPLETE_INSERT_DATA.sql`
5. Run INSERT script

### 3. Setup Python Environment

```bash
# Clone atau download project
cd "d:\Kampus ITK\ABD\Tugas Besar - ABD 8 v2"

# Buat virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Konfigurasi Database

Edit file `config.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",              # ← Ubah ke username Anda
    "password": "postgres",          # ← Ubah ke password Anda
    "database": "world_happiness_db"
}
```

### 5. Test Koneksi Database

```bash
python config.py
```

Output yang diharapkan:
```
======================================================================
TEST KONEKSI DATABASE (PostgreSQL)
======================================================================
Host: localhost
Port: 5432
Database: world_happiness_db
User: postgres

✅ Berhasil terhubung ke PostgreSQL
   Versi: PostgreSQL 14.5

📊 Tabel yang ditemukan: 6
   ✓ country                         (175 rows)
   ✓ economic_indicator              (1,502 rows)
   ✓ happiness_report                (1,502 rows)
   ✓ perception_indicator            (1,502 rows)
   ✓ region                          (11 rows)
   ✓ social_indicator                (1,502 rows)

======================================================================
✅ KONEKSI BERHASIL
======================================================================
```

## 📱 Menjalankan Dashboard

```bash
streamlit run app.py
```

Dashboard akan terbuka di browser: `http://localhost:8501`

## 📊 Data Overview

- **Periode:** 2015-2024 (10 tahun)
- **Total Records:** 1,502 entries
- **Countries:** 175+ negara
- **Regions:** 11 wilayah geografis
- **Indicators:** 11 indikator kebahagiaan

### Data Indicators

| Indikator | Deskripsi | Range |
|-----------|-----------|-------|
| **Happiness Score** | Skor kebahagiaan (Ladder Score) | 0-10 |
| **GDP per Capita** | Produk domestik bruto per kapita (log scale) | 0-11 |
| **Social Support** | Dukungan sosial | 0-1 |
| **Life Expectancy** | Harapan hidup sehat (tahun) | 0-100 |
| **Freedom** | Kebebasan membuat pilihan hidup | 0-1 |
| **Generosity** | Skor kemurahan hati | -0.5-1 |
| **Corruption** | Persepsi korupsi pemerintah | 0-1 |
| **Dystopia Residual** | Sisa dari model regresi | 0-1 |

## 🎨 Halaman-halaman Dashboard

### 1. 🏠 Beranda
- Statistik global (negara, tahun, rata-rata)
- Trend rata-rata kebahagiaan per tahun
- Top 10 negara terbahagia (tahun terbaru)

### 2. 🌍 Overview Global
- Analisis statistik per region
- Perbandingan kebahagiaan antar region
- Jumlah negara per region
- Pie chart distribusi negara

### 3. 💰 Indikator Ekonomi
- Scatter plot GDP vs Kebahagiaan
- Histogram distribusi GDP
- Korelasi indikator dengan kebahagiaan
- Tabel data ekonomi lengkap

### 4. 👥 Indikator Sosial
- Dukungan sosial vs Kebahagiaan
- Harapan hidup vs Kebahagiaan
- Top 10 negara dukungan sosial terbaik
- Top 10 negara harapan hidup tertinggi

### 5. 🔍 Indikator Persepsi
- Kemurahan hati vs Kebahagiaan
- Persepsi korupsi vs Kebahagiaan
- Top 10 negara paling dermawan
- Top 10 negara dengan korupsi terendah

### 6. 🏆 Ranking & Negara
- Ranking negara per tahun
- Top 10 dan Bottom 10 negara
- Tabel ranking lengkap dengan filter
- Download ranking sebagai CSV

## 🔧 Troubleshooting

### Database Connection Error

**Error:** `OperationalError: could not connect to server`

**Solusi:**
1. Pastikan PostgreSQL service sudah running
2. Periksa host/port/user/password di config.py
3. Buat database jika belum ada: `createdb -U postgres world_happiness_db`

### ModuleNotFoundError: No module named 'psycopg2'

**Solusi:**
```bash
pip install psycopg2-binary
```

### Streamlit Not Found

**Solusi:**
```bash
pip install streamlit
```

### Data Not Loaded

**Solusi:**
1. Jalankan DDL script: `psql -U postgres -d world_happiness_db -f DDL_whr_v2.sql`
2. Load data: `psql -U postgres -d world_happiness_db -f COMPLETE_INSERT_DATA.sql`
3. Restart Streamlit: `streamlit run app.py`

## 📖 Dokumentasi SQL

### Contoh Query

**Top 5 Negara Terbahagia 2024:**
```sql
SELECT 
    c.country_name,
    r.region_name,
    hr.ranking,
    hr.happiness_score
FROM happiness_report hr
JOIN country c ON hr.country_id = c.country_id
JOIN region r ON c.region_id = r.region_id
WHERE hr.year = 2024
ORDER BY hr.ranking
LIMIT 5;
```

**Rata-rata Kebahagiaan per Region:**
```sql
SELECT 
    r.region_name,
    COUNT(DISTINCT c.country_id) as jumlah_negara,
    AVG(hr.happiness_score) as rata_rata_kebahagiaan
FROM happiness_report hr
JOIN country c ON hr.country_id = c.country_id
JOIN region r ON c.region_id = r.region_id
GROUP BY r.region_name
ORDER BY rata_rata_kebahagiaan DESC;
```

**Korelasi GDP dengan Kebahagiaan:**
```sql
SELECT 
    CORR(ei.gdp_per_capita, hr.happiness_score) as korelasi_gdp_kebahagiaan
FROM happiness_report hr
JOIN economic_indicator ei ON hr.report_id = ei.report_id
WHERE hr.happiness_score IS NOT NULL 
  AND ei.gdp_per_capita IS NOT NULL;
```

## 🎯 Analisis Insights

### Faktor Terpenting Kebahagiaan
1. **Dukungan Sosial** - Korelasi tertinggi dengan kebahagiaan
2. **Harapan Hidup** - Indikator kesehatan masyarakat
3. **GDP per Capita** - Kemakmuran ekonomi
4. **Kebebasan** - Otonomi individu
5. **Persepsi Korupsi** - Kepercayaan pada pemerintah
6. **Kemurahan Hati** - Solidaritas sosial

### Region dengan Kebahagiaan Tertinggi
- Western Europe (Eropa Barat)
- North America and ANZ (Amerika Utara & Australia/Selandia Baru)

### Region dengan Kebahagiaan Terendah
- Sub-Saharan Africa (Afrika Sub-Sahara)
- South Asia (Asia Selatan)

## 📝 File Descriptions

| File | Deskripsi |
|------|-----------|
| `app.py` | Main Streamlit application |
| `config.py` | Database configuration & connection |
| `requirements.txt` | Python dependencies |
| `DDL_whr_v2.sql` | Database schema (CREATE TABLE statements) |
| `COMPLETE_INSERT_DATA.sql` | Data loading script (1,502 records) |
| `generate_insert_sql.py` | Python script to generate insert SQL |
| `README.md` | This documentation |

## 🔄 Data Processing Pipeline

```
JSON Files (2015-2024)
    ↓
[generate_insert_sql.py] → COMPLETE_INSERT_DATA.sql
    ↓
PostgreSQL Database
    ↓
[app.py] → Streamlit Dashboard
```

## 👨‍💻 Development Notes

### Menambah Data Baru

1. Update JSON files di `Data/Json/`
2. Jalankan `generate_insert_sql.py`:
   ```bash
   python generate_insert_sql.py
   ```
3. Execute generated SQL ke database:
   ```bash
   psql -U postgres -d world_happiness_db -f COMPLETE_INSERT_DATA.sql
   ```

### Custom Analysis

Tambahkan halaman baru ke `app.py`:

```python
def page_custom_analysis():
    """Custom analysis page"""
    if df_happiness.empty:
        st.error("No data available")
        return
    
    st.title("Custom Analysis")
    # Your code here

# Update pages dictionary
pages_dict = {
    "🏠 Beranda": page_beranda,
    "📊 Custom Analysis": page_custom_analysis,  # Add this
    # ...other pages
}
```

## 📚 Referensi

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [World Happiness Report](https://worldhappiness.report/)

## 📄 License

This project is for educational purposes.

## ✅ Checklist Setup

- [ ] PostgreSQL installed and running
- [ ] Database `world_happiness_db` created
- [ ] DDL script executed (DDL_whr_v2.sql)
- [ ] Insert data script executed (COMPLETE_INSERT_DATA.sql)
- [ ] Python virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database connection tested (`python config.py`)
- [ ] Streamlit running (`streamlit run app.py`)

## 🆘 Support

Jika mengalami masalah:
1. Check error messages di console
2. Verify database connection: `python config.py`
3. Check `config.py` configuration
4. Check PostgreSQL service is running
5. Restart Streamlit and refresh browser

---

**Dashboard siap digunakan! 🎉**
