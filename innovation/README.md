# Planned innovation: Express + Handlebars emergency-contact portal

This application is **proposed, not yet implemented**. Its backend uses **Node.js/Express** and its frontend uses **Handlebars**. Express connects to Oracle Database via `node-oracledb` and invokes PL/SQL packages for event synchronization, duty status, contact eligibility and location search. All business rules remain in Oracle PL/SQL.

Citizen features: saved home area, search another Rwandan area without overwriting home, verified currently available approved duty contacts, and an official emergency-number fallback.

Supervisor/demo features: authenticate and simulate external event messages, confirm duty check-in, inspect audit history and synchronization freshness.

The final demo must use a **real live Oracle connection**, not hard-coded search results. The demonstration's officer names, phone numbers, and duty events are synthetic. No actual government integration or real emergency dispatch is claimed.
