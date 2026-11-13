"""Build a portable, offline catalog from portfolio.json using only Python's standard library."""
from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "07_PORTFOLIO_INDEX"


def load_catalog(root: Path = ROOT) -> list[dict]:
    catalog = root / "07_PORTFOLIO_INDEX"
    items = json.loads((catalog / "portfolio.json").read_text(encoding="utf-8-sig"))
    if not isinstance(items, list) or not items:
        raise ValueError("The catalog must be a nonempty list")
    ids = set()
    paths = set()
    for item in items:
        for key in ("id", "name", "industry", "siteType", "description", "demoPath"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(f"Missing catalog field: {key}")
        if item["id"] in ids or item["demoPath"] in paths:
            raise ValueError("Catalog IDs and demo paths must be unique")
        ids.add(item["id"])
        paths.add(item["demoPath"])
        path = (catalog / item["demoPath"]).resolve()
        if not path.is_relative_to((root / "03_RECONSTRUCTED_SITES").resolve()) or path.name != "index.html" or path.parent.name != "dist":
            raise ValueError(f"Demo path must point to a local dist/index.html: {item['id']}")
        if not path.is_file():
            raise ValueError(f"Missing demo: {item['id']}")
        if not isinstance(item.get("features"), list) or not all(isinstance(x, str) for x in item["features"]):
            raise ValueError(f"Features must be a list of strings: {item['id']}")
    return items


def render_catalog(items: list[dict]) -> str:
    options = ''.join(f'<option value="{escape(x, quote=True)}">{escape(x)}</option>' for x in sorted({x['industry'] for x in items}))
    cards = []
    for index, item in enumerate(items, 1):
        search = ' '.join([item['name'], item['industry'], item['description'], *item['features']]).lower()
        features = ''.join(f'<li>{escape(x)}</li>' for x in item['features'])
        cards.append(f'''<article data-industry="{escape(item['industry'], quote=True)}" data-search="{escape(search, quote=True)}">
<div class="card-top"><span>{index:02d}</span><span>{escape(item['industry'])}</span></div>
<h2>{escape(item['name'])}</h2><p class="type">{escape(item['siteType'])}</p>
<p>{escape(item['description'])}</p><ul>{features}</ul>
<a class="demo-link" href="{escape(item['demoPath'], quote=True)}">Explore demo <span aria-hidden="true">↗</span></a></article>''')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'">
<meta name="description" content="Explore fictional industry website concepts by Unshaken Voice Productions. No tracking, accounts or live transactions.">
<title>Industry Demo Library | Unshaken Voice Productions</title><link rel="stylesheet" href="catalog.css"></head>
<body><a class="skip" href="#catalog">Skip to demos</a><header><a class="brand" href="index.html">UNSHAKEN VOICE PRODUCTIONS</a><span>Industry Demo Library</span></header>
<main><section class="intro"><p class="eyebrow">Ideas you can explore</p><h1>Different industries.<br>Clear possibilities.</h1>
<p>Browse {len(items)} fictional website concepts, from local services to learning and creative work. Explore the layouts and sample content at your own pace.</p>
<p class="disclosure">Every business shown is fictional. Forms are simulations: nothing is submitted or stored. No accounts, analytics or external services.</p></section>
<section aria-label="Find a demo" class="controls"><label>Search demos<input id="search" type="search" placeholder="Try automotive or learning" autocomplete="off"></label>
<label>Industry<select id="industry"><option value="">All industries</option>{options}</select></label><button id="reset" type="button">Reset filters</button></section>
<p id="count" role="status" aria-live="polite">{len(items)} demos</p><section id="catalog" class="grid" aria-label="Industry demos">{''.join(cards)}</section>
<p id="empty" hidden>No demos match. Try another search or reset the filters.</p><noscript><p>All demos are shown. Enable JavaScript to search and filter.</p></noscript></main>
<footer>Fictional demonstration websites by Unshaken Voice Productions LLC. See the repository LICENSE for reuse terms.</footer><script src="catalog.js"></script></body></html>
'''


def build(check: bool = False, root: Path = ROOT) -> list[str]:
    items = load_catalog(root)
    catalog = root / "07_PORTFOLIO_INDEX"
    stale = []
    outputs = {catalog / 'index.html': render_catalog(items).encode('utf-8')}
    for item in items:
        dist = (catalog / item['demoPath']).resolve().parent
        for source in sorted((dist.parent / 'source').iterdir()):
            if source.is_file():
                outputs[dist / source.name] = source.read_bytes()
    for path, payload in outputs.items():
        if not path.exists() or path.read_bytes() != payload:
            stale.append(str(path.relative_to(root)))
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(payload)
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated catalog or distribution files are stale')
    args = parser.parse_args()
    try:
        stale = build(args.check)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, f'Catalog error: {exc}\n')
    if args.check and stale:
        parser.exit(1, 'Stale generated files: ' + ', '.join(stale) + '\nRun python tools/build_catalog.py\n')
    print('Catalog checked.' if args.check else f'Catalog built; {len(stale)} files updated.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
