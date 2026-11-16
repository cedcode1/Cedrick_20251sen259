# Phase II — Normalization (UNF → 1NF → 2NF → 3NF)

## Raw source and grain
Five unchanged JSON files in `data/raw/provinces/` contain `provinces[] → districts[] → sectors[] → cells[] → villages[]`. In total: 5 provinces, 30 districts, 416 sectors, 2,142 cells, 14,816 villages (**17,409** real administrative objects). The source is a 2019 NISR-derived edition redistributed by rwanda-admin. This model covers *real geography only*. No real officer or duty records occur in the raw files.

The examples below are actual values in the raw JSON. The temporary `row_no` used to demonstrate 1NF/2NF is an ordinal generated during reading in each physical source file; it is **not** an original JSON field.

## UNF — Unnormalized Form

A raw province object contains a **repeating list** of districts; districts contain a list of sectors; sectors contain cells; cells contain villages. The nested lists are not atomic values in a single relational row.

| Source province record (actual name) | District array | Typical further nested repetition |
|---|---:|---|
| Umujyi wa Kigali | 3 district objects | districts→sectors→cells→villages |
| Amajyaruguru | 5 district objects | districts→sectors→cells→villages |
| Amajyepfo | 8 district objects | districts→sectors→cells→villages |
| Iburasirazuba | 7 district objects | districts→sectors→cells→villages |
| Iburengerazuba | 7 district objects | districts→sectors→cells→villages |

**Dependency/issue:** repeating groups (`districts[]`, `sectors[]`, `cells[]`, `villages[]`) are embedded inside parent records. This is UNF.

## 1NF — One value per field, one village per row

For a clear intermediate example, traverse each nested province file in the original order and produce one *temporary wide row per village*. All columns contain individual values; no column contains an array. A valid **staging composite key** is `(source_file, row_no)` because `row_no` restarts at 1 within each source file. This composite key identifies the staging observation; the source's `village_id` is also globally unique.

| source_file (short form) | row_no | Province | District | Sector | Cell | village_id | Village | nep |
|---|---:|---|---|---|---|---|---|---|
| umujyi-wa-kigali.json | 1 | Umujyi wa Kigali | Nyarugenge | Gitega | Akabahizi | village-11010102 | Gihanga | GE |
| umujyi-wa-kigali.json | 2 | Umujyi wa Kigali | Nyarugenge | Gitega | Akabahizi | village-11010103 | Iterambere | GE |
| umujyi-wa-kigali.json | 3 | Umujyi wa Kigali | Nyarugenge | Gitega | Akabahizi | village-11010104 | Izuba | GE |
| umujyi-wa-kigali.json | 4 | Umujyi wa Kigali | Nyarugenge | Gitega | Akabahizi | village-11010105 | Nyaburanga | GE |
| umujyi-wa-kigali.json | 5 | Umujyi wa Kigali | Nyarugenge | Gitega | Akabahizi | village-11010106 | Nyenyeri | GE |

**Dependency removed:** repeating groups are unfolded into atomic rows. The field values themselves are unchanged. Names repeat across rows and still create update anomalies; 1NF does **not** mean 3NF.

## 2NF — Remove partial dependencies from the staging composite key

The staging primary key is `(source_file, row_no)`. But `source_file → country, version, dataVersion, source, sourceDate, license, codeStandard`: these metadata values depend only on **part of the composite key**. With these five province-split files, `source_file → province_id, province_name` also holds. Store these in `SOURCE_SNAPSHOT` and `PROVINCE`, not 14,816 repeated village rows.

Illustrative 2NF stage rows (real values; `snapshot_id` is a generated file-key reference, `row_no` a generated ordinal):

| snapshot_id | row_no | village_id | village_name | cell_id suffix | cell_name | district_name |
|---|---:|---|---|---|---|---|
| umujyi-wa-kigali | 1 | village-11010102 | Gihanga | cell-akabahizi | Akabahizi | Nyarugenge |
| umujyi-wa-kigali | 2 | village-11010103 | Iterambere | cell-akabahizi | Akabahizi | Nyarugenge |
| umujyi-wa-kigali | 3 | village-11010104 | Izuba | cell-akabahizi | Akabahizi | Nyarugenge |
| umujyi-wa-kigali | 4 | village-11010105 | Nyaburanga | cell-akabahizi | Akabahizi | Nyarugenge |
| umujyi-wa-kigali | 5 | village-11010106 | Nyenyeri | cell-akabahizi | Akabahizi | Nyarugenge |

`cell-akabahizi` above is a **displayed suffix**, not the stored source ID. The full source ID is `province-umujyi-wa-kigali-district-nyarugenge-sector-gitega-cell-akabahizi`.

**Dependency removed:** source metadata and province description no longer depend on only `source_file` while being duplicated against a composite `(source_file,row_no)` key. The wider 2NF stage still repeats district, sector, and cell descriptions, so more normalization remains.

> Important distinction: if instead we had chosen the **single** globally unique `village_id` as the 1NF key, the village flat table would already satisfy 2NF automatically (a one-column key cannot have a partial-key dependency). The composite *staging* key above makes the legitimate source-file partial dependency visible; do not claim 2NF must always involve splitting.

## 3NF — Remove transitive dependencies

A wide village record redundantly repeats the descriptions of its ancestors:
`village_id → cell_id → cell_name, sector_id`,
`cell_id → sector_id → sector_name, district_id`,
`sector_id → district_id → district_name, province_id`,
`district_id → province_id → province_name`.

**Dependency removed:** these are transitive dependencies. Store each place at its own level; child tables retain only their direct parent's ID. No table stores the parent's name as an attribute of the child.

Final tables: `SOURCE_SNAPSHOT`, `PROVINCE`, `DISTRICT`, `SECTOR`, `CELL`, `VILLAGE` (**6 related tables**).

