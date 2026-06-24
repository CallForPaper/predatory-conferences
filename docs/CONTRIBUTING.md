# Contributing to the Predatory Conferences Dataset

Thank you for helping protect researchers! Here's how to contribute.

---

## Adding a New Entry

### Option A: GitHub Issue (easier)

1. Open a new issue using the **"Flag an Organizer"** or **"Flag a Conference"** template
2. Fill in all required fields including an evidence URL
3. A maintainer will review and add it if it meets the criteria

### Option B: Pull Request (faster)

1. Fork the repo
2. Add your entry to `data/organizers.csv` or `data/conferences.csv`
3. Follow the schema exactly (no extra columns, proper quoting for commas)
4. Include a public `evidence_url` — this is required for `confirmed`/`suspected` entries
5. Submit a PR with a brief description of the evidence

---

## Evidence Requirements

| Status | Evidence Required |
|--------|------------------|
| `confirmed` | At least one: FTC/government action, court document, Beall's list archive, university advisory with documentation |
| `suspected` | At least one public source (news article, researcher blog with documentation, archived spam patterns) + meeting 3+ criteria from `docs/criteria.md` |

**We do not accept:**
- Anonymous tips without any public supporting evidence
- "I got a spam email" without corroborating sources (though this can be submitted as a comment to an existing entry)
- Entries for conferences you disliked or that rejected your paper

---

## Correcting an Entry

If you believe an entry is wrong:
1. Open an issue with the label `dispute`
2. Explain the error and provide counter-evidence
3. We'll update to `disputed` while reviewing

---

## Updating Sources

If you know of a curated predatory conference list we haven't ingested:
1. Open an issue with the label `new-source`
2. Provide the URL, license, and approximate entry count
3. We'll review and add it to `data/sources.csv` for batch ingestion

---

## Code of Conduct

- Be factual and evidence-based
- Do not submit entries for personal disputes or to harm specific researchers
- This dataset is for protecting researchers, not competitive advantage

---

## Sync with callforpaper.org

The maintainers sync this dataset to callforpaper.org's backend on a weekly basis. Accepted PRs are typically live within 7 days.
