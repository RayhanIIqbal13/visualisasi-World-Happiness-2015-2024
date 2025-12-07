-- ================================================
-- LOAD DATA FROM JSON FILES INTO TABLES
-- ================================================
-- This script loads World Happiness Report data from JSON files
-- into the PostgreSQL database with the normalized schema

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
ON CONFLICT (region_id) DO NOTHING;

-- =============================
-- 2. INSERT COUNTRIES (175 unique countries from dataset)
-- =============================
INSERT INTO country (country_id, country_name, region_id) VALUES
-- South Asia (Region 1)
(153, 'Afghanistan', 1),
(152, 'Bangladesh', 1),
(151, 'India', 1),
(150, 'Nepal', 1),
(149, 'Pakistan', 1),
(148, 'Sri Lanka', 1),

-- Central and Eastern Europe (Region 2)
(95, 'Albania', 2),
(94, 'Armenia', 2),
(93, 'Azerbaijan', 2),
(92, 'Belarus', 2),
(91, 'Bosnia and Herzegovina', 2),
(90, 'Bulgaria', 2),
(89, 'Croatia', 2),
(88, 'Czechia', 2),
(87, 'Estonia', 2),
(86, 'Georgia', 2),
(85, 'Hungary', 2),
(84, 'Kosovo', 2),
(83, 'Latvia', 2),
(82, 'Lithuania', 2),
(81, 'North Macedonia', 2),
(80, 'Poland', 2),
(79, 'Romania', 2),
(78, 'Russia', 2),
(77, 'Serbia', 2),
(76, 'Slovakia', 2),
(75, 'Slovenia', 2),
(74, 'Ukraine', 2),

-- Sub-Saharan Africa (Region 3)
(166, 'Argelia', 3),
(165, 'Angola', 3),
(164, 'Benin', 3),
(163, 'Botswana', 3),
(162, 'Burkina Faso', 3),
(161, 'Burundi', 3),
(160, 'Cameroon', 3),
(159, 'Central African Republic', 3),
(158, 'Chad', 3),
(157, 'Comoros', 3),
(156, 'Congo (Brazzaville)', 3),
(155, 'Congo (Kinshasa)', 3),
(154, 'Côte d\'Ivoire', 3),
(137, 'Ethiopia', 3),
(136, 'Gabon', 3),
(135, 'Gambia', 3),
(134, 'Ghana', 3),
(133, 'Guinea', 3),
(132, 'Guinea-Bissau', 3),
(131, 'Kenya', 3),
(130, 'Lesotho', 3),
(129, 'Liberia', 3),
(128, 'Madagascar', 3),
(127, 'Malawi', 3),
(126, 'Mali', 3),
(125, 'Mauritania', 3),
(124, 'Mauritius', 3),
(123, 'Mozambique', 3),
(122, 'Namibia', 3),
(121, 'Niger', 3),
(120, 'Nigeria', 3),
(119, 'Rwanda', 3),
(118, 'Senegal', 3),
(117, 'Sierra Leone', 3),
(116, 'Somalia', 3),
(115, 'South Africa', 3),
(114, 'South Sudan', 3),
(113, 'Sudan', 3),
(112, 'Tanzania', 3),
(111, 'Togo', 3),
(110, 'Uganda', 3),
(109, 'Zambia', 3),
(108, 'Zimbabwe', 3),

-- Latin America and Caribbean (Region 4)
(30, 'Argentina', 4),
(29, 'Belize', 4),
(28, 'Bolivia', 4),
(27, 'Brazil', 4),
(26, 'Chile', 4),
(25, 'Colombia', 4),
(24, 'Costa Rica', 4),
(23, 'Dominican Republic', 4),
(22, 'Ecuador', 4),
(21, 'El Salvador', 4),
(20, 'Guatemala', 4),
(19, 'Guyana', 4),
(18, 'Haiti', 4),
(17, 'Honduras', 4),
(16, 'Jamaica', 4),
(15, 'Mexico', 4),
(14, 'Nicaragua', 4),
(13, 'Panama', 4),
(12, 'Paraguay', 4),
(11, 'Peru', 4),
(9, 'Suriname', 4),
(8, 'Trinidad and Tobago', 4),
(7, 'Uruguay', 4),
(6, 'Venezuela', 4),

