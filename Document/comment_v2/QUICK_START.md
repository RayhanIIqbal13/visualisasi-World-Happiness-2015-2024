# 🚀 QUICK START - MEMAHAMI KODE DALAM 10 MENIT

Baca file ini untuk memahami dashboard dengan cepat!

---

## 📌 1. Struktur Folder (30 detik)

```
d:\Kampus ITK\ABD\Tugas Besar - ABD 8 v2\
├── app_whr.py                 ← MAIN APP (Frontend)
├── config_whr.py              ← DATABASE (Backend)
├── DOKUMENTASI_KODE.md        ← Dokumentasi lengkap
├── KOMENTAR_CODE_SUMMARY.md   ← Ringkasan komentar
├── QUICK_START.md             ← File ini
└── Data/
    └── Csv/ (CSV files)
```

---

## 💡 2. Konsep Utama (2 menit)

### A. Ada 2 File Utama:

**app_whr.py** (Frontend)
- Streamlit dashboard dengan 8 halaman
- User melihat: Chart, map, tabel, filter
- Cara kerja: Menerima input → Query database → Tampilkan hasil

**config_whr.py** (Backend)
- Database connection dan query functions
- 24+ functions untuk query data
- Cara kerja: Receive parameter → Execute SQL → Return data as list

### B. Data Flow:

```
User klik filter tahun "2024"
         ↓
app_whr.py terima input tahun=2024
         ↓
Panggil get_happiness_report_by_year(2024) dari config_whr.py
         ↓
config_whr.py execute SQL: WHERE year = 2024
         ↓
Database return data (list of tuples)
         ↓
app_whr.py convert ke DataFrame
         ↓
Create visualisasi dengan Plotly
         ↓
Tampilkan di browser
```

### C. Dual Function Pattern (PENTING!):

**Setiap indicator punya 2 functions:**

```python
# Function 1: Get ALL YEARS
get_happiness_report_all()
  └─ Return: 8 columns (include year, report_id, dsb)
  └─ Digunakan: Saat user pilih "Semua Tahun"

# Function 2: Get SPECIFIC YEAR  
get_happiness_report_by_year(2024)
  └─ Return: 5 columns (hanya essential data)
  └─ Digunakan: Saat user pilih tahun 2024

# Penting: Column count berbeda!
# Jika tidak match → Error!
```

---

## 🎯 3. 8 Halaman Dashboard (3 menit)

| No | Halaman | Fitur | Queries |
|---|---------|-------|---------|
| 1 | 🏠 Beranda | Statistik 4 metrics | get_region_count(), get_country_count(), dll |
| 2 | 🌐 Region | Map + Bar + Pie chart | get_region_with_countries_count() |
| 3 | 🗺️ Country | Map + Chart + Filter by region | get_countries_by_region() |
| 4 | 😊 Happiness | Ranking + Histogram + Filter tahun+region | get_happiness_report_all/by_year() |
| 5 | 💰 Economic | GDP analysis + Scatter plot + Filter | get_economic_indicators_all/by_year() |
| 6 | 👥 Social | 3 sub-pages + Bar + Heatmap + Filter | get_social_indicators_all/by_year() |
| 7 | 🤝 Perception | Generosity + Corruption + Filter | get_perception_indicators_all/by_year() |

**Key Insight:**
- Halaman 1-3: Tidak ada filter (hanya tampilkan data)
- Halaman 4-7: Ada filter tahun + region

---

## 🔑 4. Filter Pattern (2 menit)

### How Filter Works:

```python
# 1. User select di sidebar
selected_year = "2024"  atau  "Semua Tahun"
selected_region = "Western Europe"  atau  "Semua Region"

# 2. Convert string ke usable value
if selected_year_display == "Semua Tahun":
    selected_year = None  # None = all years
else:
    selected_year = int(selected_year_display)

if selected_region_display == "Semua Region":
    selected_region = None
else:
    selected_region = selected_region_display

# 3. Query dengan parameter
if selected_year is None:
    data = get_happiness_report_all()      # All years
else:
    data = get_happiness_report_by_year(selected_year)  # Specific year

# 4. Apply region filter (jika dipilih)
if selected_region:
    df = df[df['region_name'] == selected_region]

# 5. Visualisasi
st.plotly_chart(fig)
```

