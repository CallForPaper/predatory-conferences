# Dataset Methodology & Criteria

This document defines the rules, standards, and workflow used to maintain this evidence-backed database of organizers and conferences that do not meet basic academic-integrity verification standards. It is a factual, criteria-based record of observed patterns — not a legal determination of fraud, and not an assertion of intent. Entries reflect what was directly observed, when, and by what evidence; they are updated as evidence changes.

---

## 📖 How to Read an Entry

Entries in this dataset describe **specific, dated, evidenced patterns** — not a legal finding of predatory intent, and not a permanent judgment. Status can and does change as new evidence is added. If you are named in this dataset and believe an entry is inaccurate or outdated, please use the dispute process below rather than requesting removal outside of it — a documented dispute and resolution is more durable and more fair to everyone than an undocumented one.

A conference-level entry does **not** imply wrongdoing by its named organizer unless that organizer separately carries its own independently-evidenced flag. See "Organizer vs. Conference" below for how this distinction is maintained in the data.

---

## 🏢 Organizer vs. Conference — Which File?

This dataset tracks two kinds of entity: **organizers** (a person, company, or network responsible for one or more events) and **conferences** (a specific event, distinct from its organizer, with its own standalone issue). Most flags belong at the organizer level. Use this decision order:

1. **Same domain as an existing organizer entry, or a clear pattern across multiple events** → add/update the **organizer** file. Do not create a separate conference file merely because one event under the same domain has an issue — the evidence's `source_url` already points to the specific page.

2. **Different domain, and the page states an affiliation** with an existing flagged organizer (e.g. "organized by X"), or shows other concrete signs of common ownership (identical site template, shared registration flow, shared contact details) → create a **conference** file with `organizer_slug` pointing to that organizer, and record the linking evidence (the affiliation statement or shared-ownership signal) in that conference's own evidence.

3. **Different domain, common ownership later confirmed** (e.g. a WHOIS match, an admin's own public statement) → prefer adding the second domain to the *organizer's* existing `domains: []` list over creating a conference file — this is really one organizer with two domains, not a distinct event-level issue.

4. **A single event has its own standalone issue, but the named organizer is otherwise unimplicated** (e.g. one rogue local chair fabricates a speaker at one event run by an otherwise-uninvolved institution) → create a **conference** file. For the organizer side of that link, use whichever of these fits:
   - If you want a durable structured link for future entries under the same name, create an `organizers/*.yaml` file with **`status: reference_only`** (see below) — this creates no accusation and carries no red flags of its own.
   - If a durable record isn't warranted, skip the organizer file entirely and set `organizer_slug: null` with a plain-text `organizer_name` on the conference file instead — informational only, not a tracked entity.

5. **Different domain, no affiliation claim, no ownership link, no shared organizer context at all** → this is a new, independent **organizer**, not a conference of anyone already in the dataset.

**Never require an organizer to be created or upgraded to `active_flag` purely as a side effect of filing a conference-level entry.** An organizer only carries `active_flag` status when there is evidence specifically about the organizer itself — not by inheritance from a single flagged event underneath it.

## 🕸️ Networks

Some organizers are linked not by direct evidence against each other, but by 
shared infrastructure — a common proceedings host, a published "conference 
partner"/"associate" listing, shared hosting, or a WHOIS match. This dataset 
models that as a **hub-and-spoke** relationship, not a pairwise mesh: the 
hub (e.g. the site hosting the partner listing) is itself an organizer entity 
in this dataset — typically with `status: reference_only` unless it separately 
carries its own evidenced flags — and every member links to that one hub via 
its own `networks: []` field, rather than every member linking to every other 
member directly.

- **`networks`**: an array of network-hub slugs on an organizer entry, e.g. 
  `networks: [example]`. A single organizer may belong to more 
  than one network.
- **Bi-directional sync**: when Organizer A adds a network hub to its 
  `networks`, the hub's own file (and by extension every other member 
  already linked to that hub) reflects the new member without manual editing 
  of each existing member's file — the hub is the single source of truth for 
  membership, not a fact duplicated across every spoke.
