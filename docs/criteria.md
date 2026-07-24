# Criteria for Identifying Predatory Conferences

This document defines the standards used to classify entries in this dataset.

---

## Status Levels

These match the statuses tracked in [`schema/entity.schema.json`](../schema/entity.schema.json):

| Status | Definition |
|--------|-----------|
| `active_flag` | Active flagged organizer or conference meeting red flag criteria |
| `disputed` | Subject to an active dispute review process |
| `resolved` | Prior flag has been removed or dispute resolved successfully |
| `unverified` | Suspicious behavior reported but awaiting formal evidence links |

---

## Criteria for Classification

Entries may be classified based on meeting **3 or more** of the following criteria, or **1 major criterion**:

### Major Criteria (any single one is sufficient for `suspected`)

1. **FTC / government enforcement action** — Organization has been formally charged with deceptive practices by a government body
2. **Near-duplicate name abuse** — Deliberately adopts names nearly identical to legitimate, established conferences
3. **Mass simultaneous events** — Organizes hundreds of conferences on the same dates at the same venue across wildly unrelated fields
4. **Documented non-delivery** — Has a history of canceling events after collecting fees, or events that do not take place as described

### Supporting Criteria (3+ for `suspected`)

5. **No legitimate peer review** — Accepts papers without substantive review; allows anyone to purchase a speaking slot
6. **Fake indexing claims** — Falsely claims proceedings are indexed in Scopus, Web of Science, IEEE Xplore, or similar
7. **Aggressive spam** — Sends mass unsolicited invitations with misleading claims
8. **Opaque organization** — No verifiable committee, unclear or false headquarters address
9. **Predatory publisher affiliation** — Directly associated with a known predatory publisher (e.g., OMICS affiliate)
10. **Overly broad scope** — Conference titles like "International Conference on Science and Technology" with no specific focus
11. **Tourist destination framing** — Marketing heavily emphasizes venue/tourism over academic program
12. **Grammatical errors** — Website and communications contain significant grammatical or spelling errors suggesting unprofessional operation
13. **Guaranteed acceptance** — Promises publication/acceptance before any review
14. **Bundled fee exploitation** — Registration fees bundled with hotel/tours in ways that obscure actual costs

---

## What This Dataset is NOT

- Not a complete list — new predatory conferences emerge constantly
- Not legal accusation — `suspected` entries reflect patterns, not proven wrongdoing
- Not a comment on individual researchers who may have unknowingly attended these events
- Not applicable to legitimate low-prestige conferences — low quality ≠ predatory

---

## Boundary Cases

**Regional/emerging conferences**: A conference that is small, poorly organized, or low-quality is not automatically predatory. Predatory behavior requires intentional deception and exploitation.

**One-off events**: Single events that go poorly are not added to this list. We focus on organizers with patterns of behavior.

**Disputed legitimacy**: Some organizers (e.g., WSEAS, INASE) are debated in the community. We mark these `suspected` and link to both supporting and counter-evidence where available.

---

## Removal Process

If you believe an entry is incorrect:
1. Open a GitHub dispute request using our [Dispute Issue Template](https://github.com/callforpaper/predatory-conferences/issues/new?template=dispute-flag.yml).
2. Provide counter-evidence as detailed in [methodology.md](../methodology.md).
3. Maintainers will review the dispute and log outcomes inside the disputes registry.

---

## References

- [Think. Check. Attend.](https://thinkcheckattend.org) — researcher checklist
- [Beall's Criteria](https://beallslist.net) — original criteria for predatory journals
- [FTC OMICS Action](https://www.ftc.gov/news-events/news/press-releases/2019/04/federal-trade-commission-charges-academic-publisher-deceived-researchers)
- [Nature Editorial on Predatory Conferences (2024)](https://www.nature.com/articles/d41586-024-02218-z)
