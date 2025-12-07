-- ================================================
-- SCRIPT UNTUK LOAD DATA DARI JSON KE DATABASE
-- ================================================
-- Script ini membantu Anda memahami bagaimana data dari JSON
-- seharusnya di-insert ke tabel database sesuai schema

-- ================================================
-- 1. POPULATE TABEL REGION (dari region_id mapping)
-- ================================================

INSERT INTO region (region_id, region_name, regional_indicator) VALUES
(1, 'South Asia', 'South Asia'),
(2, 'Central and Eastern Europe', 'Central and Eastern Europe'),
(3, 'Sub-Saharan Africa', 'Sub-Saharan Africa'),
(4, 'Latin America and Caribbean', 'Latin America and Caribbean'),
(5, 'Commonwealth of Independent States', 'Commonwealth of Independent States'),
(6, 'North America and ANZ', 'North America and ANZ'),
(7, 'Western Europe', 'Western Europe'),
(8, 'Southeast Asia', 'Southeast Asia'),
(9, 'East Asia', 'East Asia'),
(10, 'Middle East and North Africa', 'Middle East and North Africa');

-- ================================================
-- 2. POPULATE TABEL COUNTRY (dari JSON data)
-- ================================================
-- Catatan: Pastikan country_id sesuai dengan yang di JSON

-- Contoh beberapa entries:
INSERT INTO country (country_id, country_name, region_id) VALUES
(1, 'Switzerland', 7),
(2, 'Iceland', 7),
(3, 'Denmark', 7),
(4, 'Sweden', 7),
(5, 'Israel', 10),
(6, 'Netherlands', 7),
(7, 'Norway', 7),
(8, 'Luxembourg', 7),
(9, 'Switzerland', 7),
(10, 'Australia', 6),
-- ... lanjutkan dengan semua negara dari JSON

-- ================================================
-- 3. POPULATE TABEL HAPPINESS_REPORT
-- ================================================
-- Mapping dari JSON entries:
/*
Contoh structure dari JSON:
{
  "Ranking": 1,
  "Country": "Finland",
  "Happiness score": "7,7407",
  "dystopia_residual": "0,000",
  "country_id": 28,
  "report_id": 28001,
  "year": 2024
}

INSERT ke happiness_report:
*/

INSERT INTO happiness_report (report_id, country_id, year, ranking, happiness_score, dystopia_residual) VALUES
-- Finland 2024
(28001, 28, 2024, 1, 7.7407, 0.000),
-- Denmark 2024
(3009, 3, 2024, 2, 7.5827, 0.000),
-- Iceland 2024
(2003, 2, 2024, 3, 7.5251, 0.000);

-- ================================================
-- 4. POPULATE TABEL ECONOMIC_INDICATOR
-- ================================================
-- Mapping dari JSON:
/*
{
  "GDP per capita": "8,61498",
  "economic_id": 280011,
  "report_id": 28001
}
*/

INSERT INTO economic_indicator (economic_id, report_id, gdp_per_capita) VALUES
-- Finland 2024
(280011, 28001, 8.61498),
-- Denmark 2024
(30091, 3009, 8.91278),
-- Iceland 2024
(20031, 2003, 8.78627);

-- ================================================
-- 5. POPULATE TABEL SOCIAL_INDICATOR
-- ================================================
-- Mapping dari JSON:
/*
{
  "Social support": "0,97268",
  "Healthy life expectancy": 76,
  "Freedom to make life choices": "0,99532",
  "social_id": 280012,
  "report_id": 28001
}
*/

INSERT INTO social_indicator (social_id, report_id, social_support, healthy_life_expectancy, freedom_to_make_life_choices) VALUES
-- Finland 2024
(280012, 28001, 0.97268, 76, 0.99532),
-- Denmark 2024
(30092, 3009, 0.94051, 76, 0.95298),
-- Iceland 2024
(20032, 2003, 1.0, 77, 0.94808);