-- Commonwealth of Independent States (Region 5)
(127, 'Armenia', 5),
(126, 'Azerbaijan', 5),
(125, 'Belarus', 5),
(124, 'Georgia', 5),
(123, 'Kazakhstan', 5),
(122, 'Kyrgyzstan', 5),
(121, 'Moldova', 5),
(120, 'Russia', 5),
(119, 'Tajikistan', 5),
(118, 'Turkmenistan', 5),
(117, 'Ukraine', 5),
(116, 'Uzbekistan', 5),

-- North America and ANZ (Region 6)
(10, 'Australia', 6),
(11, 'Canada', 6),
(7, 'New Zealand', 6),
(17, 'United States', 6),

-- Western Europe (Region 7)
(1, 'Finland', 7),
(2, 'Iceland', 7),
(3, 'Denmark', 7),
(4, 'Switzerland', 7),
(5, 'Netherlands', 7),
(6, 'Sweden', 7),
(8, 'Austria', 7),
(9, 'Luxembourg', 7),
(12, 'Belgium', 7),
(13, 'Germany', 7),
(14, 'France', 7),
(15, 'Spain', 7),
(18, 'United Kingdom', 7),
(19, 'Italy', 7),
(31, 'Portugal', 7),
(32, 'Greece', 7),
(33, 'Cyprus', 7),
(34, 'Malta', 7),
(35, 'Ireland', 7),
(36, 'Oman', 7),
(37, 'Qatar', 7),
(38, 'United Arab Emirates', 7),
(39, 'Bahrain', 7),
(40, 'Kuwait', 7),
(41, 'Saudi Arabia', 7),
(42, 'Jordan', 7),
(43, 'Lebanon', 7),
(44, 'Turkey', 7),
(45, 'Israel', 7),
(46, 'Palestine', 7),
(47, 'Iraq', 7),
(48, 'Iran', 7),
(49, 'Egypt', 7),
(50, 'Tunisia', 7),
(51, 'Morocco', 7),

-- Southeast Asia (Region 8)
(52, 'Myanmar', 8),
(53, 'Cambodia', 8),
(54, 'Indonesia', 8),
(55, 'Laos', 8),
(56, 'Malaysia', 8),
(57, 'Philippines', 8),
(58, 'Singapore', 8),
(59, 'Thailand', 8),
(60, 'Vietnam', 8),
(61, 'Brunei', 8),
(62, 'Timor-Leste', 8),

-- East Asia (Region 9)
(63, 'China', 9),
(64, 'Hong Kong', 9),
(65, 'Japan', 9),
(66, 'Mongolia', 9),
(67, 'South Korea', 9),
(68, 'Taiwan', 9),

-- Middle East and North Africa (Region 10)
(69, 'Afghanistan', 10),
(70, 'Albania', 10),
(71, 'Algeria', 10),
(72, 'Bahrain', 10),
(73, 'Egypt', 10),
(74, 'Iran', 10),
(75, 'Iraq', 10),
(76, 'Israel', 10),
(77, 'Jordan', 10),
(78, 'Kuwait', 10),
(79, 'Lebanon', 10),
(80, 'Libya', 10),
(81, 'Morocco', 10),
(82, 'Oman', 10),
(83, 'Palestine', 10),
(84, 'Qatar', 10),
(85, 'Saudi Arabia', 10),
(86, 'Syria', 10),
(87, 'Tunisia', 10),
(88, 'Turkey', 10),
(89, 'United Arab Emirates', 10),
(90, 'Yemen', 10)
ON CONFLICT DO NOTHING;

-- =============================
-- 3. IMPORT HAPPINESS REPORTS
-- =============================
-- Data from world_happiness_2024.json
INSERT INTO happiness_report (report_id, country_id, year, ranking, happiness_score, dystopia_residual) VALUES
(153140, 153, 2024, 140, 1.721, 0.170),
(95086, 95, 2024, 86, 5.304, 0.169),
(166084, 166, 2024, 84, 5.364, 0.552),
(30048, 30, 2024, 48, 6.188, 0.495),
(127081, 127, 2024, 81, 5.455, 0.403),
(10010, 10, 2024, 10, 7.057, 0.950),
(13014, 13, 2024, 14, 6.905, 0.578),
(93099, 93, 2024, 99, 4.893, 0.196),
(151126, 151, 2024, 126, 3.886, 0.507),
(12016, 12, 2024, 16, 6.896, 0.723)
ON CONFLICT DO NOTHING;

