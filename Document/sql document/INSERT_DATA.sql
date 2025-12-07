-- ================================================
-- INSERT DATA INTO WORLD HAPPINESS REPORT DATABASE
-- ================================================

-- =============================
-- 1. INSERT REGIONS
-- =============================
INSERT INTO region (region_id, region_name) VALUES
(1, 'South Asia'),
(2, 'Central and Eastern Europe'),
(3, 'Sub-Saharan Africa'),
(4, 'Latin America and Caribbean'),
(5, 'Commonwealth of Independent States'),
(6, 'North America and ANZ'),
(7, 'Western Europe'),
(8, 'Southeast Asia'),
(9, 'East Asia'),
(10, 'Middle East and North Africa')
ON CONFLICT DO NOTHING;

-- =============================
-- 2. INSERT COUNTRIES (Sample)
-- =============================
-- Note: Full country list will be generated from JSON data via Python script
-- This shows the structure for manual entry if needed

INSERT INTO country (country_id, country_name, region_id) VALUES
(1, 'Finland', 7),
(2, 'Iceland', 7),
(3, 'Denmark', 7),
(4, 'Switzerland', 7),
(5, 'Netherlands', 7),
(6, 'Sweden', 7),
(7, 'New Zealand', 6),
(8, 'Austria', 7),
(9, 'Luxembourg', 7),
(10, 'Australia', 6),
(11, 'Canada', 6),
(12, 'United Kingdom', 7),
(13, 'Germany', 7),
(14, 'Belgium', 7),
(15, 'France', 7),
(16, 'Czechia', 2),
(17, 'United States', 6),
(18, 'Spain', 7),
(19, 'Italy', 7),
(20, 'Japan', 9)
ON CONFLICT DO NOTHING;

-- =============================
-- 3. SAMPLE DATA VERIFICATION QUERY
-- =============================

-- Count all inserted data
SELECT 
    'Regions' as table_name,
    COUNT(*) as total_records
FROM region
UNION ALL
SELECT 
    'Countries' as table_name,
    COUNT(*) as total_records
FROM country
UNION ALL
SELECT 
    'Happiness Reports' as table_name,
    COUNT(*) as total_records
FROM happiness_report
UNION ALL
SELECT 
    'Economic Indicators' as table_name,
    COUNT(*) as total_records
FROM economic_indicator
UNION ALL
SELECT 
    'Social Indicators' as table_name,
    COUNT(*) as total_records
FROM social_indicator
UNION ALL
SELECT 
    'Perception Indicators' as table_name,
    COUNT(*) as total_records
FROM perception_indicator;

-- Show sample data
SELECT 
    c.country_name,
    r.region_name,
    hr.year,
    hr.ranking,
    ROUND(CAST(hr.happiness_score AS NUMERIC), 3) as happiness_score,
    ROUND(CAST(ei.gdp_per_capita AS NUMERIC), 3) as gdp_per_capita,
    ROUND(CAST(si.social_support AS NUMERIC), 3) as social_support,
    ROUND(CAST(si.healthy_life_expectancy AS NUMERIC), 3) as life_expectancy,
    ROUND(CAST(si.freedom_to_make_life_choices AS NUMERIC), 3) as freedom,
    ROUND(CAST(pi.generosity AS NUMERIC), 3) as generosity,
    ROUND(CAST(pi.perceptions_of_corruption AS NUMERIC), 3) as corruption
FROM happiness_report hr
JOIN country c ON hr.country_id = c.country_id
JOIN region r ON c.region_id = r.region_id
JOIN economic_indicator ei ON hr.report_id = ei.report_id
JOIN social_indicator si ON hr.report_id = si.report_id
JOIN perception_indicator pi ON hr.report_id = pi.report_id
ORDER BY hr.year DESC, hr.ranking ASC
LIMIT 20;
