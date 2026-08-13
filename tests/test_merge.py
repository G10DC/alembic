import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from merge import extract_terms_from_text  # noqa: E402


class TestExtractTermsFromText(unittest.TestCase):
    def test_extracts_term_and_definition(self):
        terms = extract_terms_from_text("- **quorum**: il numero minimo di presenti richiesto", 1)
        self.assertIn("quorum", terms)
        self.assertEqual(terms["quorum"], ["il numero minimo di presenti richiesto"])

    def test_strips_leading_verb_phrases(self):
        terms = extract_terms_from_text("* **delibera** è un atto formale dell'organo", 1)
        self.assertEqual(terms["delibera"], ["un atto formale dell'organo"])

    def test_ignores_heading_lines(self):
        terms = extract_terms_from_text("# **not a term** heading", 1)
        self.assertEqual(terms, {})

    def test_ignores_blank_lines(self):
        terms = extract_terms_from_text("\n\n", 1)
        self.assertEqual(terms, {})

    def test_two_terms_on_one_line_split_definitions_correctly(self):
        line = "**alpha**: first def **beta**: second def"
        terms = extract_terms_from_text(line, 1)
        self.assertIn("alpha", terms)
        self.assertIn("beta", terms)
        self.assertEqual(terms["beta"], ["second def"])

    def test_short_definitions_are_dropped(self):
        # Definitions of length <= 3 after cleanup are filtered out.
        terms = extract_terms_from_text("**x**: ab", 1)
        self.assertEqual(terms, {})


if __name__ == "__main__":
    unittest.main()
