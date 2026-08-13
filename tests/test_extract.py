import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from extract import slugify, word_count, split_by_regex_or_whole  # noqa: E402


class TestSlugify(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Chapter One"), "chapter-one")

    def test_strips_punctuation(self):
        self.assertEqual(slugify("Part 2: The Rise!"), "part-2-the-rise")

    def test_empty_falls_back_to_section(self):
        self.assertEqual(slugify(""), "section")

    def test_truncates_to_max_len(self):
        long_title = "word " * 30
        self.assertLessEqual(len(slugify(long_title, max_len=20)), 20)


class TestWordCount(unittest.TestCase):
    def test_counts_words(self):
        self.assertEqual(word_count("one two three"), 3)


class TestSplitByRegexOrWhole(unittest.TestCase):
    def test_no_chapters_returns_single_section(self):
        sections = split_by_regex_or_whole("just some prose\nwith no markers")
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0][2], "single_section")

    def test_splits_on_chapter_markers(self):
        text = "Chapter 1\nfirst content\nChapter 2\nsecond content"
        sections = split_by_regex_or_whole(text)
        self.assertEqual(len(sections), 2)
        self.assertTrue(sections[0][0].startswith("Chapter 1"))
        self.assertTrue(sections[1][0].startswith("Chapter 2"))

    def test_recognizes_italian_markers(self):
        text = "Capitolo 1\ntesto"
        sections = split_by_regex_or_whole(text)
        self.assertEqual(sections[0][2], "regex_chapter")


if __name__ == "__main__":
    unittest.main()
