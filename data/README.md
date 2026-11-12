# Real source data: Rwanda administrative units

**Source:** Open Admin Data, *Rwanda administrative divisions* GitHub repository. https://github.com/open-admin-data/rwanda-administrative-divisions
**Upstream source files:** `data/all-province.json`, `data/all-district.json`, `data/all-sector.json` (default branch as read on 11 November 2026). License shown in upstream country-data file header: **CC-BY-4.0**; re-check repository licensing at delivery.
**Extracted:** 451 records (5 province-level units, 30 districts, 416 sectors) from upstream JSON. 0 duplicate IDs; 0 broken parent references in 451 records; fields `id,level,name,parent_id,latitude,longitude,source_file`.
**Method:** for each source JSON object, select `id`, `level`, `name.en` (fallback `name.local`), `parent.id` (blank for province), `geo.lat`, `geo.lon` and source filename. Write one CSV row per upstream object. The files `provinces.csv`, `districts.csv`, and `sectors.csv` are derived subsets.
**License notice:** CC BY 4.0 attribution must be maintained. Source repo https://github.com/open-admin-data/rwanda-administrative-divisions. These are third-party public geographies, not our invented records. No real persons are included.
**Data caveats:** The dataset is at sector level only; there are NO cells or villages in the packaged file. A complete public emergency lookup below sector level would require additional verified reference data and freshness checks. Coordinates require independent geospatial validation before any real operational routing use. Administrative structure may change.

### Sample records
```
RW1,1,Kigali City,, -1.957,30.103,data/all-province.json
RW12,2,Gasabo,RW1,-1.884,30.133,data/all-district.json
RW3304,3,Gisenyi,RW33,-1.691,29.259,data/all-sector.json
```

### Reproducibility
The upstream JSON collection is publicly addressable in the linked repository. See `database/phase0_geo_import.sql` for SQL*Loader external CSV staging and 3NF destination ideas for Phase II. Keep `source_file` and source URL as lineage. Data was inspected for IDs and parental integrity; no external accuracy guarantees are implied.
