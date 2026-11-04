# Repository Guidelines

## Project Structure and Module Organization
This repository contains the static GitHub profile for Muhammad Abubakar, not application source. The public entry point is `README.md`; the design system is authored in `DESIGN.md` with YAML front matter and rules; product context and evidence live in `PRODUCT.md`; banner artwork lives in `assets/banner-dark.svg` and `assets/banner-light.svg`; design context is mirrored in `.impeccable/design.json`.

## Design and Content Standards
- GitHub profile pages use static GitHub-Flavored Markdown; do not introduce CSS, JavaScript, or live components.
- Use the single monospace stack and phosphor color system defined in `DESIGN.md`.
- Reserve bright phosphor (`#33FF66` dark / `#0F5132` light) for the `whoami` keyword, display name, and cursor only.
- Keep every line in fenced code blocks at or under 36 characters.
- Write status, deploy-log, and stack blocks as terminal output (`[ok] ...`, indented role lines), not ordinary prose.
- Do not introduce unsupported metrics, claims, or project details; source evidence is in `PRODUCT.md`.

## Build, Test, and Development Commands
No build, test, lint, or format pipeline is configured.
- Preview by rendering `README.md` through GitHub.
- Validate GFM and SVG manually; no local build command is available.

## Coding Style and Naming Conventions
- Markdown: GFM, fenced blocks use `text` or `yaml`.
- Design YAML front matter: two-space indentation.
- SVG: kebab-case filenames, 1200×320 viewBox, `width="100%"`, dark/light siblings.
- Preserve terminal layout and column discipline.

## Testing Guidelines
- No automated tests or coverage requirements apply.
- Manually verify fenced-line length, banner parity, links, and accuracy.
- Check dark and light banner variants remain structurally synchronized.

## Commit and Pull Request Guidelines
- No Git history was available in this checkout, so no historical commit convention could be inferred; use concise, imperative subjects such as `docs: tighten terminal status readout`.
- Pull requests should include a clear description, linked issue where applicable, and screenshots for visual or content changes.
- Show before/after screenshots for banner or README edits and confirm design claims remain evidence-backed.
