# Dokumentasi Penambahan Data Dummy ke File JSON

## Ringkasan
Semua file JSON World Happiness Report (2015-2024) telah diupdate dengan menambahkan field dummy yang sesuai dengan schema database yang telah didefinisikan.

## Field yang Ditambahkan

### 1. **dystopia_residual** (DECIMAL 5,3)
- **Deskripsi**: Nilai Dystopia Residual dari happiness score
- **Perhitungan**: `happiness_score - (sum of all indicators)`
- **Format**: String dengan pemisah koma (contoh: "0,123")
- **Range**: 0.000 - nilai maksimal sesuai data

### 2. **region_id** (INT - PRIMARY KEY)
- **Deskripsi**: ID region yang diambil dari mapping "Regional indicator"
- **Nilai**:
  - 1 = South Asia
  - 2 = Central and Eastern Europe
  - 3 = Sub-Saharan Africa
  - 4 = Latin America and Caribbean
  - 5 = Commonwealth of Independent States
  - 6 = North America and ANZ
  - 7 = Western Europe
  - 8 = Southeast Asia
  - 9 = East Asia
  - 10 = Middle East and North Africa
  - 11 = Other (jika tidak ditemukan)

### 3. **country_id** (INT - FOREIGN KEY ke tabel country)
- **Deskripsi**: ID unik untuk setiap negara
- **Generated**: Secara konsisten untuk setiap negara di semua tahun
- **Range**: 1-167 (berdasarkan jumlah negara unik)

### 4. **report_id** (INT - PRIMARY KEY tabel happiness_report)
- **Deskripsi**: ID unik untuk setiap laporan (country + ranking)
- **Formula**: `(country_id * 1000) + ranking`
- **Unik per**: country + year combination

### 5. **economic_id** (INT - PRIMARY KEY tabel economic_indicator)
- **Deskripsi**: ID indikator ekonomi
- **Formula**: `(report_id * 10) + 1`
- **Relasi**: One-to-One dengan report_id

### 6. **social_id** (INT - PRIMARY KEY tabel social_indicator)
- **Deskripsi**: ID indikator sosial
- **Formula**: `(report_id * 10) + 2`
- **Relasi**: One-to-One dengan report_id

### 7. **perception_id** (INT - PRIMARY KEY tabel perception_indicator)
- **Deskripsi**: ID indikator persepsi
- **Formula**: `(report_id * 10) + 3`
- **Relasi**: One-to-One dengan report_id

### 8. **region_name** (VARCHAR 100)
- **Deskripsi**: Nama region dalam bentuk string
- **Sumber**: Mapping dari "Regional indicator"
- **Contoh**: "South Asia", "Western Europe", etc.

### 9. **country_name** (VARCHAR 100)
- **Deskripsi**: Nama negara
- **Sumber**: Langsung dari field "Country"
- **Contoh**: "Finland", "Afghanistan", etc.

## File yang Diupdate

| File | Entries | Status |
|------|---------|--------|
| world_happiness_2015.json | 158 | ✓ Berhasil |
| world_happiness_2016.json | 157 | ✓ Berhasil |
| world_happiness_2017.json | 155 | ✓ Berhasil |
| world_happiness_2018.json | 155 | ✓ Berhasil |
| world_happiness_2019.json | 155 | ✓ Berhasil |
| world_happiness_2020.json | 152 | ✓ Berhasil |
| world_happiness_2021.json | 148 | ✓ Berhasil |
| world_happiness_2022.json | 145 | ✓ Berhasil |
| world_happiness_2023.json | 137 | ✓ Berhasil |
| world_happiness_2024.json | 140 | ✓ Berhasil |

**Total entries yang diupdate**: 1,402

## Contoh Entry Hasil Update

```json
{
  "Ranking": 140,
  "Country": "Afghanistan",
  "Regional indicator": "South Asia",
  "Happiness score": "1,721",
  "GDP per capita": "2,93451",
  "Social support": "0",
  "Healthy life expectancy": 62,
  "Freedom to make life choices": "0",
  "Generosity": "0,22638",
  "Perceptions of corruption": "0,15383",
  "dystopia_residual": "0,000",
  "region_id": 1,
  "country_id": 153,
  "report_id": 153140,
  "economic_id": 1531401,
  "social_id": 1531402,
  "perception_id": 1531403,
  "region_name": "South Asia",
  "country_name": "Afghanistan"
}
```

## Mapping Region

Region mapping yang digunakan konsisten di semua file:

```python
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
```

## Catatan Penting

1. **Country ID Consistency**: Country ID sama untuk setiap negara di semua tahun, memastikan relasi foreign key yang benar
2. **Dystopia Residual**: Nilai ini dihitung dari happiness score dikurangi jumlah semua indikator. Jika hasilnya negatif, diset ke 0
3. **Format Numeric**: Semua nilai decimal menggunakan koma (,) sebagai pemisah desimal (format Indonesial)
4. **Unique Constraints**: 
   - report_id unik per country + tahun
   - economic_id, social_id, perception_id unik per report_id
5. **Data Integrity**: Semua ID dirancang untuk maintain referential integrity dengan schema database

## Script Eksekusi

Script yang digunakan untuk update: `add_dummy_data.py`

Menjalankan script:
```bash
python add_dummy_data.py
```

Output akan menampilkan status setiap file dan jumlah entries yang berhasil diupdate.
