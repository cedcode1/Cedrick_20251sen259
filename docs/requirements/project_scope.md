# Project boundary and operational requirements

## Owns
1. Verified administrative geographic lookup and saved/current/selected location logic.
2. External-event ingestion, validation, event history and derived eligibility state.
3. Duty check-in/availability, public-approved duty-contact access and search audit.
4. Data-freshness warnings, supervisor administrative availability views and official emergency fallback.

## Does NOT own
Hiring decisions, payroll, transfer approvals, dismissal decisions, disciplinary judgments, personal phone publication, official emergency dispatch, or RNP emergency operations.

## Event contract (simulation)
Each upstream message should contain `source_system`, `event_id`, `officer_ref`, `event_type`, `effective_at`, `occurred_at`, `payload`, `source_signature` (or authenticated channel), `received_at`. Events must be idempotent and ordered by effective time or sequence; conflicts are quarantined for human review. Data source trust is separate from event occurrence.

## Public availability rule
To show a contact: officer eligible AND currently assigned to the requested area AND checked-in for a current shift AND not suspended/dismissed AND not expired/stale AND duty contact approved for public display. A schedule alone never establishes actual availability. Return last-verified indicator. Never expose unapproved personal numbers.

## High-value acceptance tests
- Search home area returns same area after user searches Rubavu, without overwriting Kigali preference.
- Duplicate event processed once, not twice.
- Late transfer does not override a newer assignment.
- Suspension blocks public result immediately and leaves audit history.
- No check-in: no "available" public contact.
- A full day of silent upstream feed generates a freshness warning, not false confidence.
- No verified contacts -> fallback official emergency number and clear messaging.
- Citizen can select a different district/sector manually without precise GPS permission.