**3NF VILLAGE example (five real rows):**

| village_id (PK) | village_name | source_nep | cell_id (FK, displayed suffix) |
|---|---|---|---|
| village-11010102 | Gihanga | GE | cell-akabahizi |
| village-11010103 | Iterambere | GE | cell-akabahizi |
| village-11010104 | Izuba | GE | cell-akabahizi |
| village-11010105 | Nyaburanga | GE | cell-akabahizi |
| village-11010106 | Nyenyeri | GE | cell-akabahizi |

**3NF parent examples (actual records; each actual full ID is preserved in the database):**

| Table | ID (abbreviated for display) | Name | Parent |
|---|---|---|---|
| PROVINCE | province-umujyi-wa-kigali | Umujyi wa Kigali | source file umujyi-wa-kigali.json |
| PROVINCE | province-amajyaruguru | Amajyaruguru | source file amajyaruguru.json |
| PROVINCE | province-amajyepfo | Amajyepfo | source file amajyepfo.json |
| DISTRICT | district-nyarugenge | Nyarugenge | Umujyi wa Kigali |
| DISTRICT | district-gasabo | Gasabo | Umujyi wa Kigali |
| DISTRICT | district-kicukiro | Kicukiro | Umujyi wa Kigali |
| CELL | cell-akabahizi | Akabahizi | Gitega |
| CELL | cell-akabeza | Akabeza | Gitega |
| CELL | cell-gacyamo | Gacyamo | Gitega |

The abbreviated labels are for explanation only. **Never load the shortened IDs; use the complete original JSON `id` values.**

## Functional dependencies in the final 3NF design

- `snapshot_id → country, source_title, source_date, source_version, dataset_version, license, code_standard, source_url, original_filename, original_git_sha`
- `province_id → province_name, snapshot_id`
- `district_id → district_name, province_id`
- `sector_id → sector_name, district_id`
- `cell_id → cell_name, sector_id`
- `village_id → village_name, source_nep, cell_id`

Names are **not unique keys** (7 same-cell duplicate village-name groups occur in the source). Each child has one required parent; a parent may have multiple children. There are no many-to-many relationships in this geographical source, so **no junction table is justified** for the source itself.

## Complete raw-field-to-target mapping (and future conversions)

| Raw JSON path | Target field(s) | Transformation or reason |
|---|---|---|
| `country` | `SOURCE_SNAPSHOT.country` | Copy as text |
| `version` | `SOURCE_SNAPSHOT.source_version` | Copy as text; not an Oracle NUMBER |
| `dataVersion` | `SOURCE_SNAPSHOT.dataset_version` | Copy text such as `2019-07` |
| `source` | `SOURCE_SNAPSHOT.source_title` | Copy as text |
| `sourceDate` | `SOURCE_SNAPSHOT.source_date` | Convert ISO text to validated date in Phase IV |
| `license` | `SOURCE_SNAPSHOT.license` | Copy as text |
| `codeStandard` | `SOURCE_SNAPSHOT.code_standard` | Copy as text; not proof of any extra code field |
| `provinces[]` | `PROVINCE` | One child row per object (repeating list becomes table) |
| `provinces[].id` | `PROVINCE.province_id` | Copy entire source string |
| `provinces[].name` | `PROVINCE.province_name` | Copy original text |
| `provinces[].districts[]` | `DISTRICT` | One row per element |
| `districts[].id` | `DISTRICT.district_id` | Copy entire string |
| `districts[].name` | `DISTRICT.district_name` | Copy original text |
| `districts[].sectors[]` | `SECTOR` | One row per element |
| `sectors[].id` | `SECTOR.sector_id` | Copy entire string |
| `sectors[].name` | `SECTOR.sector_name` | Copy original text |
| `sectors[].cells[]` | `CELL` | One row per element |
| `cells[].id` | `CELL.cell_id` | Copy entire string |
| `cells[].name` | `CELL.cell_name` | Copy original text |
| `cells[].villages[]` | `VILLAGE` | One row per element |
| `villages[].id` | `VILLAGE.village_id` | Copy entire string |
| `villages[].name` | `VILLAGE.village_name` | Copy original text |
| `villages[].nep` | `VILLAGE.source_nep` | Copy exactly, without guessing what it means |
| Object containment | `DISTRICT.province_id`, `SECTOR.district_id`, `CELL.sector_id`, `VILLAGE.cell_id` | **Derived FK** from immediate enclosing object, not a new raw attribute |
| Physical source filename | `SOURCE_SNAPSHOT.snapshot_id`, `original_filename`; `PROVINCE.snapshot_id` | File name preserved; stable snapshot key derived |
| Upstream URL + Git blob SHA | `SOURCE_SNAPSHOT.source_url`, `original_git_sha` | Provenance added at ingestion, not fields inside JSON |

No actual raw fields are silently dropped. The **nested array containers** are replaced by rows and foreign-key relationships, and `row_no` is temporary staging information only.

## Phase IV cleaning/conversion checklist
1. Keep the original 5 raw JSON files immutable.
2. Validate source dates before converting text to date; confirm source keys remain strings.
3. Log 7 same-cell duplicate-name groups for investigation; IDs remain distinct, with no automatic merge.
4. Decide if display casing should be standardized for 44 uppercase sector names, without overwriting the original source.
5. Validate all ancestor FKs and file lineage when loading Oracle; loading expected counts are 5/30/416/2142/14816.
6. Do not join these source IDs with the earlier Open Admin Data (451-unit) IDs without a verified crosswalk.

See [data_dictionary.md](data_dictionary.md) and [erd.png](erd.png). The schema is **logical**: no Oracle-specific types or sizes are specified here.
