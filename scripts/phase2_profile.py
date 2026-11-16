#!/usr/bin/env python3
"""Reproduce the Phase II profile from unchanged raw province JSON files.

Usage: python3 scripts/phase2_profile.py
No third-party packages; never writes to data/raw/.
"""
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "provinces"
SOURCES = {
    "umujyi-wa-kigali.json": "6180baef2a84c95d40a31bb9812c4f5c21c4b021",
    "amajyaruguru.json": "ad6a46bdfb9097f5a44a64488a2a8963cf23fce0",
    "amajyepfo.json": "1dc18529c369014d6d9e061cd06fe75290bb3aea",
    "iburasirazuba.json": "a773ed2e9946637dff99d3859aebe8ab09959c3e",
    "iburengerazuba.json": "a8e0b46c19ebf4ce48eaa707a8381948eff61c8f",
}
EXPECTED = {"province": 5, "district": 30, "sector": 416, "cell": 2142, "village": 14816}

def git_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def main():
    counts = Counter()
    per_file = {}
    visited_ids = set()
    duplicates_ids = []
    missing_ids = []
    missing_names = []
    orphan_links = []
    empty_arrays = Counter()
    exact_seen = {level: set() for level in EXPECTED}
    duplicate_exact = Counter()
    sibling_village_names = defaultdict(list)
    nep_values = Counter()
    uppercase_sector_names = 0
    raw_verification = {}

    def add(level, item, filename):
        unit_id = item.get("id")
        name = item.get("name")
        counts[level] += 1
        if not unit_id:
            missing_ids.append((filename, level))
        elif unit_id in visited_ids:
            duplicates_ids.append(unit_id)
        else:
            visited_ids.add(unit_id)
        if not isinstance(name, str) or not name.strip():
            missing_names.append((filename, level, unit_id))
        # Exact duplicate of the full nested source object, separately by level.
        canonical = json.dumps(item, sort_keys=True, ensure_ascii=False)
        if canonical in exact_seen[level]:
            duplicate_exact[level] += 1
        exact_seen[level].add(canonical)

    for filename, expected_sha in SOURCES.items():
        data = (RAW / filename).read_bytes()
        found_sha = git_blob_sha(data)
        raw_verification[filename] = {
            "bytes": len(data),
            "git_blob_sha": found_sha,
            "matches_upstream": found_sha == expected_sha,
        }
        root = json.loads(data)
        local = Counter()
        if not isinstance(root.get("provinces"), list):
            raise ValueError(f"{filename}: provinces must be an array")
        for p in root["provinces"]:
            add("province", p, filename); local["province"] += 1
            if not p.get("districts"): empty_arrays["districts"] += 1
            for d in p.get("districts", []):
                add("district", d, filename); local["district"] += 1
                if not p.get("id"): orphan_links.append(("district", d.get("id")))
                if not d.get("sectors"): empty_arrays["sectors"] += 1
                for s in d.get("sectors", []):
                    add("sector", s, filename); local["sector"] += 1
                    if not d.get("id"): orphan_links.append(("sector", s.get("id")))
                    if isinstance(s.get("name"), str) and s["name"] == s["name"].upper():
                        uppercase_sector_names += 1
                    if not s.get("cells"): empty_arrays["cells"] += 1
                    for c in s.get("cells", []):
                        add("cell", c, filename); local["cell"] += 1
                        if not s.get("id"): orphan_links.append(("cell", c.get("id")))
                        if not c.get("villages"): empty_arrays["villages"] += 1
                        for v in c.get("villages", []):
                            add("village", v, filename); local["village"] += 1
                            if not c.get("id"): orphan_links.append(("village", v.get("id")))
                            nep_values[v.get("nep")] += 1
                            key = (c.get("id"), str(v.get("name", "")).strip().casefold())
                            sibling_village_names[key].append({
                                "id": v.get("id"),
                                "name": v.get("name"),
                                "cell": c.get("name"),
                                "sector": s.get("name"),
                                "district": d.get("name"),
                                "province": p.get("name"),
                            })
        per_file[filename] = dict(local)

    sibling_duplicates = [
        records for records in sibling_village_names.values() if len(records) > 1
    ]
    report = {
        "dataset": "NISR-derived Rwanda administrative hierarchy; source data edition 2019-07",
        "counts_by_level": {key: counts[key] for key in EXPECTED},
        "total_nested_records": sum(counts.values()),
        "source_file_profiles": per_file,
        "raw_blob_hashes": raw_verification,
        "missing_ids": len(missing_ids),
        "duplicate_ids": len(duplicates_ids),
        "missing_names": len(missing_names),
        "invalid_parent_container_refs": len(orphan_links),
        "empty_child_arrays": dict(empty_arrays),
        "exact_duplicate_records_by_level": dict(duplicate_exact),
        "duplicate_village_name_groups_within_cell": len(sibling_duplicates),
        "duplicate_village_name_examples": sibling_duplicates,
        "sector_names_all_uppercase": uppercase_sector_names,
        "village_nep_values": dict(nep_values),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))

    errors = []
    if dict(counts) != EXPECTED: errors.append("unexpected level counts")
    if sum(counts.values()) != 17409: errors.append("unexpected total records")
    if any(not obj["matches_upstream"] for obj in raw_verification.values()):
        errors.append("raw file differs from source Git blob")
    if missing_ids or duplicates_ids or missing_names or orphan_links:
        errors.append("missing/duplicate IDs, blank names, or invalid parents")
    if len(sibling_duplicates) != 7: errors.append("duplicate-name count changed")
    if uppercase_sector_names != 44: errors.append("uppercase sector count changed")
    if dict(nep_values) != {"GE": 7655, "Microgrid": 2436, "SAS": 4725}:
        errors.append("nep category counts changed")
    if errors:
        print("PHASE II PROFILE FAILURE: " + "; ".join(errors), file=sys.stderr)
        return 1
    print("\nPHASE II PROFILE PASSED", file=sys.stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
