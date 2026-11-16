# ABANYERONDO — Phase II Dataset Card

## Dataset identity
- **Title:** Rwanda administrative hierarchy, province-split JSON snapshot.
- **Why this dataset:** A citizen searches Abanyerondo contacts by location. Real place names and parent–child administrative boundaries are needed for that location lookup.
- **Original data provider:** National Institute of Statistics of Rwanda (NISR), *List of Villages* (source edition dated 2019-07-03), as attributed by the redistributing project.
- **Redistributor:** [rwanda-admin project](https://github.com/Derrick-MUGISHA/Rwanda-Province-District-Sector-Cell-Village---in-Rwanda).
- **Original download URLs:** `https://raw.githubusercontent.com/Derrick-MUGISHA/Rwanda-Province-District-Sector-Cell-Village---in-Rwanda/main/data/provinces/<filename>`.
- **Source license:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) for the DATASET; see upstream [LICENSE-DATA](https://github.com/Derrick-MUGISHA/Rwanda-Province-District-Sector-Cell-Village---in-Rwanda/blob/main/LICENSE-DATA). The repository code has a separate ISC license.
- **Format:** UTF-8 nested JSON, five unmodified province files.
- **Collection date:** 2026-11-16.
- **Data version:** 2019-07; **package version:** 1.0.0.
- **Total raw size:** 3,071,434 bytes across five files (GitHub source blob sizes).
- **Grain:** One nested province/district/sector/cell/village object represents **one administrative unit**. Each physical source file has one top-level province and numerous nested records. The record counts below count nested units, not top-level JSON documents.
- **Personal data:** No personnel names, ID numbers or telephone numbers. The names are of public places. No anonymization required.

## Unchanged source files and chain of custody

All five files were copied byte-for-byte into `data/raw/provinces/`. Their destination Git blob SHA-1 values were checked against the upstream blobs (Git's object hash; not a file-content SHA-256 checksum).

| Original filename | Districts | Sectors | Cells | Villages | Raw Git blob SHA |
|---|---:|---:|---:|---:|---|
| umujyi-wa-kigali.json | 3 | 35 | 156 | 1,163 | `6180baef2a84c95d40a31bb9812c4f5c21c4b021` |
| amajyaruguru.json | 5 | 89 | 414 | 2,744 | `ad6a46bdfb9097f5a44a64488a2a8963cf23fce0` |
| amajyepfo.json | 8 | 101 | 532 | 3,501 | `1dc18529c369014d6d9e061cd06fe75290bb3aea` |
| iburasirazuba.json | 7 | 95 | 502 | 3,791 | `a773ed2e9946637dff99d3859aebe8ab09959c3e` |
| iburengerazuba.json | 7 | 96 | 538 | 3,617 | `a8e0b46c19ebf4ce48eaa707a8381948eff61c8f` |

All files contain one province each; provinces total 5. Every one of these files has more than 500 *nested village records*.

## Verified record counts

| Hierarchy level | Records |
|---|---:|
| Province | 5 |
| District | 30 |
| Sector | 416 |
| Cell | 2,142 |
| Village | 14,816 |
| **Total distinct administrative objects** | **17,409** |

## Data quality audit (before cleaning)

Methods: parsed all five JSON files; traversed every nested object; counted the objects by hierarchy level; checked ID and name presence and global uniqueness of IDs; checked that every child has a parent in the immediately enclosing level; counted empty child arrays and exact duplicate JSON objects within each level; compared case-folded village names within the *same cell*.

| Test | Observed count | Interpretation |
|---|---:|---|
| Missing/empty administrative IDs | **0 / 17,409** | Every unit has an ID |
| Repeated administrative IDs, all levels combined | **0** | IDs are globally unique in this snapshot |
| Missing/blank administrative names | **0 / 17,409** | All names present |
| Missing parent references after extracting containment | **0** | Every child belongs to a parent |
| Empty child arrays for province/district/sector/cell | **0** | No empty branches observed |
| Exact duplicate nested records within a level | **0** | No identical unit object duplicates observed |
| **Repeated village names within the same cell** | **7 duplicate-name groups (14 village rows)** | Different village IDs; must investigate, not delete |
| Sector names written entirely in uppercase | **44 / 416** | Style inconsistency; not automatically an error |
| Missing village `nep` fields | **0 / 14,816** | Field present for each village |

**Seven same-cell repeated names (do not remove without external verification):** Rusekabuye (Mahaza, Rulindo), Kigarama (Cyarwa, Huye), Gatoki (Kabeza, Gatsibo), Bara (Rubimba, Kayonza), Murama (Gabiro, Rutsiro), Nyakiriba (Tyazo, Nyabihu), Kazuba (Mashya, Ngororero). In all seven cases the two records have distinct IDs.

`nep` values: `GE` **7,655**; `Microgrid` **2,436**; `SAS` **4,725** (sum **14,816**). The precise meaning of `nep` is not verified here, so it is preserved as a source field rather than interpreted as security information.

There are **no standalone `code` attributes** on the nested administrative objects: actual raw fields are `id`, `name`, children arrays, and `nep` at village level. Do not invent a missing-code count.

## Example source record
The first village is `village-11010102`, `Gihanga`, `nep=GE`, inside cell `Akabahizi` → sector `Gitega` → district `Nyarugenge` → province `Umujyi wa Kigali`.

## Limitations and Phase IV cleaning checklist
1. **Source age:** A July 2019 administrative edition may not reflect November 2026 boundaries or renamed locations. Validate against a current authorized source before operational use.
2. **Duplicate same-cell names:** Investigate the 7 pairs using official village codes; do not merge based on names alone.
3. **Casing:** Assess the 44 all-uppercase sector names before any optional presentation normalization. Preserve original names in `data/raw/`.
4. **`nep` semantics:** Obtain the source definition if it will be used; no inferred security meaning.
5. **Key compatibility:** IDs do not automatically match those in the older 451-row Open Admin Data dataset. Use an explicit mapping before joining.
6. **Type conversion:** `sourceDate` is ISO text and will need date validation/conversion in Phase IV; IDs and names remain strings.
7. **Privacy and emergency safety:** This is geographic reference data only. No real officer or emergency-call information is included; not a live dispatch data source.

**No raw records were edited or cleaned in Phase II.** Detailed field mapping and normalization: [normalization.md](../docs/design/normalization.md).
