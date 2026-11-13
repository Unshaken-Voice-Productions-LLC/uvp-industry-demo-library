# Repository guidance

This is a public curated library of 14 fictional static industry demos. The private source archive, customer records, original imagery, transaction records and proprietary internals must remain excluded. LICENSE is pending; public visibility is not an open-source grant. Security concerns go to the private channel in SECURITY.md.

## Authoritative paths

- `07_PORTFOLIO_INDEX/portfolio.json`: current catalog manifest.
- `tools/build_catalog.py`: generates the catalog HTML and copies site source files into dist.
- `07_PORTFOLIO_INDEX/catalog.css` and `catalog.js`: shared catalog presentation and local filtering.
- `03_RECONSTRUCTED_SITES/<industry>/<slug>/source`: authoritative site assets; rebuild dist after editing.
- `01_INVENTORY` and `05_REPORTS`: historical reconstruction records. Do not restore excluded private pipeline stages.
- `tests`: Python integrity checks and Node catalog interaction checks.

Run the build/check/test commands in README. There are no runtime packages or services. Keep the fictional disclosures, noindex/nofollow, CSP form-action/connect-src restrictions and simulated forms. Do not add real client identities, tracking, authentication, checkout, uploads or backend connections. Do not describe illustrative cards as operational business features. Do not claim manual accessibility or runtime QA was performed merely because static checks pass.