### Code Location:
- Sidebar dropdowns: `app_whr.py` lines ~1420-1450 (dalam setiap halaman)
- Query logic: `app_whr.py` lines ~1460-1480
- Region filter: `app_whr.py` lines ~1490-1510

---

## 🗄️ 5. Database Structure (2 menit)

### 3 Tabel Utama:

```sql
region
├─ 13 rows (Western Europe, Asia, dsb)

country
├─ 175+ rows (Denmark, Iceland, dsb)
└─ Foreign Key: region_id → region

happiness_report
├─ 1289 rows (175 countries × ~10 years)
├─ Columns: report_id, country_id, year, ranking, happiness_score
└─ Foreign Key: country_id → country
```

### 3 Tabel Indicator:

```sql
economic_indicator
├─ GDP data
└─ Foreign Key: report_id → happiness_report

social_indicator
├─ Social support, life expectancy, freedom
└─ Foreign Key: report_id → happiness_report

perception_indicator
├─ Generosity, corruption perception
└─ Foreign Key: report_id → happiness_report
```

### Join Pattern:

```sql
SELECT ...
FROM happiness_report hr
JOIN country c ON hr.country_id = c.country_id
JOIN region r ON c.region_id = r.region_id
JOIN economic_indicator ei ON hr.report_id = ei.report_id
```

---

## 📖 6. Reading Komentar (1 menit)

### Where to find comments:

**app_whr.py**
```
Lines 1-60:    Architecture overview (cara kerja keseluruhan)
Lines 60-90:   Import libraries (apa aja library yang digunakan)
Lines 150-290: halaman_beranda() dengan docstring detail
Lines 290-400: halaman_region() dengan docstring detail
Lines 1550+:   Sidebar navigation dengan comments
```

**config_whr.py**
```
Lines 1-70:    Architecture overview (database, tables, foreign keys)
Lines 75-100:  Connection setup dengan comments
Lines 100+:    Setiap function punya docstring detail:
               - FUNGSI: Apa yang dilakukan
               - PARAMETER: Input
               - RETURN: Output format
               - PENGGUNAAN: Code example
```

**Documentation Files**
```
DOKUMENTASI_KODE.md       → Full documentation (649 lines)
KOMENTAR_CODE_SUMMARY.md  → Quick reference (418 lines)
QUICK_START.md            → This file
```

---

## ✅ 7. Verifikasi Setup (1 menit)

### Check 1: Python Syntax
```bash
python -m py_compile app_whr.py config_whr.py
# Output: Tidak ada error = OK!
```

### Check 2: Database Connection
```bash
# Buka terminal Python:
python
>>> from config_whr import *
>>> # Jika tidak ada error = Database connected!
```

### Check 3: Run Dashboard
```bash
cd "d:\Kampus ITK\ABD\Tugas Besar - ABD 8 v2"
streamlit run app_whr.py
# Output: Local URL: http://localhost:8501
```

---

## 🎓 8. Learning Paths

### Path 1: Beginner (Cukup 10 menit)
1. ✅ Read this file (QUICK_START.md)
2. ✅ Open app_whr.py lines 1-60 (architecture overview)
3. ✅ Open config_whr.py lines 1-70 (database overview)
4. ✅ Open DOKUMENTASI_KODE.md → Arsitektur Aplikasi section
5. ✅ Done! Anda sudah paham 80% of the code

### Path 2: Intermediate (30 menit)
1. ✅ Read DOKUMENTASI_KODE.md → Struktur Database
2. ✅ Read config_whr.py region functions (lines 100-150)
3. ✅ Read app_whr.py halaman_region() (lines 290-400)
4. ✅ Read DOKUMENTASI_KODE.md → Alur Data section
5. ✅ Understand: How queries work + data flows

