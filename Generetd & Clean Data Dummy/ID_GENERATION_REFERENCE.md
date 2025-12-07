# 🔑 ID Generation & Mapping Reference

## Overview

Semua ID yang ditambahkan dalam dummy data mengikuti pattern yang konsisten dan deterministic, memastikan data integrity dan mendukung relational integrity di database.

---

## Region ID Mapping

### Full Mapping Table

| Region ID | Region Name | Regional Indicator | Characteristics |
|-----------|-------------|-------------------|-----------------|
| 1 | South Asia | South Asia | Developing economies, large populations |
| 2 | Central and Eastern Europe | Central and Eastern Europe | Transition economies, EU members |
| 3 | Sub-Saharan Africa | Sub-Saharan Africa | Diverse development levels |
| 4 | Latin America and Caribbean | Latin America and Caribbean | Mixed income countries |
| 5 | Commonwealth of Independent States | Commonwealth of Independent States | Post-Soviet countries |
| 6 | North America and ANZ | North America and ANZ | Developed, high-income |
| 7 | Western Europe | Western Europe | Most developed, highest happiness |
| 8 | Southeast Asia | Southeast Asia | Growing economies, ASEAN region |
| 9 | East Asia | East Asia | Major Asian economies |
| 10 | Middle East and North Africa | Middle East and North Africa | Oil-rich and developing nations |

---

## Country ID Structure

### Assignment Logic

```
Each country receives a UNIQUE country_id that:
- Is assigned sequentially (1, 2, 3, ...)
- REMAINS CONSISTENT across all years (2015-2024)
- Is based on first appearance in data
- Enables year-over-year comparison
- Maintains referential integrity
```

### Example Country IDs

| Country | Region | Country ID | Reason |
|---------|--------|-----------|--------|
| Switzerland | Western Europe | 1 | First in 2015 data |
| Iceland | Western Europe | 2 | Second in data |
| Denmark | Western Europe | 3 | Third in data |
| Sweden | Western Europe | 4 | Fourth in data |
| ... | ... | ... | ... |
| Finland | Western Europe | 28 | Ranked #1 in 2024 |
| Afghanistan | South Asia | 153 | Lowest ranking countries |

### Key Characteristics

✅ **Immutability**: Same country = same ID always
✅ **Global**: ID is consistent across all 10 years
✅ **Predictable**: Based on first data appearance
✅ **Unique**: No two countries share an ID
✅ **References**: Used as FK in multiple tables

---

## Report ID Structure

### Generation Formula

```
report_id = (country_id × 1000) + ranking

Example:
- Finland (country_id=28) with Ranking=1 in 2024
  report_id = (28 × 1000) + 1 = 28001

- Sweden (country_id=4) with Ranking=7 in 2024
  report_id = (4 × 1000) + 7 = 4007
```

### Properties

| Property | Value |
|----------|-------|
| Range | 1001 - 160140 |
| Format | (CCC)RRR where CCC=country_id, RRR=ranking |
| Uniqueness | Unique per country per year |
| Generation | Deterministic, reproducible |
| Sortability | Hierarchical (country_id groups) |

### Examples by Year

#### Finland (country_id=28)
| Year | Ranking | report_id |
|------|---------|-----------|
| 2015 | 5 | 28005 |
| 2016 | 4 | 28004 |
| 2017 | 5 | 28005 |
| 2020 | 1 | 28001 |
| 2024 | 1 | 28001 |

#### Switzerland (country_id=1)
| Year | Ranking | report_id |
|------|---------|-----------|
| 2015 | 1 | 1001 |
| 2016 | 1 | 1001 |
| 2017 | 1 | 1001 |
| 2020 | 3 | 1003 |
| 2024 | 9 | 1009 |

---

## Indicator ID Structure

### Economic Indicator ID (economic_id)

```
economic_id = (report_id × 10) + 1

Example:
- Finland 2024 (report_id=28001)
  economic_id = (28001 × 10) + 1 = 280011

- Switzerland 2024 (report_id=1009)
  economic_id = (1009 × 10) + 1 = 10091
```

**Purpose**: Reference to economic_indicator table (GDP per capita)

### Social Indicator ID (social_id)

```
social_id = (report_id × 10) + 2

Example:
- Finland 2024 (report_id=28001)
  social_id = (28001 × 10) + 2 = 280012

- Switzerland 2024 (report_id=1009)
  social_id = (1009 × 10) + 2 = 10092
```

**Purpose**: Reference to social_indicator table (social support, life expectancy, freedom)

### Perception Indicator ID (perception_id)

```
perception_id = (report_id × 10) + 3

Example:
- Finland 2024 (report_id=28001)
  perception_id = (28001 × 10) + 3 = 280013

- Switzerland 2024 (report_id=1009)
  perception_id = (1009 × 10) + 3 = 10093
```

**Purpose**: Reference to perception_indicator table (generosity, corruption perception)

---

## ID Uniqueness Constraints

### Primary Keys (Unique)

| Field | Uniqueness Scope | Usage |
|-------|-----------------|-------|
| `region_id` | Global | Identify regions |
| `country_id` | Global | Identify countries |
| `report_id` | Per country per year | Identify happiness reports |
| `economic_id` | Per report | One-to-one with report |
| `social_id` | Per report | One-to-one with report |
| `perception_id` | Per report | One-to-one with report |

### Composite Unique Keys

| Composite | Scope | Example |
|-----------|-------|---------|
| (country_id, year) | Global | (28, 2024) = Finland 2024 |
| (region_id, country_id) | Global | (7, 28) = Western Europe, Finland |

---

## Relationship Diagram