- **Bi-directional removal**: removing a network link from either side (a 
  member disputing membership and winning, or a hub entry being corrected) 
  removes the edge on both sides consistently.
- **Evidence provenance on synced edges**: the member that originally supplied 
  the evidence for a network link (e.g. the associates-page snapshot) keeps 
  that evidence in its own `evidence[]`. Other members who gain the reciprocal 
  edge via sync are not required to independently re-prove the link — but 
  their entry should note which member's evidence the edge traces back to, 
  so the link remains auditable rather than appearing to originate from 
  nowhere.
- Network membership on its own is **not** a red flag — it's a structural fact. 
  See `shared_predatory_network` below for when membership in a network 
  becomes an evidenced criterion.

---

## 🚦 Status Values

Applies to both organizer and conference entries.

- **`active_flag`** — one or more red flags are currently active, each backed by linked evidence.
- **`disputed`** — an open dispute exists (see Dispute Resolution below); flags remain visible pending review.
- **`resolved`** — flags that were once active no longer apply, per a dated re-check; prior evidence remains in history.
- **`unverified`** — the entry's evidence can no longer be independently confirmed (e.g. a cited source has expired or been squatted); not currently presented as an active finding, pending re-verification.
- **`reference_only`** *(organizer entries only)* — this organizer record exists solely so a conference entry can link to it via `organizer_slug`. It carries no red flags and makes no claim about the organizer. Compiled output and any downstream product sync (e.g. callforpaper.org) must treat `reference_only` organizers as **not flagged** — no warning, no negative signal.

---

## 🚫 Red Flag Definitions

An entity is flagged when it meets **any 1 Major Criterion** or **3+ Supporting Criteria**. Every flag must link (`evidence_refs`) to at least one dated, hashed evidence entry that directly supports it — a flag with no linked evidence should not be marked `active`.

Each criterion below includes a **description template**. Generate the `description` field for a flag by filling the template from the entry's structured fields rather than writing free prose — this keeps every flag specific to that organizer/conference and consistent with the wording this document publicly commits to. Only fall back to hand-written description text for `other`, where by definition no template fits.

### Major Criteria

- **`same_day_same_venue_stacking`**
  Hosting **10 or more** conferences across unrelated subject domains at the exact same venue on the exact same date(s).
  *3–9 unrelated conferences at the same venue/date is a Supporting Criterion instead — see below.*
  Structured fields: `stacking_count`, `stacking_domains` (list), `venue`, `event_date`
  Template: `"{stacking_count} conferences across unrelated domains ({stacking_domains}) listed at {venue} on {event_date}."`

- **`no_named_accrediting_body`**
  Claiming accreditation, sponsorship, or partnership with an academic institution, society, or standards body that does not exist, or that has been directly contacted and denies the relationship.
  Structured fields: `claimed_body`, `verification_method` (e.g. "no matching entry in {registry}", "institution contacted, denies affiliation")
  Template: `"Claims accreditation/partnership with '{claimed_body}'; {verification_method}."`

- **`generic_reused_content`**
  Program descriptions, committee bios, greeting messages, or attendee reviews copied verbatim (or near-verbatim) from other unrelated conferences or organizers.
  Structured fields: `content_type` (e.g. "About Us text", "committee bios"), `matched_source` (the other page/organizer it matches), `match_count` (how many pages share the text)
  Template: `"{content_type} matches {matched_source} verbatim, reused across {match_count} otherwise-unrelated listings."`

- **`unregistered_isbn`**
  Publishing an ISBN/ISSN for conference proceedings that fails to resolve in the relevant national or international registry.
  Structured fields: `identifier` (the ISBN/ISSN string), `registry_checked`
  Template: `"ISBN/ISSN '{identifier}' does not resolve in {registry_checked}."`

### Supporting Criteria

