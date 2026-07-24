# Dataset Methodology & Criteria

This document defines the rules, standards, and workflow used to maintain the predatory academic conferences database.

---

## 🚫 Red Flag Definitions

An entity is flagged when it meets any **1 Major Criterion** or **3+ Supporting Criteria** as described below. Each flag must be linked directly to a dated, hashed evidence entry.

### Major Criteria
- **`same_day_same_venue_stacking`**: Hosting dozens or hundreds of conferences across wildly unrelated domains (e.g. quantum physics and dentistry) at the exact same venue on the exact same date.
- **`no_named_accrediting_body`**: Claiming accreditation or sponsorship by fictitious or non-existent academic institutions.
- **`generic_reused_content`**: Copying program boards, greeting messages, or reviews verbatim from other completely unrelated conferences.
- **`unregistered_isbn`**: Issuing fake ISBN or ISSN registries that fail checks in Global Register systems.

### Supporting Criteria
- **`date_inconsistencies`**: Displaying contradictory deadlines (e.g., acceptance date prior to submission deadline).
- **`fake_or_unverifiable_speakers`**: Listing keynote speakers who have not agreed to speak or do not exist.
- **`false_indexing_claims`**: Stating proceedings are indexed in Scopus, IEEE Xplore, or Web of Science when they are not.
- **`plagiarized_proceedings`**: Publishing accepted papers that contain plagiarized materials without review.
- **`other`**: Any other deceptive academic practices (requires detail description).

---

## 📂 Evidence Standards
- **Snapshots**: Every entry must reference at least one snapshot source.
- **Wayback Machine**: If available, Wayback Machine links should be recorded (`archive_org_url`).
- **Cryptographic Hashes**: Raw HTML snapshots are stored in `evidence/<slug>/...` and hashed using SHA-256 to ensure authenticity.
- **Append-Only Evidence**: Once added, evidence is never deleted or altered. Corrections are appended, preserving historical auditability.

---

## ⚖️ Dispute Resolution Process

Anyone may file a dispute if they believe a flag has been incorrectly added.

### Resolution Statuses:
1. **`unresolved`**: Dispute has been logged and is undergoing maintainer review.
2. **`flag_upheld`**: The dispute was reviewed and dismissed; evidence supports keeping the flag active.
3. **`flag_removed`**: The dispute was verified and the flag has been deactivated/resolved.

*Note: Even when a flag is removed, existing evidence remains in the repository history to preserve accountability.*

---

## 📜 Version History

### `v1.0` — 2026-07-24
- Initial release of structured evidence-backed schemas and workflows.
- Migrated legacy CSV datasets to YAML.
