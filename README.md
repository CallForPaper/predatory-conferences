# 🚫 Predatory Conferences & Events — Open Dataset

A community-maintained, open-source dataset of predatory conference organizers and events that exploit researchers through deceptive academic meetings.

> **Maintained in partnership with [callforpaper.org](https://callforpaper.org)** — used to power backend trust-scoring and protect researchers from predatory CFPs.

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Last Updated](https://img.shields.io/github/last-commit/callforpaper/predatory-conferences)](https://github.com/callforpaper/predatory-conferences/commits/main)

---

## 📦 What's in this repo

| File | Description |
|------|-------------|
| `data/organizers.csv` | Known predatory conference organizers/publishers |
| `data/conferences.csv` | Specific flagged conference series/events |
| `data/sources.csv` | Upstream sources this dataset is compiled from |
| `docs/criteria.md` | How we define and identify predatory conferences |
| `docs/sources.md` | Full source attribution and methodology |

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
| Predatory organizers | 150+ |
| Flagged conference series | 300+ |
| Sources compiled | 8 |
| Last full refresh | June 2025 |

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

## 📋 CSV Schema

### `data/organizers.csv`

```
name, domain, aliases, status, evidence_url, source, added_date, notes
```

| Field | Description |
|-------|-------------|
| `name` | Organization name |
| `domain` | Primary website domain |
| `aliases` | Other names used (pipe-separated) |
| `status` | `confirmed` / `suspected` / `disputed` |
| `evidence_url` | URL to evidence or documentation |
| `source` | Which upstream source flagged this |
| `added_date` | YYYY-MM-DD |
| `notes` | Free-text context |

### `data/conferences.csv`

```
name, organizer_domain, scope, status, evidence_url, source, added_date, notes
```

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