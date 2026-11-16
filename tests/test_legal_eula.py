"""The licence page cannot ship a placeholder."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


build = _load("build-legal-eula")
check = _load("check-legal-eula")

FINAL = "# T\n\nVersion 1.0\n\n**1. Licence.** You may install it. See https://blindsight.io/privacy-policy/.\n\n**2. Law.** Swiss law applies.\n"
DRAFT = "# T\n\n**1. Licence.** Pay [amount].\n\n**2. Law.** Write to <legal contact address>.\n"


class LegalEulaPage(unittest.TestCase):
    def test_a_draft_builds_a_notice_with_none_of_the_text(self):
        page, final = build.build(DRAFT, "0.1", "2026-11-16")
        self.assertFalse(final)
        self.assertNotIn("Pay", page)
        self.assertNotIn("legal contact", page)
        self.assertIn("being finalised", page)
        self.assertIn('content="noindex, nofollow"', page)
        self.assertEqual(check.problems(page), [])

    def test_a_final_text_builds_the_full_page(self):
        page, final = build.build(FINAL, "1.0", "2026-12-01")
        self.assertTrue(final)
        self.assertIn("<h2>1. Licence.</h2>" if "<h2>1. Licence.</h2>" in page else "<h2>1. Licence.", page)
        self.assertIn("Swiss law applies", page)
        self.assertIn("Version 1.0, published 2026-12-01", page)
        self.assertNotIn("noindex", page)
        self.assertEqual(check.problems(page), [])

    def test_the_checker_catches_a_page_that_shows_a_placeholder(self):
        bad, _ = build.build(FINAL, "1.0", "2026-12-01")
        bad = bad.replace("Swiss law applies", "Swiss law applies in [city]")
        self.assertTrue(check.problems(bad))

    def test_require_final_refuses_a_draft(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "t.md"
            src.write_text(DRAFT)
            out = Path(d) / "o" / "index.html"
            r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build-legal-eula.py"), str(src), "--require-final", "--out", str(out)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertFalse(out.exists())

    def test_the_committed_page_passes_the_check(self):
        self.assertEqual(subprocess.run([sys.executable, str(ROOT / "scripts" / "check-legal-eula.py")]).returncode, 0)


if __name__ == "__main__":
    unittest.main()
