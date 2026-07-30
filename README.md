# 🚫 Predatory Conferences & Events — Open Dataset

A community-maintained, open-source dataset of predatory conference organizers and events that exploit researchers through deceptive academic meetings.

> **Maintained by [callforpaper.org](https://callforpaper.org)** — used to power backend trust-scoring and protect researchers from predatory CFPs.

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)
[![DOI](https://zenodo.org/badge/1278977525.svg)](https://doi.org/10.5281/zenodo.21699200)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Last Updated](https://img.shields.io/github/last-commit/callforpaper/predatory-conferences)](https://github.com/callforpaper/predatory-conferences/commits/main)

---

## 📦 What's in this repo

| File / Folder | Description |
|------|-------------|
| `schema/entity.schema.json` | JSON Schema specifying data formats for organizers and conferences |
| `organizers/` | Folder containing structured YAML files for predatory organizers |
| `conferences/` | Folder containing structured YAML files for individual conferences (grouped by organizer) |
| `dist/` | Compiled output JSON files containing all processed entities |
| `evidence/` | Raw HTML snapshots and screenshots proving red flags |
| `methodology.md` | Core standards, red flag definitions, and dispute process |
| `CONTRIBUTING.md` | Guidelines for issues, PRs, and running local validation |

---

## ⚠️ What is a predatory conference?

Predatory conferences exploit researchers by:
- Charging registration fees without providing genuine academic value
- Having no real peer review process (anyone can buy a speaking slot)
- Using deceptive names mimicking legitimate conferences
- Spamming researchers with unsolicited invitations
- Publishing proceedings in predatory journals
- Sometimes canceling events after collecting fees

**Key identifiers:** Overly broad scope, tourist destinations, grammatical errors, no clear organizer affiliations, thousands of simultaneous events, fake indexing claims.

---

## 📊 Dataset Stats

| Category | Count |
|----------|-------|
| Predatory organizers | 50 |
| Flagged conference series | 28 |
| Sources compiled | 8 |
| Last full refresh | July 2026 |

---

## 🔗 Data Sources

This dataset is compiled and deduplicated from:

1. **Beall's List** (archived) — Jeffrey Beall's original predatory publishers/organizers list
2. **stop-predatory-journals** — GitHub-maintained list of predatory publishers
3. **Caltech Questionable Conferences** — Dana Roth's curated list (90+ organizers)
4. **Dolos List** — 34 dubious organizers list
5. **boytchev/spam** — Academic spam metadata collected from researchers
6. **WASET documentation** — World Academy of Science, Engineering and Technology
7. **OMICS International** — FTC-charged predatory publisher/conference organizer
8. **Community submissions** — Via GitHub issues and PRs

See [`docs/sources.md`](docs/sources.md) for full attribution.

---

## 🔄 Integration with callforpaper.org

This repo is the upstream data source for callforpaper.org's backend trust-scoring system. The integration works as follows:

```
GitHub repo (this) → weekly sync → callforpaper.org backend → CFP trust scores
```

- Organizer domains are matched against CFP submissions
- Matched entries influence the verification badge system (Listed → Verified → Trusted → Premium)
- New entries from callforpaper.org's detection pipeline are contributed back here

---

## 📋 Entity Schema

All entries in the dataset are stored in structured YAML files matching the JSON Schema defined in [`schema/entity.schema.json`](schema/entity.schema.json).

### Common Fields:
- `type`: `organizer` or `conference`
- `slug`: Unique identifier string
- `status`: `active_flag` | `disputed` | `resolved` | `unverified`
- `red_flags`: List of flagged behaviors matching versioned methodology criteria
- `evidence`: Cryptographically hashed and snapshot-linked evidence items
- `disputes`: Dispute registry to capture organizer/third-party disputes transparently

## 🤖 GitHub Automation Workflows

We use automated workflows to manage dataset additions, schema validation, and API builds:

1. **Triage & Duplicate Verification (`issue-triage.yml`)**: Triggered when a new report issue is opened. Runs automated checks for existing domain/name duplicates. If the entry is new, it requests wayback machine archival, maps data to compliant YAML schema format, and opens a Pull Request.
2. **Schema & QA Verification (`validate.yml`)**: Runs QA tests checking YAML validation, missing file references, future dates, and cross-reference integrity on every PR.
3. **Distribution Compilation (`compile-report.yml`)**: Upon merging to `main`, compiles individual YAML records into flat JSON arrays at `dist/` and commits them back to the repository.

---

## 🤝 Contributing

We welcome contributions! The most helpful are:

- **New entries** — via issue or PR with evidence
- **Corrections** — if an entry is wrong or outdated
- **Source additions** — pointing to other curated lists we haven't ingested

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

> ⚠️ **Standard of evidence**: All new entries should have a public evidence URL (news article, FTC action, university advisory, archived documentation, etc.). We do not accept unsubstantiated nominations.

---

## ⚖️ License & Disclaimer

Data is released under [CC0 1.0 Universal](LICENSE) (public domain). Use freely.

This dataset represents community-flagged information. Inclusion does not constitute legal accusation. Some entries marked `suspected` reflect patterns consistent with predatory behavior but may not be definitively confirmed. See `status` field.

---

## 🙏 Acknowledgements

Built on the shoulders of Jeffrey Beall, the stop-predatory-journals community, Dana Roth (Caltech), and researchers worldwide who document and expose predatory practices.