-- ================================================
-- 6. POPULATE TABEL PERCEPTION_INDICATOR
-- ================================================
-- Mapping dari JSON:
/*
{
  "Generosity": "0,35347",
  "Perceptions of corruption": "0,94966",
  "perception_id": 280013,
  "report_id": 28001
}
*/

INSERT INTO perception_indicator (perception_id, report_id, generosity, perceptions_of_corruption) VALUES
-- Finland 2024
(280013, 28001, 0.35347, 0.94966),
-- Denmark 2024
(30093, 3009, 0.50792, 0.95358),
-- Iceland 2024
(20033, 2003, 0.64455, 0.31728);

-- ================================================
-- QUERY UNTUK VERIFY DATA
-- ================================================

-- 1. Check data di REGION
SELECT * FROM region;

-- 2. Check data di COUNTRY
SELECT * FROM country WHERE country_id IN (1,2,3,28);

-- 3. Check data di HAPPINESS_REPORT dengan JOIN
SELECT 
  hr.report_id,
  c.country_name,
  r.region_name,
  hr.year,
  hr.ranking,
  hr.happiness_score,
  hr.dystopia_residual
FROM happiness_report hr
JOIN country c ON hr.country_id = c.country_id
JOIN region r ON c.region_id = r.region_id
ORDER BY hr.year DESC, hr.ranking ASC;

-- 4. Check complete data dengan semua indikator
SELECT 
  c.country_name,
  r.region_name,
  hr.year,
  hr.ranking,
  hr.happiness_score,
  hr.dystopia_residual,
  ei.gdp_per_capita,
  si.social_support,
  si.healthy_life_expectancy,
  si.freedom_to_make_life_choices,
  pi.generosity,
  pi.perceptions_of_corruption
FROM happiness_report hr
JOIN country c ON hr.country_id = c.country_id
JOIN region r ON c.region_id = r.region_id
LEFT JOIN economic_indicator ei ON hr.report_id = ei.report_id
LEFT JOIN social_indicator si ON hr.report_id = si.report_id
LEFT JOIN perception_indicator pi ON hr.report_id = pi.report_id
WHERE hr.year = 2024
ORDER BY hr.ranking ASC;

-- ================================================
-- NOTES UNTUK DATA LOADING
-- ================================================

/*
PENTING SAAT LOAD DATA:

1. ORDER LOADING:
   - Load REGION terlebih dahulu (no dependencies)
   - Load COUNTRY (depends on REGION)
   - Load HAPPINESS_REPORT (depends on COUNTRY)
   - Load ECONOMIC_INDICATOR (depends on HAPPINESS_REPORT)
   - Load SOCIAL_INDICATOR (depends on HAPPINESS_REPORT)
   - Load PERCEPTION_INDICATOR (depends on HAPPINESS_REPORT)

2. DATA CONVERSION:
   - JSON menggunakan format decimal dengan koma (,) sebagai separator
   - Database menggunakan titik (.) sebagai separator
   - Contoh: "8,61498" → 8.61498

3. YEAR FIELD:
   - Year dapat diambil dari nama file JSON
   - 2015-2024 berdasarkan filename

4. CONSTRAINT HANDLING:
   - UNIQUE constraint pada (country_id, year) di happiness_report
   - UNIQUE constraint pada report_id di economic_indicator, social_indicator, perception_indicator
   - Ensure tidak ada duplicate entries

5. FOREIGN KEY VERIFICATION:
   - Semua country_id harus exist di tabel country
   - Semua region_id harus exist di tabel region
   - Semua report_id harus exist di tabel happiness_report sebelum insert ke indicator tables

6. BULK INSERT OPTIMIZATION:
   - Disable indexes sebelum bulk insert
   - Batch insert dengan COMMIT interval
   - Re-enable indexes setelah selesai
   - Run ANALYZE untuk update statistics

CONTOH BULK INSERT:
   BEGIN TRANSACTION;
   -- Disable triggers dan constraints jika perlu
   -- INSERT dari JSON ke tables
   -- COMMIT;
*/
