import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from coverage import tokenize, significant_terms, load_original  # noqa: E402


class TestTokenize(unittest.TestCase):
    def test_splits_words(self):
        self.assertEqual(tokenize("hello world"), ["hello", "world"])

    def test_strips_italian_elisions(self):
        # "l'energia" should yield "energia", not "l energia" or "lenergia"
        self.assertIn("energia", tokenize("l'energia rinnovabile"))
        self.assertNotIn("lenergia", tokenize("l'energia rinnovabile"))

    def test_lowercases(self):
        self.assertEqual(tokenize("HELLO World"), ["hello", "world"])

    def test_keeps_internal_hyphens(self):
        self.assertIn("multi-livello", tokenize("sistema multi-livello"))


class TestSignificantTerms(unittest.TestCase):
    def test_drops_stopwords(self):
        terms = significant_terms("il gatto e il cane sono animali", min_len=3)
        self.assertNotIn("che", terms)
        self.assertIn("gatto", terms)

    def test_drops_short_tokens(self):
        terms = significant_terms("a bb ccc dddd", min_len=4)
        self.assertEqual(terms, ["dddd"])


class TestLoadOriginal(unittest.TestCase):
    def test_reads_single_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "a.txt"
            f.write_text("hello", encoding="utf-8")
            self.assertEqual(load_original(str(f)), "hello")

    def test_reads_directory_of_txt_files_in_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "001.txt").write_text("first", encoding="utf-8")
            (tmp / "002.txt").write_text("second", encoding="utf-8")
            (tmp / "notes.md").write_text("ignored", encoding="utf-8")
            result = load_original(str(tmp))
            self.assertIn("first", result)
            self.assertIn("second", result)
            self.assertNotIn("ignored", result)


class TestLoadOriginalSkipsSplit(unittest.TestCase):
    def test_split_subfolder_is_not_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "a.txt").write_text("alfa", encoding="utf-8")
            (tmp / "_split").mkdir()
            (tmp / "_split" / "orig.txt").write_text("duplicato", encoding="utf-8")
            text = load_original(tmp)
            self.assertIn("alfa", text)
            self.assertNotIn("duplicato", text)


class TestCoverageEndToEnd(unittest.TestCase):
    def test_reports_missing_and_present_terms(self):
        import subprocess
        import json

        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            original = tmp / "original.txt"
            condensed = tmp / "condensed.md"
            report = tmp / "report.json"
            # "importante" repeated enough to be a top term; only "presente" survives condensing.
            original.write_text("importante importante importante presente presente", encoding="utf-8")
            condensed.write_text("presente", encoding="utf-8")

            script = Path(__file__).parent.parent / "scripts" / "coverage.py"
            result = subprocess.run(
                [sys.executable, str(script), "--original", str(original),
                 "--condensed", str(condensed), "--report", str(report), "--min-len", "4"],
                capture_output=True, text=True, encoding="utf-8",
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(report.read_text(encoding="utf-8"))
            missing_terms = [m["term"] for m in data["missing_terms"]]
            self.assertIn("importante", missing_terms)
            self.assertLess(data["coverage_pct"], 100.0)


if __name__ == "__main__":
    unittest.main()