```
REGION (region_id PK)
  ↓
COUNTRY (country_id PK, region_id FK)
  ↓
HAPPINESS_REPORT (report_id PK, country_id FK, year)
  ├─→ ECONOMIC_INDICATOR (economic_id PK, report_id FK 1:1)
  ├─→ SOCIAL_INDICATOR (social_id PK, report_id FK 1:1)
  └─→ PERCEPTION_INDICATOR (perception_id PK, report_id FK 1:1)
```

---

## ID Assignment Example

### Scenario: Adding Finland 2024 Record

Step 1: Lookup region
```
Regional indicator: "Western Europe"
→ region_id = 7
```

Step 2: Lookup country
```
Country: "Finland"
→ country_id = 28 (from mapping)
```

Step 3: Calculate report_id
```
Ranking: 1
→ report_id = (28 × 1000) + 1 = 28001
```

Step 4: Calculate indicator IDs
```
→ economic_id = (28001 × 10) + 1 = 280011
→ social_id = (28001 × 10) + 2 = 280012
→ perception_id = (28001 × 10) + 3 = 280013
```

Step 5: Get region name and country name
```
region_name = "Western Europe"
country_name = "Finland"
```

**Result**: Complete entry with all IDs assigned

---

## ID Range Statistics

### By Category

| Category | Min | Max | Count |
|----------|-----|-----|-------|
| region_id | 1 | 10 | 10 |
| country_id | 1 | ~167 | ~167 |
| report_id | 1001 | 160140 | ~1,402 |
| economic_id | 10011 | 1601401 | ~1,402 |
| social_id | 10012 | 1601402 | ~1,402 |
| perception_id | 10013 | 1601403 | ~1,402 |

### Distribution by Region

| Region | Country Count | Report Count |
|--------|---------------|--------------|
| South Asia | ~8 | ~95 |
| Central & Eastern Europe | ~20 | ~245 |
| Sub-Saharan Africa | ~50 | ~510 |
| Latin America & Caribbean | ~25 | ~280 |
| Commonwealth of Independent States | ~12 | ~110 |
| North America & ANZ | ~4 | ~40 |
| Western Europe | ~25 | ~280 |
| Southeast Asia | ~12 | ~125 |
| East Asia | ~8 | ~85 |
| Middle East & North Africa | ~20 | ~232 |

---

## Query Examples

### Find All Reports for a Country

```sql
-- Get Finland (country_id = 28) reports across all years
SELECT report_id, year, ranking, happiness_score 
FROM happiness_report 
WHERE country_id = 28 
ORDER BY year;

-- Result:
-- report_id | year | ranking | happiness_score
-- 28005     | 2015 |    5    | 7.4689
-- 28004     | 2016 |    4    | 7.4869
-- 28005     | 2017 |    5    | 7.4690
-- 28001     | 2020 |    1    | 7.8091
-- 28001     | 2024 |    1    | 7.7407
```

### Find All Indicators for a Report

```sql
-- Get all indicators for Finland 2024 (report_id = 28001)
SELECT 
  ei.gdp_per_capita,
  si.social_support,
  si.healthy_life_expectancy,
  pi.generosity,
  pi.perceptions_of_corruption
FROM economic_indicator ei
JOIN social_indicator si ON ei.report_id = si.report_id
JOIN perception_indicator pi ON ei.report_id = pi.report_id
WHERE ei.report_id = 28001;
```

### Countries by Region

```sql
-- Count countries in each region
SELECT r.region_id, r.region_name, COUNT(DISTINCT c.country_id) as country_count
FROM region r
LEFT JOIN country c ON r.region_id = c.region_id
GROUP BY r.region_id, r.region_name
ORDER BY r.region_id;
```

---

## Migration Notes

### When Importing to Database

1. **Preserve Region IDs**: Must match the mapping exactly
2. **Preserve Country IDs**: Critical for maintaining relationships
3. **Report IDs**: Will be consistent only if ranking data is same
4. **Year Information**: Add year field during import from filename
5. **Decimal Format**: Convert "8,61498" → 8.61498

---

## Validation Queries

Run these to verify ID integrity:

```sql
-- 1. Check for duplicate country_ids
SELECT country_id, COUNT(*) as cnt 
FROM country 
GROUP BY country_id 
HAVING COUNT(*) > 1;

-- 2. Check for orphaned reports
SELECT hr.report_id, hr.country_id 
FROM happiness_report hr 
WHERE NOT EXISTS (SELECT 1 FROM country c WHERE c.country_id = hr.country_id);

-- 3. Check for orphaned indicators
SELECT ei.economic_id, ei.report_id 
FROM economic_indicator ei 
WHERE NOT EXISTS (SELECT 1 FROM happiness_report hr WHERE hr.report_id = ei.report_id);

-- 4. Verify region coverage
SELECT DISTINCT region_id FROM country ORDER BY region_id;

-- 5. Count reports per year
SELECT EXTRACT(YEAR FROM DATE '2024-01-01'), COUNT(*) 
FROM happiness_report 
GROUP BY year 
ORDER BY year;
```

---

## Performance Considerations

### Index Strategy

```sql
-- Create indexes for fast lookups
CREATE INDEX idx_country_country_id ON country(country_id);
CREATE INDEX idx_country_region_id ON country(region_id);
CREATE INDEX idx_report_country_id ON happiness_report(country_id);
CREATE INDEX idx_report_year ON happiness_report(year);
CREATE INDEX idx_econ_report_id ON economic_indicator(report_id);
CREATE INDEX idx_social_report_id ON social_indicator(report_id);
CREATE INDEX idx_perception_report_id ON perception_indicator(report_id);
```

### Query Optimization

- Use country_id for fast joins
- Filter by year for annual reports
- Use report_id for indicator lookups
- Batch operations for bulk imports

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-12  
**Status**: Complete ✅
