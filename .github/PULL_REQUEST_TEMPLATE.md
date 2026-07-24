### Pull Request Checklist

Before submitting this PR, please ensure:
- [ ] Any added/modified organizer or conference files validate locally via `python scripts/validate_entities.py`.
- [ ] Every `evidence_refs` references a valid item `id` inside the same file's `evidence` array.
- [ ] No slugs collide with existing entries.
- [ ] Raw HTML files are stored in `evidence/<slug>/...` and referenced correctly.
- [ ] Binary screenshot files (e.g. `.png`) are tracked under Git LFS.
- [ ] I have read the [CONTRIBUTING.md](CONTRIBUTING.md) guide.

Thank you for helping protect the research community!