### Path 3: Advanced (1+ jam)
1. ✅ Read all config_whr.py functions dengan docstrings
2. ✅ Read all app_whr.py halaman functions dengan docstrings
3. ✅ Read DOKUMENTASI_KODE.md → Panduan Maintenance
4. ✅ Understand: How to add features, debug errors
5. ✅ Ready to modify/extend the code

---

## 🔧 9. Common Tasks

### Task 1: Understand a specific function
**Example**: Ingin tahu apa `get_happiness_report_by_year()` lakukan

```bash
# Step 1: Open config_whr.py
# Step 2: Find function (Ctrl+F: "get_happiness_report_by_year")
# Step 3: Read docstring:
#   - FUNGSI: Mengambil happiness report untuk tahun tertentu
#   - PARAMETER: year (int)
#   - RETURN: List of tuples dengan 5 columns
#   - SQL LOGIC: Penjelasan query
#   - PENGGUNAAN: Code example
```

### Task 2: Understand data flow for a page
**Example**: Ingin tahu bagaimana halaman "Happiness Report" bekerja

```bash
# Step 1: Open DOKUMENTASI_KODE.md
# Step 2: Find "Penjelasan Per Halaman" section
# Step 3: Read "4. 😊 Happiness Report" bagian
# Step 4: Understand: komponen, filters, queries, dual function pattern
```

### Task 3: Add a new query function
**Example**: Ingin menambah function untuk ambil top 5 countries

```bash
# Step 1: Read DOKUMENTASI_KODE.md → Panduan Maintenance
# Step 2: Find "Menambah Query Function Baru" bagian
# Step 3: Follow template di bagian tersebut
# Step 4: Add function ke config_whr.py
# Step 5: Import di app_whr.py dengan: from config_whr import *
# Step 6: Use function di halaman mana saja
```

---

## 🎯 10. Key Takeaways

### Tiga konsep paling penting:

1. **Dual Function Pattern**
   - `get_*_all()` = return many columns + all years
   - `get_*_by_year()` = return few columns + specific year
   - Column count harus match! Kalau tidak → ERROR!

2. **Filter Pattern**
   - "Semua Tahun" = selected_year = None
   - "2024" = selected_year = 2024
   - If selected_year is None → gunakan _all()
   - Else → gunakan _by_year()

3. **Data Flow**
   - User input → app_whr.py → config_whr.py → PostgreSQL
   - Return data → Convert to DataFrame → Visualisasi
   - Simple pipeline!

---

## 📞 Troubleshooting

### Problem: "No such table: region"
**Cause**: Database tidak punya tables
**Solution**: Run DDL_whr_v2.sql di PostgreSQL

### Problem: "5 columns passed, passed data had 8 columns"
**Cause**: Column count tidak match
**Solution**: Count columns di function return dan sesuaikan dengan DataFrame columns parameter

### Problem: Dashboard tidak muncul di browser
**Cause**: Streamlit tidak jalan dengan benar
**Solution**: 
- Check console: ada error?
- Kill existing streamlit process: `taskkill /F /IM streamlit.exe`
- Jalankan lagi: `streamlit run app_whr.py`

### Problem: Database connection error
**Cause**: PostgreSQL tidak running atau credentials salah
**Solution**:
- Check PostgreSQL service: Services → PostgreSQL
- Check DB_CONFIG di config_whr.py (host, port, user, password)
- Test: `psql -h localhost -U postgres`

---

## 🚀 Next Steps

1. ✅ Read this file (seharusnya sudah selesai)
2. 📖 Open DOKUMENTASI_KODE.md untuk deep dive
3. 💻 Open app_whr.py dan bacca comments
4. 🗄️ Open config_whr.py dan baca comments
5. 🧪 Run dashboard dan test filter
6. 🔧 Try memodifikasi kode (add new visualization, etc)

---

**Happy Learning! 🎉**

Jika ada pertanyaan, cek:
1. Inline comments di kode (app_whr.py + config_whr.py)
2. DOKUMENTASI_KODE.md untuk detailed explanation
3. KOMENTAR_CODE_SUMMARY.md untuk quick reference
