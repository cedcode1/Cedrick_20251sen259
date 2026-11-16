# Phase II — Data Sourcing, Normalization and Logical Design

## Required deliverables

- [Dataset card with source and data-quality counts](../../data/dataset_card.md)
- [Unchanged original raw JSON sources](../../data/raw/provinces/)
- [UNF → 1NF → 2NF → 3NF and complete source-field mapping](normalization.md)
- [Logical ERD, crow's-foot notation](erd.png)
- [Editable diagram source (Graphviz)](erd.dot)
- [Logical data dictionary](data_dictionary.md)

## Summary of the verified source
- **17,409** real administrative units from the 2019 source edition: **5** provinces, **30** districts, **416** sectors, **2,142** cells and **14,816** villages.
- **6** related target tables including source-snapshot lineage.
- No duplicate IDs or missing parent links. **7** duplicate village-name groups within the same cell require later investigation.
- The older 451-record Open Admin Data dataset remains in the repository for Phase 0. Do not join its IDs to the new source without a crosswalk.

## Five-minute in-class demonstration

1. Open `data/raw/provinces/umujyi-wa-kigali.json` in a JSON viewer.
2. Locate `village-11010102` with name `Gihanga` and `nep = GE`.
3. Follow its enclosing cell `Akabahizi`, sector `Gitega`, district `Nyarugenge`, province `Umujyi wa Kigali`.
4. Open `normalization.md` and show the first 1NF row with the complete flattened lineage.
5. Open `erd.png` and show that in 3NF `VILLAGE` stores `cell_id` rather than copying all parent names; follow FK `VILLAGE → CELL → SECTOR → DISTRICT → PROVINCE → SOURCE_SNAPSHOT`.
6. Show `data_dictionary.md` for PK/FK cardinality and source date. Explain 7 duplicate same-cell village-name groups and why IDs, not names, are the keys.

**Limitation:** These are 2019-era administrative records, not real-time officer or emergency locations. No real officer data was included.