- **`same_day_same_venue_stacking` (supporting tier)**
  3–9 unrelated conferences at the same venue on the same date(s) — same fields/template as the major-criterion version above, at the lower count.

- **`date_inconsistencies`**
  Contradictory published dates (e.g., an acceptance-notification date earlier than the submission deadline, or a registration deadline after the event date).
  Structured fields: `date_field_a`, `value_a`, `date_field_b`, `value_b`
  Template: `"Listed {date_field_a} ({value_a}) is inconsistent with {date_field_b} ({value_b})."`

- **`fake_or_unverifiable_speakers`**
  Listing a named keynote/invited speaker who, when contacted or checked against their own public record, did not agree to speak or has no discoverable connection to the event.
  Structured fields: `speaker_name`, `verification_method`
  Template: `"Listed speaker '{speaker_name}' — {verification_method}."`

- **`false_indexing_claims`**
  Stating that proceedings are indexed in Scopus, Web of Science, IEEE Xplore, or a similarly named index, where no matching record exists in that index at the time checked.
  Structured fields: `claimed_index`, `check_date`
  Template: `"Claims indexing in {claimed_index}; no matching record found as of {check_date}."`

- **`plagiarized_proceedings`**
  Published proceedings containing material substantially duplicated from prior, unrelated publications without attribution.
  Structured fields: `paper_title_or_id`, `matched_source`, `similarity_note`
  Template: `"Proceedings entry '{paper_title_or_id}' substantially duplicates {matched_source} ({similarity_note})."`
  