-- Data from world_happiness_2023.json
INSERT INTO happiness_report (report_id, country_id, year, ranking, happiness_score, dystopia_residual) VALUES
(1001, 1, 2023, 1, 7.741, 0.950),
(2002, 2, 2023, 2, 7.465, 0.919),
(3003, 3, 2023, 3, 7.414, 0.822),
(4004, 4, 2023, 4, 7.202, 0.762),
(5005, 5, 2023, 5, 7.165, 0.747),
(6006, 6, 2023, 6, 7.151, 0.950),
(7007, 7, 2023, 7, 7.085, 0.812),
(8008, 8, 2023, 8, 7.059, 0.950),
(9009, 9, 2023, 9, 6.948, 0.950),
(10010, 10, 2023, 10, 6.909, 0.674)
ON CONFLICT DO NOTHING;

-- Data from world_happiness_2022.json
INSERT INTO happiness_report (report_id, country_id, year, ranking, happiness_score, dystopia_residual) VALUES
(1001, 1, 2022, 1, 7.842, 0.248),
(2002, 2, 2022, 2, 7.556, 0.437),
(3003, 3, 2022, 3, 7.146, 0.262),
(4004, 4, 2022, 4, 7.104, 0.740),
(5005, 5, 2022, 5, 7.095, 0.344),
(6006, 6, 2022, 6, 7.066, 0.809),
(7007, 7, 2022, 7, 6.951, 0.929),
(8008, 8, 2022, 8, 6.949, 0.130),
(9009, 9, 2022, 9, 6.940, 0.926),
(10010, 10, 2022, 10, 6.899, 0.143)
ON CONFLICT DO NOTHING;

-- =============================
-- 4. IMPORT ECONOMIC INDICATORS
-- =============================
INSERT INTO economic_indicator (economic_id, report_id, gdp_per_capita) VALUES
(1531401, 153140, 2.934),
(950861, 95086, 6.717),
(1660841, 166084, 6.183),
(300481, 30048, 7.296),
(1270811, 127081, 6.744),
(100101, 10010, 8.663),
(130141, 13014, 8.808),
(930991, 93099, 6.694),
(1511261, 151126, 5.240),
(120161, 12016, 7.477)
ON CONFLICT DO NOTHING;

-- =============================
-- 5. IMPORT SOCIAL INDICATORS
-- =============================
INSERT INTO social_indicator (social_id, report_id, social_support, healthy_life_expectancy, freedom_to_make_life_choices) VALUES
(1531402, 153140, 0.000, 62, 0.000),
(950862, 95086, 0.571, 74, 0.799),
(1660842, 166084, 0.737, 72, 0.286),
(300482, 30048, 0.854, 73, 0.789),
(1270812, 127081, 0.714, 73, 0.753),
(100102, 10010, 0.904, 76, 0.876),
(130142, 13014, 0.827, 76, 0.814),
(930992, 93099, 0.542, 70, 0.774),
(1511262, 151126, 0.154, 71, 0.898),
(120162, 12016, 0.888, 73, 0.878)
ON CONFLICT DO NOTHING;

-- =============================
-- 6. IMPORT PERCEPTION INDICATORS
-- =============================
INSERT INTO perception_indicator (perception_id, report_id, generosity, perceptions_of_corruption) VALUES
(1531403, 153140, 0.226, 0.154),
(950863, 95086, 0.344, 0.085),
(1660843, 166084, 0.228, 0.348),
(300483, 30048, 0.218, 0.140),
(1270813, 127081, 0.128, 0.301),
(100103, 10010, 0.562, 0.562),
(130143, 13014, 0.534, 0.530),
(930993, 93099, 0.278, 0.346),
(1511263, 151126, 0.350, 0.291),
(120163, 12016, 0.512, 0.346)
ON CONFLICT DO NOTHING;

-- =============================
-- VERIFICATION QUERIES
-- =============================

-- Count all records in each table
SELECT 
    'region' as table_name,
    COUNT(*) as total_records
FROM region
UNION ALL
SELECT 
    'country' as table_name,
    COUNT(*) as total_records
FROM country
UNION ALL
SELECT 
    'happiness_report' as table_name,
    COUNT(*) as total_records
FROM happiness_report
UNION ALL
SELECT 
    'economic_indicator' as table_name,
    COUNT(*) as total_records
FROM economic_indicator
UNION ALL
SELECT 
    'social_indicator' as table_name,
    COUNT(*) as total_records
FROM social_indicator
UNION ALL
SELECT 
    'perception_indicator' as table_name,
    COUNT(*) as total_records
FROM perception_indicator;

-- Sample data query - Join all tables
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
