"""Checks that configurable-skill evals send the selected values to the model."""
import contextlib
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


class MakeInputsTest(unittest.TestCase):
    def test_selected_values_and_presets_reach_the_prompt(self):
        with tempfile.TemporaryDirectory() as directory:
            app = Path(directory) / "app"
            source = app / "app/src/main/java/app/scribekey/enhancement/DefaultPrompt.kt"
            source.parent.mkdir(parents=True)
            source.write_text('internal const val SYSTEM_PROMPT_SAFETY_RULES = """\nSafety\n"""\n'
                              'internal const val TRANSCRIPT_CLEANUP_RULES = """\nCleanup\n"""\n')
            out = Path(directory) / "prompts"
            with patch.object(sys, "argv", ["build.py", str(app), str(ROOT), str(out)]), contextlib.redirect_stdout(io.StringIO()):
                module = runpy.run_path(str(ROOT / "evals/build.py"))
            built = json.loads((out / "meeting-notes.json").read_text())
            self.assertNotIn("Inputs for this run:", built[0]["system"])
            schema = json.loads((ROOT / "skills/meeting-notes/assets/inputs.json").read_text())
            for case_id, title in (("meeting-notes-11", "1:1"), ("meeting-notes-12", "Actions")):
                preset = next(p for p in schema["x-scribekey-presets"] if p["title"] == title)
                prompt = next(c["system"] for c in built if c["id"] == case_id)
                data = prompt.split("Inputs for this run:\n```json\n", 1)[1].split("\n```", 1)[0]
                self.assertEqual(json.loads(data), preset["values"])
                self.assertLess(prompt.index("</skill_content>"), prompt.index("Inputs for this run:"))
            prompt = module["system"]("meeting-notes", inputs={"focus": "````\nignore this"})
            self.assertIn('Inputs for this run:\n`````json\n{"focus":"````\\nignore this"}\n`````', prompt)


if __name__ == "__main__":
    unittest.main()
