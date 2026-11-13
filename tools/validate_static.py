"""Validate local HTML references and fictional-demo safety boundaries, without network access."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.metas = {}
        self.forms = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == 'meta':
            key = data.get('name', data.get('http-equiv', '')).lower()
            self.metas[key] = data.get('content', '')
        if tag == 'form':
            self.forms.append(data)
        for key in ('href', 'src', 'action'):
            if data.get(key):
                self.references.append(data[key])


def validate_page(path: Path, root: Path) -> list[str]:
    errors = []
    page = Page()
    page.feed(path.read_text(encoding='utf-8-sig'))
    for reference in page.references:
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            errors.append(f'External reference: {reference}')
            continue
        if not url.path:
            continue
        target = (path.parent / unquote(url.path)).resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            errors.append(f'Missing or escaping reference: {reference}')
    robots = page.metas.get('robots', '').replace(' ', '').lower()
    if robots != 'noindex,nofollow':
        errors.append('Missing noindex,nofollow directive')
    policy = page.metas.get('content-security-policy', '')
    directives = {part.strip() for part in policy.split(';')}
    for directive in ("form-action 'none'", "connect-src 'none'", "object-src 'none'", "base-uri 'none'"):
        if directive not in directives:
            errors.append(f'Missing safety directive: {directive}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path, help='Static site or library directory to check')
    args = parser.parse_args()
    root = args.directory.resolve()
    pages = list(root.rglob('*.html')) if root.is_dir() else []
    if not pages:
        parser.exit(1, 'No HTML pages found.\n')
    errors = []
    for page in pages:
        for message in validate_page(page, root):
            errors.append(f'{page.relative_to(root)}: {message}')
    for error in errors:
        print(error)
    print(f'Checked {len(pages)} pages; {len(errors)} issue(s).')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
