# UVP Industry Demo Library

Explore 14 fictional industry website concepts. Every demo is static HTML/CSS/JavaScript with local assets, sample content and a simulated inquiry form. No accounts, payment processing, analytics or external services are connected.

## Explore

From the repository root:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/07_PORTFOLIO_INDEX/`. Search by name, industry or feature, select an industry, and explore a demo. The generated catalog also contains all links without JavaScript. No build is needed to browse the committed files.

These are variations on a shared layout. Feature cards describe illustrative service categories; they are not working booking, checkout, content-feed or business-management applications. All identities are fictional.

## Build and validate

Requires Python 3.11+. No Python runtime dependencies.

```bash
python tools/build_catalog.py
python tools/build_catalog.py --check
python -m unittest discover -s tests -v
node --test tests/catalog.test.cjs
```

Node is only needed for the catalog interaction tests; it is not needed to build or browse the demos. `portfolio.json` supplies catalog cards at build time. The builder synchronizes each `source/` into its deployable `dist/`; CI rejects stale output. Edit `source/`, then rebuild. The numbered inventory and reports are historical reconstruction records, not the catalog's runtime source.

## Reuse boundaries

The catalog builder and validator are small, reusable examples of standard-library static tooling. No source archive or private records are included. Demo forms are blocked from submitting by both their local handler and Content Security Policy. Keep the simulated forms, fictional disclosure and noindex/nofollow directives when extending the library.

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [PUBLIC_RELEASE_BOUNDARY.md](PUBLIC_RELEASE_BOUNDARY.md) and [LICENSE](LICENSE). Public visibility does not yet grant an open-source license.
