# Phase II — Logical Data Dictionary (3NF)

**Scope:** Real administrative geography from five untouched 2019-edition source JSON files. Six related tables: `SOURCE_SNAPSHOT`, `PROVINCE`, `DISTRICT`, `SECTOR`, `CELL`, `VILLAGE`. **No Oracle data types or sizes** in Phase II, as required by the lecturer.

## SOURCE_SNAPSHOT — five original files

| Column | Meaning | Required? | Key / unique? |
|---|---|---|---|
| `snapshot_id` | Stable internal source-file key, derived from province filename | Yes | **PK, unique** |
| `country` | Original root `country` | Yes | No |
| `source_title` | Root `source`, citation/title of raw data | Yes | No |
| `source_date` | Root `sourceDate`, original source edition date | Yes | No |
| `source_version` | Root `version`, package version | Yes | No |
| `dataset_version` | Root `dataVersion` | Yes | No |
| `license` | Root data licensing label | Yes | No |
| `code_standard` | Root `codeStandard` claim, preserved verbatim | Yes | No |
| `original_filename` | Exact filename of original JSON | Yes | Unique |
| `source_url` | URL used to retrieve original JSON | Yes | Unique |
| `original_git_sha` | Git blob ID for byte-for-byte source copy | Yes | Unique |

## PROVINCE — five rows

| Column | Meaning | Required? | Key / unique? |
|---|---|---|---|
| `province_id` | Original `provinces[].id` | Yes | **PK, unique** |
| `province_name` | Original province name | Yes | No |
| `snapshot_id` | Source file containing this province | Yes | **FK → SOURCE_SNAPSHOT.snapshot_id** |

## DISTRICT — 30 rows

| Column | Meaning | Required? | Key / unique? |
|---|---|---|---|
| `district_id` | Original district ID | Yes | **PK, unique** |
| `district_name` | Original district name | Yes | No |
| `province_id` | Its enclosing province ID | Yes | **FK → PROVINCE.province_id** |

## SECTOR — 416 rows

| Column | Meaning | Required? | Key / unique? |
|---|---|---|---|
| `sector_id` | Original sector ID | Yes | **PK, unique** |
| `sector_name` | Original sector name, including source case | Yes | No |
| `district_id` | Its enclosing district ID | Yes | **FK → DISTRICT.district_id** |

## CELL — 2,142 rows

| Column | Meaning | Required? | Key / unique? |
|---|---|---|---|
| `cell_id` | Original cell ID | Yes | **PK, unique** |
| `cell_name` | Original cell name | Yes | No |
| `sector_id` | Its enclosing sector ID | Yes | **FK → SECTOR.sector_id** |

## VILLAGE — 14,816 rows

| Column | Meaning | Required? | Key / unique? |
|---|---|---|---|
| `village_id` | Original village ID (e.g., `village-11010102`) | Yes | **PK, unique** |
| `village_name` | Original village name | Yes | **Not unique** |
| `source_nep` | Original village `nep` text, not interpreted | Yes in current source | No |
| `cell_id` | Its enclosing cell ID | Yes | **FK → CELL.cell_id** |

**Do not add a unique constraint on (cell_id, village_name):** seven duplicate village-name groups within the same cell exist, with distinct IDs.

## Relationships, cardinality, and optionality

| Parent (exactly one for a child) | Child (zero or many per parent, logical design) | Child FK | FK optional? |
|---|---|---|---|
| SOURCE_SNAPSHOT | PROVINCE | `PROVINCE.snapshot_id` | No |
| PROVINCE | DISTRICT | `DISTRICT.province_id` | No |
| DISTRICT | SECTOR | `SECTOR.district_id` | No |
| SECTOR | CELL | `CELL.sector_id` | No |
| CELL | VILLAGE | `VILLAGE.cell_id` | No |

The raw snapshot actually has **at least one child in every recorded branch**. The **0..many** logical cardinality allows a parent to exist before children are loaded. Every **child→parent** foreign key is mandatory. This is a chain of one-to-many relationships, so the source has **no many-to-many relationship** requiring a junction table.

## Logical constraints and validation

- All six primary keys must be unique and nonblank.
- All listed required fields must be present.
- No FK may reference a missing parent.
- Preserve original names and `source_nep` in source form until an explicitly approved Phase IV cleaning step.
- `SOURCE_SNAPSHOT.original_filename` and `source_url` identify one source file, not an officer/duty record.
- Use source IDs as strings without extracting assumptions from their readable segments.

## Boundary with the full ABANYERONDO application

The six tables here normalize the **real dataset supplied for Phase II**. They are not the entire future application's schema. Officer eligibility, automatic patrol-post schedules, supervisor overrides, attendance and citizen contact search will require **additional application tables and synthetic demonstration fixtures** in later implementation work. None of those tables is falsely presented as containing real officer data today.

See [normalization.md](normalization.md) for row samples, UNF→3NF transformations, and full field mapping, and [erd.png](erd.png) for the crow's-foot ERD.
