# 📚 DOKUMENTASI KODE - World Happiness Report Dashboard

## 📋 Daftar Isi
1. [Gambaran Umum](#gambaran-umum)
2. [Arsitektur Aplikasi](#arsitektur-aplikasi)
3. [Penjelasan File Utama](#penjelasan-file-utama)
4. [Alur Data](#alur-data)
5. [Struktur Database](#struktur-database)
6. [Penjelasan Per Halaman](#penjelasan-per-halaman)
7. [Fungsi-Fungsi Kunci](#fungsi-fungsi-kunci)
8. [Panduan Maintenance](#panduan-maintenance)

---

## 🎯 Gambaran Umum

**World Happiness Report Dashboard** adalah aplikasi web interaktif yang menampilkan analisis data kebahagiaan dunia dari 175+ negara (tahun 2015-2024).

### Teknologi Stack:
- **Frontend**: Streamlit (Python web framework)
- **Backend**: PostgreSQL 17.6 database
- **Visualisasi**: Plotly Express + Plotly Graph Objects
- **Maps**: Folium + Streamlit-folium
- **Data Processing**: Pandas, NumPy

### Features Utama:
- 🗺️ **Interactive Maps**: Peta folium dengan marker region dan negara
- 📊 **Interactive Charts**: Bar chart, pie chart, scatter plot, heatmap
- 🔍 **Filter System**: Filter by tahun dan region
- 📋 **Data Tables**: Tabel dengan export CSV
- 📈 **Statistik Ringkas**: Metrics dan summary statistics

---

## 🏗️ Arsitektur Aplikasi

```
┌─────────────────────────────────────────────────────────────┐
│                    BROWSER (User Interface)                 │
│                   Streamlit Web App UI                      │
│                   (http://localhost:8501)                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    app_whr.py (Frontend)                    │
│  8 Halaman:                                                 │
│  - Beranda (Home)                                           │
│  - Region (Map + Charts)                                    │
│  - Country (Map + Charts)                                   │
│  - Happiness Report (Ranking + Filter)                      │
│  - Economic Indicator (GDP Analysis)                        │
│  - Social Indicator (3 sub-pages)                           │
│  - Perception Indicator (Generosity + Corruption)           │
│                                                              │
│  Technologies: Streamlit, Plotly, Folium, Pandas           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  config_whr.py (Backend)                    │
│  24+ Query Functions:                                       │
│  - get_regions(), get_countries()                           │
│  - get_happiness_report_all/by_year()                       │
│  - get_economic_indicators_all/by_year()                    │
│  - get_social_indicators_all/by_year()                      │
│  - get_perception_indicators_all/by_year()                  │
│                                                              │
│  Technology: psycopg2 (PostgreSQL driver)                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│            PostgreSQL Database (localhost:5432)             │
│         Database: world_happines_v2                         │
│                                                              │
│  7 Tables:                                                  │
│  - region (13 rows)                                         │
│  - country (175+ rows)                                      │
│  - happiness_report (1289 rows)                             │
│  - economic_indicator                                       │
│  - social_indicator                                         │
│  - perception_indicator                                     │
│  - [Relationships via Foreign Keys]                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Penjelasan File Utama

### 1. **app_whr.py** (1600+ lines)
**Fungsi**: Frontend dashboard Streamlit dengan 8 halaman

**Struktur File**:
```python
1. Import & Configuration (lines 1-150)
   - Import libraries (streamlit, pandas, plotly, folium)
   - Config page layout
   - Init session state
   - Define coordinates (region + country)

2. Utility Functions (lines 150-190)
   - convert_df_to_csv(): Convert DataFrame to CSV bytes

3. Page Functions (lines 190-1570)
   - halaman_beranda(): Home page with statistics
   - halaman_region(): Region map + charts
   - halaman_country(): Country map + charts + filter
   - halaman_happiness_report(): Ranking + histogram + box plot
   - halaman_economic_indicator(): GDP analysis
   - halaman_social_indicator(): Social indicators (3 tabs)
   - halaman_perception_indicator(): Generosity + corruption

4. Sidebar Navigation (lines 1570-1620)
   - Sidebar menu buttons untuk select halaman
   - Conditional rendering based on session state
```

**Key Features**:
- Session state management untuk persist halaman aktif
- Dual filter pattern: Tahun + Region
- 4-8 tabs per halaman untuk different views (Map, Charts, Table, Stats)
- Comprehensive error handling dengan st.error()

### 2. **config_whr.py** (780+ lines)
**Fungsi**: Backend database connection & query functions

**Struktur File**:
```python
1. Database Configuration (lines 1-70)
   - DB_CONFIG dictionary
   - Connection setup
   - Error handling saat connect

2. Region Functions (lines 70-150)
   - get_regions()
   - get_region_count()
   - get_region_with_countries_count()

3. Country Functions (lines 150-230)
   - get_countries()
   - get_countries_by_region()
   - get_country_count()

4. Happiness Report Functions (lines 230-370)
   - get_happiness_report_all() → 8 columns
   - get_happiness_report_by_year() → 5 columns
   - get_happiness_report_by_country()
   - get_available_years()
   - get_happiness_count()

5. Economic Indicator Functions (lines 370-440)
   - get_economic_indicators_all() → 7 columns
   - get_economic_indicators_by_year() → 4 columns
   - get_economic_count()

6. Social Indicator Functions (lines 440-520)
   - get_social_indicators_all() → 9 columns
   - get_social_indicators_by_year() → 6 columns
   - get_social_count()

7. Perception Indicator Functions (lines 520-610)
   - get_perception_indicators_all() → 8 columns
   - get_perception_indicators_by_year() → 5 columns
   - get_perception_count()

8. Utility Functions (lines 610-650)
   - close_connection()
```

**Key Design Pattern**:
```
SETIAP INDICATOR PUNYA 2 FUNCTIONS:

get_*_all()
├─ Return: ALL YEARS data
├─ Columns: Lebih banyak (include year, id fields)
├─ Digunakan: Saat user pilih "Semua Tahun"
└─ Contoh return:
   (report_id, country_id, country_name, region_name, year, ranking, happiness_score, dystopia_residual)
   
get_*_by_year(year)
├─ Return: SPECIFIC YEAR data
├─ Columns: Lebih sedikit (hanya essential)
├─ Digunakan: Saat user pilih tahun spesifik
└─ Contoh return:
   (country_name, region_name, ranking, happiness_score, dystopia_residual)
```

---

## 🔄 Alur Data

### Scenario 1: User Filter "Semua Tahun"

```
1. User buka halaman "Happiness Report"
   ↓
2. Session state: selected_year = None
   ↓
3. app_whr.py panggil get_happiness_report_all()
   ↓
4. config_whr.py query database (NO WHERE clause for year)
   ↓
5. Database return list of tuples dengan 8 columns + ALL YEARS
   ↓
6. app_whr.py buat DataFrame dengan 8 columns:
   df = pd.DataFrame(data, columns=['report_id', 'country_id', 'country_name', 
                                    'region_name', 'year', 'ranking', 
                                    'happiness_score', 'dystopia_residual'])
   ↓
7. Visualisasi chart dengan data lengkap semua tahun
```

### Scenario 2: User Filter "Tahun 2024"

```
1. User buka halaman "Happiness Report" dan pilih tahun "2024"
   ↓
2. Session state: selected_year = 2024
   ↓
3. app_whr.py panggil get_happiness_report_by_year(2024)
   ↓
4. config_whr.py query database (WHERE year = 2024)
   ↓
5. Database return list of tuples dengan 5 columns (tahun 2024 only)
   ↓
6. app_whr.py buat DataFrame dengan 5 columns:
   df = pd.DataFrame(data, columns=['country_name', 'region_name', 'ranking', 
                                    'happiness_score', 'dystopia_residual'])
   ↓
7. Visualisasi chart dengan data tahun 2024 saja
```

**PENTING**: Column count HARUS sesuai! Jika tidak → Error!

---

## 💾 Struktur Database

### Table: region
```sql
CREATE TABLE region (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(100) UNIQUE NOT NULL
);
-- 13 rows: Western Europe, Central and Eastern Europe, dll
```

### Table: country
```sql
CREATE TABLE country (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    region_id INT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES region(region_id)
);
-- 175+ rows: Denmark, Iceland, Switzerland, dll
```

### Table: happiness_report
```sql
CREATE TABLE happiness_report (
    report_id SERIAL PRIMARY KEY,
    country_id INT NOT NULL,
    year INT NOT NULL,
    ranking INT,
    happiness_score DECIMAL(4, 3),
    dystopia_residual DECIMAL(4, 3),
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);
-- 1289 rows: 175 negara × ~10 tahun (2015-2024)
```

### Table: economic_indicator
```sql
CREATE TABLE economic_indicator (
    economic_id SERIAL PRIMARY KEY,
    report_id INT NOT NULL,
    gdp_per_capita DECIMAL(8, 6),
    FOREIGN KEY (report_id) REFERENCES happiness_report(report_id)
);
-- Join dengan happiness_report untuk dapat country_id, year, dst
```

### Table: social_indicator
```sql
CREATE TABLE social_indicator (
    social_id SERIAL PRIMARY KEY,
    report_id INT NOT NULL,
    social_support DECIMAL(4, 3),
    healthy_life_expectancy DECIMAL(5, 2),
    freedom_to_make_life_choices DECIMAL(4, 3),
    FOREIGN KEY (report_id) REFERENCES happiness_report(report_id)
);
```

### Table: perception_indicator
```sql
CREATE TABLE perception_indicator (
    perception_id SERIAL PRIMARY KEY,
    report_id INT NOT NULL,
    generosity DECIMAL(4, 3),
    perceptions_of_corruption DECIMAL(4, 3),
    FOREIGN KEY (report_id) REFERENCES happiness_report(report_id)
);
```

### Relasi Foreign Key:
```
region
  ↑
  | (1 to many)
  |
country
  ↓
  | (1 to many)
  |
happiness_report ← report_id
  ↑        ↑       ↑
  |        |       |
  |        └──────economic_indicator
  |               social_indicator
  |               perception_indicator
  └─────────────────────────────────────
```

---

## 📄 Penjelasan Per Halaman

### 1. 🏠 Beranda (Home Page)
**Komponen**:
- Title + deskripsi dashboard
- 4 Metrics: Total Region (13), Total Country (175+), Total Records (1289), Year Range (2015-2024)

**Queries**:
- `get_region_count()`
- `get_country_count()`
- `get_happiness_count()`
- `get_available_years()`

**Tanpa Filter** - semata-mata menampilkan statistik database

---

### 2. 🌐 Region
**Komponen**:
- Tab 1: Folium Map dengan circle markers
- Tab 2: Bar chart + Pie chart
- Tab 3: Table data region
- Tab 4: Statistics (min/max/mean/top 5)

**Features**:
- Map color legend: Red (many) → Blue (few)
- Marker size = proporsi jumlah negara
- Interactive: click marker untuk popup, hover untuk tooltip

**Queries**:
- `get_region_with_countries_count()`

---

### 3. 🗺️ Country
**Komponen**:
- Sidebar Filter: "Semua Region" atau pilih specific region
- Tab 1: Folium Map dengan country markers (colored by region)
- Tab 2: Bar chart jumlah country per region
- Tab 3: Table data country

**Features**:
- Filter bisa mengubah data dinamis
- Map legend dengan 13 warna untuk setiap region
- Country coordinates dari COUNTRY_COORDINATES dictionary (175+ entries)

**Queries**:
- `get_regions()` → untuk populate dropdown
- `get_countries_by_region(region_id)` atau `get_countries()`

---

### 4. 😊 Happiness Report
**Komponen**:
- Sidebar Filters: 
  - Year filter: "Semua Tahun" + [2024, 2023, ..., 2015]
  - Region filter: "Semua Region" + [13 regions]
- 4 Tabs:
  - Tab 1: Top 10 Bahagia / Tidak Bahagia (bar charts)
  - Tab 2: Histogram distribusi happiness_score
  - Tab 3: Table data dengan sortable columns
  - Tab 4: Detail view single country

**Dual Function Pattern**:
```python
if selected_year is None:
    data = get_happiness_report_all()
    df = pd.DataFrame(data, columns=[8 columns])
else:
    data = get_happiness_report_by_year(selected_year)
    df = pd.DataFrame(data, columns=[5 columns])
```

**Region Filter**:
```python
if selected_region:
    df = df[df['region_name'] == selected_region]
```

**Queries**:
- `get_happiness_report_all()` atau `get_happiness_report_by_year(year)`
- `get_regions()` → dropdown
- `get_available_years()` → dropdown

---

### 5. 💰 Economic Indicator
**Komponen**:
- Sidebar Filters: Year + Region (sama seperti Happiness Report)
- 3 Tabs:
  - Tab 1: Top 15 negara by GDP (bar chart) + scatter plot GDP vs Happiness
  - Tab 2: Table data dengan sortable
  - Tab 3: Correlation analysis (heatmap korelasi)

**Features**:
- Scatter plot: X=GDP per capita, Y=Happiness, color=region
- Filter data: GDP > 0 AND GDP IS NOT NULL (ada negara tanpa GDP data)
- Correlation heatmap: lihat hubungan antar columns

**Queries**:
- `get_economic_indicators_all()` atau `get_economic_indicators_by_year(year)`

---

### 6. 👥 Social Indicator
**Komponen**:
- Sidebar Filters: Year + Region
- 3 Sub-pages (Tabs):
  - Tab 1: Social Support, Life Expectancy, Freedom (3 bar charts horizontal)
  - Tab 2: Table data
  - Tab 3: **Grouped Bar Chart** + **Heatmap** (Perbandingan top 10 negara)

**Tab 3 - Perbandingan (Special Visualization)**:
```
Left Column: Grouped Bar Chart
├─ 3 horizontal bars: Social Support (green), Life Expectancy (blue), Freedom (purple)
├─ Top 10 countries by happiness_score
└─ Grouped layout untuk easy comparison

Right Column: Heatmap
├─ 3 rows = 3 indikators
├─ 10 columns = top 10 countries
├─ Colorscale: YlGnBu (yellow=low, blue=high)
└─ Text overlay showing normalized values
```

**Queries**:
- `get_social_indicators_all()` atau `get_social_indicators_by_year(year)`

---

### 7. 🤝 Perception Indicator
**Komponen**:
- Sidebar Filters: Year + Region
- 3 Tabs:
  - Tab 1: Top 10 Generosity (green) + Top 10 Corruption Perception (red)
  - Tab 2: Table data
  - Tab 3: Scatter plot Generosity vs Corruption + correlation heatmap

**Queries**:
- `get_perception_indicators_all()` atau `get_perception_indicators_by_year(year)`

---

## 🔧 Fungsi-Fungsi Kunci

### Session State Management
```python
# Persist data antar Streamlit re-run
st.session_state.current_page  # Halaman aktif (diubah sidebar button)
st.session_state.country_filter_region  # Region filter di halaman country
```

### Dual DataFrame Creation Pattern
```python
# PENTING: Column count harus sesuai!

if selected_year is None:
    # Data dari get_*_all() dengan 8 columns
    df = pd.DataFrame(data, columns=['col1', 'col2', ..., 'col8'])
else:
    # Data dari get_*_by_year() dengan 5 columns
    df = pd.DataFrame(data, columns=['col1', 'col2', 'col3', 'col4', 'col5'])
```

### Region Filter Pattern
```python
# Filter DataFrame berdasarkan region pilihan
if selected_region:
    df = df[df['region_name'] == selected_region]
```

### CSV Download
```python
# Convert DataFrame ke CSV bytes untuk download
csv = convert_df_to_csv(df)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='data.csv',
    mime='text/csv'
)
```

### Folium Map dengan Legend
```python
# Buat map dan tambahkan markers
m = folium.Map(location=[20, 0], zoom_start=2)

for region, (lat, lng) in REGION_COORDINATES.items():
    folium.CircleMarker(
        location=[lat, lng],
        radius=5,
        popup=region,
        tooltip=region,
        color='color_code'
    ).add_to(m)

st_folium(m, width=1300, height=500)
```

---

## 🛠️ Panduan Maintenance

### Menambah Halaman Baru

1. **Buat function halaman di app_whr.py**:
```python
def halaman_baru():
    st.title("📝 Halaman Baru")
    # ... layout dan visualisasi ...
```

2. **Tambahkan ke sidebar pages list**:
```python
pages = [
    "🏠 Beranda",
    # ... existing pages ...
    "📝 Halaman Baru"  # ← Tambah di sini
]
```

3. **Tambahkan conditional rendering**:
```python
elif st.session_state.active_page == "📝 Halaman Baru":
    halaman_baru()
```

### Menambah Query Function Baru

1. **Di config_whr.py, tambahkan function baru**:
```python
def get_data_baru_all():
    """Deskripsi lengkap function"""
    try:
        query = '''SQL QUERY'''
        c.execute(query)
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_data_baru_all: {str(e)}")
        return []

def get_data_baru_by_year(year):
    """Deskripsi lengkap function"""
    try:
        query = '''SQL QUERY WHERE year = %s'''
        c.execute(query, (year,))
        return c.fetchall()
    except Exception as e:
        print(f"❌ ERROR get_data_baru_by_year: {str(e)}")
        return []
```

2. **Di app_whr.py, import dan gunakan**:
```python
# Function sudah available via: from config_whr import *
data = get_data_baru_all()  # atau get_data_baru_by_year(year)
```

### Debugging Common Errors

**Error: "5 columns passed, passed data had 8 columns"**
- Cause: Jumlah columns di `pd.DataFrame(..., columns=[...])` tidak sesuai dengan data
- Solution: Count columns di return value dan sesuaikan dengan parameter columns

**Error: "TypeError: object is not subscriptable"**
- Cause: `c.fetchall()` return hasil yang not list of tuples
- Solution: Check SQL query dan pastikan data valid

**Error: "Database connection failed"**
- Cause: PostgreSQL tidak running atau connection info salah
- Solution: 
  - Check `DB_CONFIG` di config_whr.py
  - Pastikan PostgreSQL service berjalan
  - Test connection: `psql -h localhost -U postgres`

**Error: "No data found" / Empty DataFrame**
- Cause: Query return list kosong
- Solution:
  - Check filter parameters (year, region)
  - Verify database memang punya data
  - Print query result untuk debug

---

## 📞 Support & References

### PostgreSQL Connection String
```
postgresql://postgres:iqbal@localhost:5432/world_happines_v2
```

### Streamlit Commands
```bash
streamlit run app_whr.py              # Run dashboard
streamlit cache clear                 # Clear cache
streamlit config show                 # Show config
```

### Common Plotly Charts
```python
px.bar()      # Bar chart
px.pie()      # Pie chart
px.scatter()  # Scatter plot
px.histogram()  # Histogram
go.Figure()   # Advanced custom chart
```

### Folium Map Methods
```python
folium.Map()           # Create base map
folium.CircleMarker()  # Add circle marker
folium.Marker()        # Add regular marker
st_folium()            # Render in Streamlit
```

---

**Terakhir diupdate**: 2 Desember 2025
**Dokumentasi Version**: 1.0
**Dashboard Version**: Stable (All Features Implemented)
