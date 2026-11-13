import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build_catalog import build, load_catalog, render_catalog
from validate_static import validate_page


class LibraryTests(unittest.TestCase):
    def test_catalog_and_distribution_are_current(self):
        self.assertEqual(len(load_catalog()), 14)
        self.assertEqual(build(check=True), [])
        for source in (ROOT / '03_RECONSTRUCTED_SITES').glob('*/*/source'):
            dist = source.parent / 'dist'
            self.assertEqual({x.name for x in source.iterdir()}, {x.name for x in dist.iterdir()})
            for path in source.iterdir():
                self.assertEqual(path.read_bytes(), (dist / path.name).read_bytes())

    def test_all_pages_have_local_links_and_safety_policy(self):
        pages = list((ROOT / '03_RECONSTRUCTED_SITES').rglob('*.html')) + [ROOT / '07_PORTFOLIO_INDEX/index.html']
        self.assertEqual(len(pages), 29)
        for page in pages:
            with self.subTest(page=page):
                self.assertEqual(validate_page(page, ROOT), [])

    def test_each_demo_is_fictional_and_simulated(self):
        for path in (ROOT / '03_RECONSTRUCTED_SITES').glob('*/*/source/index.html'):
            with self.subTest(site=path.parent.parent.name):
                text = path.read_text()
                self.assertIn('fictional demonstration website', text)
                self.assertIn('No information entered here is transmitted or stored.', text)
                script = path.with_name('script.js').read_text()
                self.assertIn('preventDefault()', script)
                self.assertIn('no information was submitted or stored', script)

    def test_manifest_paths_cannot_escape_the_library(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '07_PORTFOLIO_INDEX').mkdir()
            item = dict(load_catalog()[0], demoPath='../../outside/index.html')
            (root / '07_PORTFOLIO_INDEX/portfolio.json').write_text(json.dumps([item]))
            with self.assertRaises(ValueError):
                load_catalog(root)

    def test_unsafe_manifest_text_is_escaped(self):
        item = dict(load_catalog()[0], name='<script>alert(1)</script>', description='"unsafe" & content')
        html = render_catalog([item])
        self.assertNotIn('<script>alert(1)</script>', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertIn('&amp; content', html)

    def test_stale_output_is_detected_and_rebuilt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'library'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.git', '__pycache__'))
            path = root / '07_PORTFOLIO_INDEX/index.html'
            path.write_text('stale')
            self.assertIn('07_PORTFOLIO_INDEX/index.html', build(check=True, root=root))
            build(root=root)
            self.assertEqual(build(check=True, root=root), [])

    def test_validator_catches_external_reference_and_missing_csp(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / 'index.html'
            page.write_text('<script src="https://example.com/script.js"></script>')
            issues = validate_page(page, Path(tmp))
            self.assertTrue(any('External reference' in x for x in issues))
            self.assertTrue(any('form-action' in x for x in issues))


if __name__ == '__main__':
    unittest.main()
