# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not an application** — it's a sanitized, public-release deliverable produced by Unshaken Voice Productions (UVP): a library of 14 fictional static "demo" websites (the "Aleph" brand family), one per industry vertical, plus the audit/compliance paperwork proving each site was scrubbed of real client data before publication.

This repo is a *derivative* of a private UVP working repository. Per `PUBLIC_RELEASE_BOUNDARY.md`, the private source repo must never be made public, and this candidate must never contain private Git history, credentials, customer/client records, real business documents, or proprietary UVP/Aleph internals. `LICENSE` currently states the license is **pending final approval** — treat this repo as **not open source** until that changes. Final publication (making the repo publicly visible) requires explicit approval from "Steven" (see `PUBLIC_RELEASE_BOUNDARY.md`).

Report security/privacy concerns to admin@unshakenvoice.tech per `SECURITY.md` — never in a public issue.

## Repository layout

Top-level directories are numbered stages of a sanitization pipeline. The numbering has gaps (no `02_`, `04_`, `06_`) because the interim/private stages — the original uploaded archive and extracted working copies — are intentionally excluded from this public deliverable (see root `README.md` and `PUBLIC_RELEASE_BOUNDARY.md`). Don't try to recreate those missing stages; their absence is a deliberate privacy boundary, not a gap to fill.

- **`01_INVENTORY/`** — `master_inventory.csv` / `master_inventory.json` (same data, two formats): one row per original private folder (e.g. `"Trucking Site"`) mapping it to its sanitized public identity (e.g. `"Aleph Logistics"`), industry, risk flags, and `disposition` (all currently `approved_for_conversion`).
- **`03_RECONSTRUCTED_SITES/<industry>/<aleph-slug>/`** — the 14 actual demo sites, one directory per site, grouped by industry folder. See "Architecture" below.
- **`05_REPORTS/`** — library-wide audit docs: `MASTER_CONVERSION_REPORT.md` (executive summary of the whole conversion), `QUARANTINE_REGISTER.md` (what was deliberately excluded — original imagery, operational/customer records, PHP/DB/auth/checkout code, executables), `SECURITY_AND_PRIVACY_NOTICE.md`.
- **`07_PORTFOLIO_INDEX/`** — `index.html`, the browsable entry point linking to every demo, plus `portfolio.json`, a machine-readable manifest of the same 14 sites. **`index.html` does not fetch `portfolio.json`** — the article cards are hand-authored directly in the HTML. Treat `portfolio.json` as a separately-maintained duplicate, not a data source the page reads at runtime.

## Working with the sites

There is **no package manager, build step, linter, or test suite** anywhere in this repo (`01_INVENTORY/master_inventory.*` explicitly records `package_manager: none`, `build_command: none` for every site). Everything is hand-authored, already-minified static HTML/CSS/JS.

To preview a single demo:
```
open 03_RECONSTRUCTED_SITES/<industry>/<slug>/dist/index.html
```
or serve it (needed only if a site ever depends on relative fetches):
```
python3 -m http.server --directory 03_RECONSTRUCTED_SITES/<industry>/<slug>/dist
```

To browse the whole library the way a visitor would, open `07_PORTFOLIO_INDEX/index.html` directly (its links are relative paths up to `03_RECONSTRUCTED_SITES/`, so this works straight from the filesystem — no server required).

**`source/` and `dist/` are byte-identical in every one of the 14 sites** — there is no actual build/minification step turning one into the other; `dist/` is simply the deployable copy. If you edit a site, edit `source/` and mirror the same change into `dist/` (or vice versa). Before committing a site change, it's worth confirming they still match:
```
diff -rq 03_RECONSTRUCTED_SITES/<industry>/<slug>/source 03_RECONSTRUCTED_SITES/<industry>/<slug>/dist
```

## Architecture: one shared template, fourteen skins

The 14 sites are **not independently written** — they render from a single shared HTML skeleton, a single shared `styles.css`, and a single shared `script.js` (all three files are byte-for-byte identical across all 14 `source/` directories; verified via `md5sum */*/source/{script.js,styles.css}`). What varies per site is:

1. **Text content** — title, meta description, hero heading/copy, three feature-card headings/blurbs, footer text.
2. **Three CSS custom properties**, set inline on `<body style="--bg:…;--accent:…;--paper:…">`, which drive the entire color theme (background/ink, accent, paper/surface). This is the *only* visual differentiation between sites — there is no per-site CSS file.
3. Occasionally one extra industry-specific micro-line (e.g. the clothing site adds `"Products and prices are illustrative. Checkout is disabled."`).

