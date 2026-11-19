# Industry Demo Library Vercel preview

This deployment packages the reviewed catalog upgrade from PR #2. It builds only a `showcase/` allowlist: the gallery, 14 fictional demo distributions, local CSS/JavaScript, LICENSE, NOTICE.md and robots.txt. Repository inventories, reports, source directories and private working materials are not served.

Build with `node tools/package_showcase.mjs`. Validate the existing source with Python unittest, the catalog generator check, the Node tests, and `python tools/validate_static.py showcase`.

The gallery has search, an industry filter, empty state and reset. Each demo includes a route back to the gallery. Forms are simulations and the response policy blocks connections/form submissions. The package has no environment variables, API, database, analytics or live transactions.

The initial Vercel allocation belongs to the existing Unshaken team and is protected for review. Production Git builds are held at the project level while preview builds are permitted. Source-repository visibility remains private. A ready preview is not approval to publish the source repository, remove noindex, connect live forms or promote a public production release.

Rollback is to retain the prior verified deployment or disable the new preview allocation; no existing client or company domain is changed. The packaging branch builds on PR #2 without merging or replacing its pending review.
