# Contributing to Predatory Conferences Database

Thank you for contributing to this open-source effort to protect researchers from predatory conferences.

---

## 📂 Repository Layout

- `/schema/entity.schema.json`: The JSON schema enforcing validations.
- `/organizers/<organizer-slug>.yaml`: Organizer entries.
- `/conferences/<organizer-slug>/<conference-slug>.yaml`: Specific conference entries.
- `/evidence/<slug>/`: Stored HTML snapshots and screenshot attachments.
- `/dist/`: Compiled output JSON lists (auto-generated, do not edit).

---

## 🛠️ How to Contribute

### 1. Through GitHub Issues
If you are not comfortable writing YAML, you can submit reports using the structured GitHub Issue Forms:
- [Report an Organizer](https://github.com/callforpaper/predatory-conferences/issues/new?template=report-organizer.yml)
- [Report a Conference](https://github.com/callforpaper/predatory-conferences/issues/new?template=report-conference.yml)
- [Submit New Evidence](https://github.com/callforpaper/predatory-conferences/issues/new?template=submit-evidence.yml)
- [Dispute a Flag](https://github.com/callforpaper/predatory-conferences/issues/new?template=dispute-flag.yml)

### 2. Through Pull Requests (YAML)
To edit or add files directly:
1. Fork the repository and clone it.
2. Ensure you have the validation requirements installed:
   ```bash
   pip install jsonschema pyyaml
   ```
3. Make your changes in `/organizers/` or `/conferences/`.
4. Run the validation script locally to check your changes:
   ```bash
   python scripts/validate_entities.py
   ```
5. Ensure your raw HTML snapshots are stored in `evidence/<slug>/`. If you add `.png` screenshots, make sure they are routed through git-lfs.
6. Open your pull request.

---

## ⚖️ Licensing
By contributing, you agree that your submissions are released under the [CC0 1.0 Universal License](LICENSE).
