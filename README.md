# ABANYERONDO: Community Security Availability and Emergency Assistance System

**Student:** IRAKOZE PEACE CEDRICK  
**Student ID:** 20251SEN259  
**Course:** INSY 8311 - Database Development with PL/SQL  
**Instructor:** Eric Maniraguha  
**Academic year:** 2026/2027, Semester I  
**Phase:** 0 - Research, data source and project proposal
**Web stack:** Node.js, Express, Handlebars; Oracle Database + PL/SQL.

## Problem
Community members may not know which approved local security duty contact to reach during danger, particularly when they are outside their saved home area. A schedule alone is not proof of availability. Irondo is a community-led security arrangement supported through local structures (Rwanda National Police, 2025). We propose a directory of **verified, currently eligible, checked-in duty contacts** with a public search by saved or selected area; the app must never replace formal emergency services.

## Proposed solution
An Oracle/PL/SQL platform receives simulated upstream personnel events (hire, transfer, suspension, dismissal) and synchronizes eligibility and assignments without itself recruiting, dismissing, paying or transferring personnel. Authorized shift confirmation establishes operational availability. A Node.js/Express backend calls Oracle PL/SQL for approved duty contacts and Handlebars renders citizen-facing location search pages. A citizen can search another location without overwriting a saved home area. A home location stays saved when searching another area. All personnel/contact and event test fixtures are **synthetic**.

## Objectives
1. Load and normalize real Rwanda geographic records and maintain source lineage.
2. Validate, deduplicate, version and audit externally supplied personnel events.
3. Enforce duty eligibility and contact visibility based on assignment, check-in, freshness and status.
4. Enable citizen saved-location and alternative-location search via a live Oracle-connected UI.

## Real dataset and limitations
- **Actual packaged dataset:** https://github.com/open-admin-data/rwanda-administrative-divisions - Open Admin Data Rwanda country repository, CC BY 4.0 as indicated in its source files; 451 validated rows = 5 province-level, 30 district, 416 sector records. The exact source files are `data/all-province.json`, `data/all-district.json`, `data/all-sector.json`. See `data/README.md` for provenance and reproducible SQL loading.
- World Bank Rwanda boundaries/villages (https://datacatalog.worldbank.org/search/dataset/0041453/rwanda-admin-boundaries-and-villages) are contextual source only; **not downloaded** into this submission. It is historical (2012). The NISR 2022 geographic service requires further license review.
- Geographic `geo.lat`/`geo.lon` values may be approximate or contain errors; **not suitable for live dispatch routing** without validation.
- No actual Irondo officer, duty, phone, emergency call or compensation records were obtained. Such demonstration records will be expressly synthetic.

## Planned normalized tables (Phase II draft)
`SOURCE_IMPORT`, `PROVINCE`, `DISTRICT`, `SECTOR`, `OFFICER_REFERENCE`, `PERSONNEL_EVENT`, `OFFICER_ASSIGNMENT`, `DUTY_SHIFT`, `DUTY_CHECKIN`, `DUTY_CONTACT`, `CITIZEN_LOCATION_PREF`, `CONTACT_LOOKUP_AUDIT`, `SYNC_AUDIT`.

## Planned PL/SQL
`PKG_SYNC.apply_event` (idempotency, event ordering, status transitions), `PKG_AVAILABILITY.find_contacts` and `is_available`, audit triggers and restrictions that block duplicate effective events, expired duty status and unauthorized contact disclosure. Exceptions and cursors for validation and area-based reporting.

## Innovation
**Node.js + Express backend with Handlebars frontend**, using `node-oracledb` to invoke Oracle PL/SQL packages (planned integration). Demo: a simulated transfer or suspension changes the real query results without any UI hardcoded answers.

## Repository layout
`docs/research/`, `docs/proposal/`, `docs/presentation/`, `docs/requirements/`, `data/`, `database/`, `innovation/`, `submission/`.

## Important boundaries
This is an academic proof of concept, **not an official Rwandan emergency hotline**. In a real emergency, use official emergency services (112 per https://www.gov.rw/emergency). No real officers' personal details are published.

## Submission status
Group I topic registration is complete (number 22, row 25), automatic check OK, and lecturer status **Approved** as verified on 12 November 2026. Project repository: https://github.com/cedcode1/Cedrick_20251sen259. Lecturer email submission is not yet verified. See `submission/STATUS.md` for remaining steps.

## References
The complete APA research log and source URLs are in `docs/research/research_log.md`.
