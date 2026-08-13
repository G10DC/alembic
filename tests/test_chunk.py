import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from chunk import word_count, chunk_paragraphs, chunk_title  # noqa: E402


class TestWordCount(unittest.TestCase):
    def test_counts_words(self):
        self.assertEqual(word_count("one two three"), 3)

    def test_empty_string(self):
        self.assertEqual(word_count(""), 0)

    def test_collapses_whitespace(self):
        self.assertEqual(word_count("one   two\nthree"), 3)


class TestChunkParagraphs(unittest.TestCase):
    def test_single_paragraph_under_limit_is_one_chunk(self):
        chunks = chunk_paragraphs("hello world", max_words=100)
        self.assertEqual(chunks, ["hello world"])

    def test_splits_when_over_limit(self):
        p1 = "word " * 10
        p2 = "word " * 10
        text = f"{p1.strip()}\n\n{p2.strip()}"
        chunks = chunk_paragraphs(text, max_words=15)
        self.assertEqual(len(chunks), 2)

    def test_keeps_paragraphs_together_under_limit(self):
        p1 = "word " * 5
        p2 = "word " * 5
        text = f"{p1.strip()}\n\n{p2.strip()}"
        chunks = chunk_paragraphs(text, max_words=15)
        self.assertEqual(len(chunks), 1)

    def test_oversized_single_paragraph_is_its_own_chunk(self):
        # A paragraph bigger than max_words on its own must not be dropped or split mid-word.
        huge = "word " * 50
        chunks = chunk_paragraphs(huge.strip(), max_words=10)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(word_count(chunks[0]), 50)

    def test_ignores_blank_paragraphs(self):
        text = "first\n\n\n\nsecond"
        chunks = chunk_paragraphs(text, max_words=100)
        self.assertEqual(chunks, ["first\n\nsecond"])


class TestChunkTitle(unittest.TestCase):
    def test_uses_first_line(self):
        self.assertEqual(chunk_title("Chapter One\nbody text", 1), "Chapter One")

    def test_falls_back_when_empty(self):
        self.assertEqual(chunk_title("", 3), "Chunk 3")

    def test_truncates_long_first_line(self):
        long_line = "x" * 80
        self.assertEqual(len(chunk_title(long_line, 1)), 50)


class TestChunkEndToEnd(unittest.TestCase):
    def test_main_writes_manifest_and_removes_source(self):
        import subprocess

        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            section = tmp / "001_big.txt"
            section.write_text(("para one is short.\n\n" * 3) + ("para two is short.\n\n" * 3), encoding="utf-8")
            script = Path(__file__).parent.parent / "scripts" / "chunk.py"

            result = subprocess.run(
                [sys.executable, str(script), str(section), "--outdir", str(tmp), "--max-words", "10"],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(section.exists(), "source file should be removed after chunking")
            self.assertTrue((tmp / "manifest.json").exists())
            self.assertTrue(any((tmp / "sections").glob("*.txt")))


if __name__ == "__main__":
    unittest.main()