- **`shared_predatory_network`**
Belonging to a network (see "Networks" above) where one or more *other* 
members already carry an independently-evidenced flag in this dataset, or 
appear on an established external blacklist (e.g. Beall's List). This 
criterion flags the affiliation itself — evidence that the entity operates 
within a documented predatory network — separately from and in addition to 
any evidence about the entity's own listings.
Structured fields: `network_ref` (slug of the network hub, from `networks`), 
`flagged_members` (list of other members already flagged, each as either 
a dataset slug or an external blacklist reference)
Template: `"Member of the {network_ref} network, alongside already-flagged 
members: {flagged_members}."`

- **`other`**
  Any other pattern not covered above. Requires a hand-written `description` — no template. Use sparingly; if a pattern recurs across multiple entries, propose a new named criterion instead (open an issue) rather than accumulating `other` flags.

---

## 📂 Evidence Standards

- **Snapshots**: every entry must reference at least one raw HTML snapshot, 
  stored under `evidence/<slug>/...`, with `content_hash` (SHA-256) of the 
  exact stored file.
- **Images**: every entry should also capture an `image_file` (full-page 
  screenshot, stored under `evidence/<slug>/...` via git-lfs) with its own 
  `image_hash` (SHA-256 of the stored image file). This is captured 
  routinely alongside the HTML snapshot — not only when Wayback is 
  unavailable — since a screenshot independently preserves what a human 
  reviewer actually saw (rendering, layout, visible pattern across a page) 
  in a way a raw HTML snapshot alone may not, particularly for dynamic, 
  paginated, or JS-rendered pages.
- **Wayback Machine**: an `archive_org_url` should be recorded whenever a 
  real Save Page Now or Availability API result exists. Never fill this 
  field with a fabricated or templated URL — leave it null rather than 
  guess. `snapshot_file`, `image_file`, and `archive_org_url` are three 
  independent legs of evidence, each captured on its own merits — none is 
  a fallback for another, and Wayback's availability should never block or 
  delay capturing the other two.
- **Cryptographic hashes**: `content_hash` and `image_hash` are both 
  SHA-256 hashes (`sha256:<64 hex chars>`) of their respective stored files, 
  so anyone can independently verify neither has been altered after capture.
- **evidence_refs**: every `red_flags[]` entry must list the `evidence[]` id(s) that support it. A flag with an empty `evidence_refs` is not considered active-flag-ready.
- **Append-only evidence**: once added, an evidence entry is never edited or deleted. Corrections, re-checks, and updated findings are added as new evidence entries (`type: recheck`), leaving the original intact for auditability.
- **Source unavailable**: if a previously cited source (e.g. a domain that has expired, been squatted, or gone dark) can no longer be independently verified, do not delete the old evidence — add a new evidence entry noting the source is no longer verifiable, and set the affected entry's `status` to `unverified` pending re-verification, rather than leaving an un-checkable claim marked active.

---

## ⚖️ Dispute Resolution Process

Anyone — including the organizer or conference named in an entry — may file a dispute if they believe a flag was added or is being maintained incorrectly.

### Resolution statuses
1. **`unresolved`** — dispute logged, under maintainer review.
2. **`flag_upheld`** — reviewed; existing evidence (or a fresh re-check) supports keeping the flag active.
3. **`flag_removed`** — reviewed and verified; the flag no longer applies (e.g. the issue was corrected, or the original evidence is found to be mistaken).

A dispute review should, wherever possible, produce a new dated evidence entry (a re-check) rather than resolving purely on the disputing party's say-so or purely on the maintainer's prior belief. Even when a flag is removed, prior evidence remains in the repository history — a `flag_removed` resolution documents that the entity no longer matches the pattern *as of the re-check date*, not that it never did.

---

## 📜 Version History

### `v1.0.0` — 2026-07-24
- Initial release of structured evidence-backed schemas and workflows.
- Migrated legacy CSV datasets to YAML.

### `v1.1.0` — 2026-07-29
- Replaced the vague "dozens or hundreds" threshold for `same_day_same_venue_stacking` with an explicit numeric split: 10+ = Major Criterion, 3–9 = Supporting Criterion.
- Added a structured-field + description-template model for every named criterion (except `other`), so flag descriptions are generated from specific facts rather than hand-typed prose, while staying consistent with this document's published wording.
- Added explicit guidance for handling sources that later become unverifiable (expired/squatted domains): downgrade to `unverified` with a new evidence entry rather than deleting or leaving an unverifiable claim marked active.
- Added "How to Read an Entry" section clarifying entries are factual/evidenced observations, not legal or intent-based determinations.

### `v1.2.0` — 2026-07-29
- Added the "Organizer vs. Conference — Which File?" section with an explicit decision order, to stop conference-level entries from implicitly requiring or implying an organizer-level flag.
- Added the `reference_only` status for organizer entries that exist solely as a structural link for a conference entry, carrying no red flags of their own; compiled output and downstream syncs must not present `reference_only` organizers as flagged.
- Clarified that `organizer_slug` on a conference entry may be `null`, with a plain-text `organizer_name` used instead, when a durable organizer record isn't warranted.
- Consolidated all status values (`active_flag`, `disputed`, `resolved`, `unverified`, `reference_only`) into one reference section.

### `v1.2.1` — 2026-08-17
- Added the "Networks" section: `networks` field on organizer entries, 
  modeled as hub-and-spoke (not pairwise mesh), with bi-directional 
  sync/removal of membership through the network hub entry.
- Added `shared_predatory_network` as a Supporting Criterion, for organizers 
  belonging to a network where other members already carry an independent 
  flag in this dataset or an external blacklist.
- Added `image_file` and `image_hash` to the evidence schema as independent, 
  routinely-captured evidence alongside `snapshot_file` — not a fallback 
  triggered only when the Wayback Machine is unavailable. Clarified that 
  `snapshot_file`, `image_file`, and `archive_org_url` are three independent 
  legs of evidence.

*Entries flagged under an earlier criteria version remain auditable against the rules that applied at the time (see each entry's `criteria_version` field). This does not retroactively invalidate prior flags, but existing `same_day_same_venue_stacking` entries with counts below 10 should be reclassified from Major to Supporting on next re-check, and any organizer that was created purely to support a conference-level entry should be reviewed for reclassification to `reference_only` if it carries no independently-evidenced flag of its own.*
