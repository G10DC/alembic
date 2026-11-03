"""Test di merge.py e chunk.py eseguiti come script (stdlib, unittest)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def run(script, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *map(str, args)],
        capture_output=True, text=True, encoding="utf-8",
    )


CHUNK_1 = """## 1. Perché l'organizzazione: è così?

🔴 Sicuro: la **delibera** è l'atto formale dell'organo collegiale.

**Quorum**: numero minimo di presenti.

## Domande di verifica

Domanda: Che cos'è una delibera?
Risposta: L'atto formale dell'organo collegiale.
"""

CHUNK_2 = """## 2. Controlli

**Quorum**: maggioranza necessaria per votare.

❌ "il quorum è sempre metà" → ✅ dipende dall'organo
"""


class TestMerge(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        (self.dir / "chunk_1.md").write_text(CHUNK_1, encoding="utf-8")
        (self.dir / "chunk_2.md").write_text(CHUNK_2, encoding="utf-8")
        self.out = self.dir / "guida.md"

    def tearDown(self):
        self.tmp.cleanup()

    def merged(self, *extra):
        r = run("merge.py", self.dir, "--output", self.out, *extra)
        self.assertEqual(r.returncode, 0, r.stderr)
        return self.out.read_text(encoding="utf-8")

    def test_title_option_and_default(self):
        self.assertTrue(self.merged("--title", "Diritto Amministrativo").startswith("# Diritto Amministrativo\n"))
        self.assertTrue(self.merged().startswith("# Guida di studio\n"))

    def test_single_h1(self):
        text = self.merged()
        self.assertEqual(sum(1 for l in text.splitlines() if l.startswith("# ")), 1)

    def test_toc_slug_accents_and_apostrophes(self):
        text = self.merged()
        self.assertIn("(#1-perché-lorganizzazione-è-così)", text)
        self.assertIn("(#2-controlli)", text)

    def test_glossary_from_definitions_with_chapter_labels(self):
        text = self.merged()
        glossary = text.split("## Glossario", 1)[1]
        self.assertIn("**Quorum**: numero minimo di presenti. (cap. 1)", glossary)
        self.assertIn("**Quorum**: maggioranza necessaria per votare. (cap. 2)", glossary)
        # Le righe con marcatori di priorità o trappole non sono definizioni.
        self.assertNotIn("delibera**:", glossary)

    def test_questions_gathered_in_one_final_section(self):
        text = self.merged()
        self.assertEqual(text.count("## Domande di verifica"), 1)
        self.assertLess(text.index("## 2. Controlli"), text.index("## Domande di verifica"))
        self.assertIn("Domanda: Che cos'è una delibera?\nRisposta: L'atto formale", text)

    def test_nonconforming_name_gives_clear_error(self):
        (self.dir / "capitolo_3.md").write_text("## 3. X\n", encoding="utf-8")
        r = run("merge.py", self.dir, "--output", self.out)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("capitolo_3.md", r.stderr)
        self.assertNotIn("Traceback", r.stderr)

    def test_empty_dir_gives_clear_error(self):
        empty = self.dir / "vuota"
        empty.mkdir()
        r = run("merge.py", empty, "--output", self.out)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("Traceback", r.stderr)


class TestChunkManifest(unittest.TestCase):
    def test_original_moved_and_manifest_consistent(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            sec = out / "sections"
            sec.mkdir()
            files = []
            for i, name in enumerate(["001_a.txt", "002_grande.txt", "003_c.txt"], start=1):
                f = sec / name
                f.write_text(("parola " * 8 + "\n\n") * (6 if i == 2 else 1), encoding="utf-8")
                files.append(f)
            manifest = [
                {"index": i, "title": f"T{i}", "path": str(f), "word_count": 8, "detection_method": "x"}
                for i, f in enumerate(files, start=1)
            ]
            (out / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

            r = run("chunk.py", files[1], "--outdir", out, "--max-words", 20)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertFalse(files[1].exists())
            self.assertTrue((sec / "_split" / files[1].name).exists())

            m = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual([e["index"] for e in m], list(range(1, len(m) + 1)))
            paths = [e["path"] for e in m]
            self.assertEqual(len(paths), len(set(paths)))
            self.assertNotIn(str(files[1]), paths)
            self.assertEqual(paths[0], str(files[0]))
            self.assertEqual(paths[-1], str(files[2]))
            self.assertGreater(len(m), 3)
            self.assertTrue(all(Path(p).exists() for p in paths))
            self.assertTrue(m[1]["title"].startswith("T2 (parte 1/"))


if __name__ == "__main__":
    unittest.main()