Every site's HTML follows the same section structure: skip link → sticky header (`brand` + nav + "UVP Demo Site" badge) → `<section id="services">` (3 feature cards) → `<section id="process">` (3-step list) → `<section id="contact">` (a simulated inquiry form) → footer with the mandatory fictional-demo disclosure sentence.

The shared `script.js` only wires up the contact form to **prevent default submission, show a "Demonstration complete — no information was submitted or stored." status message, and reset the form** — nothing is ever transmitted anywhere. Every page also carries `<meta name="robots" content="noindex,nofollow">`. **These are load-bearing privacy/compliance behaviors, not incidental defaults** — if you add a new site or touch the template, preserve all three (simulated-only form, noindex/nofollow, no external calls/analytics).

**Implication for changes:** a global tweak (layout, accessibility, copy pattern shared by all sites) means editing the template once and propagating it into all 14 `source/`+`dist/` pairs, since nothing here is templated at build time — it was templated once by hand and then forked into 14 static copies. A single-site change (new copy, new accent color) touches only that site's four content files.

### Per-site file set

Each `03_RECONSTRUCTED_SITES/<industry>/<slug>/` directory has the same six docs plus the two code dirs:

| File | Per-site or boilerplate? | Contents |
|---|---|---|
| `README.md` | per-site | Industry, site type, framework, run instructions, feature list |
| `DEMO_DISCLOSURE.md` | per-site | "This is a fictional demonstration identity..." statement |
| `RECONSTRUCTION_REPORT.md` | per-site | Source package ID → new identity mapping, disposition, known limitations |
| `ASSET_REGISTER.md` | **identical boilerplate** across all 14 sites | Classifies each file as `replacement_generated`; original images marked `quarantined` |
| `QA_REPORT.md` | **identical boilerplate** across all 14 sites | Fixed 10-row PASS checklist (static build, keyboard access, reduced motion, form transmission disabled, etc.) |
| `DEPLOYMENT.md` | **identical boilerplate** across all 14 sites | "Deploy `dist/` to any static host... no env vars, database, or server runtime required" |
| `source/`, `dist/` | per-site content, shared template | `index.html`, `script.js`, `styles.css` (byte-identical `dist`↔`source`) |

## The three parallel manifests — keep them in sync by hand

The same 14-site catalog is described independently in three places, and **none of them are generated from the others**:

1. `01_INVENTORY/master_inventory.csv` + `.json` — the audit trail (original private folder name → sanitized identity, risk disposition).
2. `07_PORTFOLIO_INDEX/portfolio.json` — public-facing manifest (id, name, industry, features, `demoPath`).
3. `07_PORTFOLIO_INDEX/index.html` — the actual rendered cards visitors click through, hand-authored inline (not populated from #2).

If you add, rename, or remove a site, update all three, plus the per-site `README.md`/`RECONSTRUCTION_REPORT.md`, plus `05_REPORTS/MASTER_CONVERSION_REPORT.md`'s counts — there is no single source of truth that propagates automatically.

## Content and compliance rules (do not violate these)

These are the actual constraints this repository exists to enforce (see `PUBLIC_RELEASE_BOUNDARY.md`, `05_REPORTS/QUARANTINE_REGISTER.md`, `05_REPORTS/SECURITY_AND_PRIVACY_NOTICE.md`):

- Never introduce real client/customer names, contacts, testimonials, transaction records, or business documents into any site or doc — every identity here (the "Aleph ___" companies) is fictional, and each site's footer/`DEMO_DISCLOSURE.md` must keep saying so.
- Never add real source imagery — image provenance/licensing was never established for the original assets, so they were deliberately excluded (`quarantined`), and generated/placeholder visuals (currently CSS-only shapes) are used instead.
- Never wire the contact/inquiry forms to a real backend, database, auth, checkout, or upload endpoint, and never add analytics/tracking scripts — `QA_REPORT.md`'s "Form transmission disabled" and "External APIs and analytics: none present" gates must keep passing.
- Keep `<meta name="robots" content="noindex,nofollow">` on every demo page unless explicitly told UVP wants the portfolio indexed.
- Don't reintroduce anything listed in `05_REPORTS/QUARANTINE_REGISTER.md` (operational records, invoices, PHP/DB/auth/checkout/admin functionality, executables).
