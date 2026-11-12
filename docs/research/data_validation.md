# Real dataset audit - 11 November 2026

- Dataset: Open Admin Data Rwanda administrative divisions (`all-province.json`, `all-district.json`, `all-sector.json`).
- Source URL: https://github.com/open-admin-data/rwanda-administrative-divisions
- Downloadable CSV package: `data/rwanda_administrative_units_451.csv`
- Total records: **451**, provinces/province-level **5**, districts **30**, sectors **416**.
- Distinct IDs **451**; duplicate IDs **0**.
- Parent reference integrity: **0 missing parents** for all districts and sectors.
- Population: administrative geography only; **no identifying data about persons**.
- License as displayed by upstream country-data file: CC BY 4.0. Attribution required.
- Risk: coordinates are not externally verified; do not treat as precise real-time locations.
- Risk: geographical coverage excludes cells and villages; not operationally sufficient for final citizen emergency lookup at village precision.
- World Bank geography was assessed but its source ZIP was NOT ingested. Therefore this phase uses the Open Admin Data licensed dataset, not a World Bank dataset.
- Sector and district codes form a stable development key only relative to this particular source snapshot. Changes require a source-edition column or migration mapping.

## Test queries for Oracle
- `SELECT COUNT(*) FROM source_admin_unit;` should yield 451.
- `SELECT level_no, COUNT(*) FROM source_admin_unit GROUP BY level_no ORDER BY level_no;` should yield 1:5, 2:30, 3:416.
- A parent-validation query should show zero children without a parent match.
