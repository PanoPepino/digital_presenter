import tempfile
import unittest
from pathlib import Path

import numpy as np
from manim import RIGHT, Square, UP
from manim_digital_presenter import load_csv_dialogue
from manim_digital_presenter.script_controller.actions import parse_value, resolve_action
from manim_digital_presenter.script_controller.models import DialogueEntry


class CsvTests(unittest.TestCase):
    def write(self, content):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        file = Path(directory.name) / "dialogue.csv"
        file.write_text(content, encoding="utf-8")
        return file

    def test_optional_argument_blanks_and_quoted_delimiter(self):
        file = self.write('\ufeff"hello/world"/happy\n\n  / / \nnext/look_at/UP\n')
        self.assertEqual(load_csv_dialogue(file),
                         (["hello/world", "next"], ["happy", "look_at"], ["", "UP"]))

    def test_existing_example_scripts_and_trailing_delimiters(self):
        root = Path(__file__).resolve().parents[1] / "examples/dialogue"
        for file in root.glob("*.csv"):
            dialogue, actions, arguments = load_csv_dialogue(file)
            self.assertTrue(dialogue)
            self.assertEqual(len(dialogue), len(actions))
            self.assertEqual(len(dialogue), len(arguments))
        self.assertEqual(load_csv_dialogue(self.write("look/look_at/UP/"))[2], ["UP"])

    def test_empty_file(self):
        self.assertEqual(load_csv_dialogue(self.write("\n")), ([], [], []))

    def test_invalid_rows_have_line_context(self):
        for row in ("only", "hello/happy/x/extra", "hello//"):
            with self.assertRaisesRegex(ValueError, r"dialogue.csv:2:"):
                load_csv_dialogue(self.write("ok/happy\n" + row))

    def test_argument_resolution(self):
        array = parse_value("UP")
        array[0] = 999
        np.testing.assert_equal(parse_value("UP"), UP)
        np.testing.assert_equal(parse_value("[1, 2, 3]"), [1, 2, 3])
        self.assertEqual(parse_value("2.5"), 2.5)
        self.assertEqual(parse_value("literal text"), "literal text")
        target = object()
        self.assertIs(parse_value("target", {"target": target}), target)

    def test_custom_actions_and_builders(self):
        square = Square()
        entry = DialogueEntry("", "move", "RIGHT", 7)
        animation = resolve_action(square, entry,
                                   actions={"move": lambda value: square.animate.shift(value)},
                                   run_time=0.5)
        self.assertEqual(animation.run_time, 0.5)
        np.testing.assert_allclose(animation.target_mobject.get_center(), RIGHT)

    def test_invalid_actions_have_context(self):
        for action in ("_private", "does_not_exist", "shift"):
            with self.assertRaisesRegex(ValueError, "script:7:"):
                resolve_action(Square(), DialogueEntry("", action, "UP", 7))
