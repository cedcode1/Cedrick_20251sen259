-- PHASE 0 REFERENCE SQL (NOT YET EXECUTED IN ORACLE)
-- Data file: data/rwanda_administrative_units_451.csv
-- Phase II will normalize these into province, district and sector.
CREATE TABLE source_admin_unit (
  geo_id VARCHAR2(10) PRIMARY KEY,
  level_no NUMBER(1) NOT NULL CHECK (level_no BETWEEN 1 AND 3),
  geo_name VARCHAR2(120) NOT NULL,
  parent_geo_id VARCHAR2(10),
  latitude NUMBER(10,6),
  longitude NUMBER(10,6),
  source_file VARCHAR2(100),
  CONSTRAINT fk_geo_parent FOREIGN KEY(parent_geo_id) REFERENCES source_admin_unit(geo_id)
);
-- Import using SQL Developer CSV import or SQL*Loader (parent-first order: province, district, sector).
-- Validation after import:
SELECT COUNT(*) total_rows FROM source_admin_unit;
SELECT level_no, COUNT(*) total_rows FROM source_admin_unit GROUP BY level_no ORDER BY level_no;
SELECT COUNT(*) missing_parents FROM source_admin_unit c
WHERE c.parent_geo_id IS NOT NULL AND NOT EXISTS
 (SELECT 1 FROM source_admin_unit p WHERE p.geo_id = c.parent_geo_id);
-- Targets: 451; [5,30,416]; 0 missing parents.
