import tempfile
from pathlib import Path
from unittest.mock import patch

from manim import FadeIn, Square, VGroup
from manim_digital_presenter import Text_Box, script_sequencer

from common import ManimTest


class SequencerTests(ManimTest):
    def script(self, content):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        file = Path(directory.name) / "dialogue.csv"
        file.write_text(content)
        return file

    def test_empty_script_yields_nothing(self):
        self.assertEqual(list(script_sequencer(self.script("\n"), Square())), [])

    def test_transition_count_layout_and_duration(self):
        square = Square()
        box = Text_Box(width=2, height=1)
        texts = VGroup(Square(side_length=5), Square(side_length=3))
        with patch("manim_digital_presenter.script_controller.sequencer.create_dialogue_tex",
                   return_value=texts):
            steps = list(script_sequencer(self.script("one/show\ntwo/show\n"), square,
                                         box, animation_rt=0.4,
                                         actions={"show": lambda: FadeIn(square)}))
        self.assertEqual([len(step) for step in steps], [2, 3, 1])
        self.assertEqual(steps[0][-1].run_time, 0.4)
        self.assertLessEqual(texts[0].width, 1.7 + 1e-8)
        self.assertLessEqual(texts[0].height, 0.7 + 1e-8)
        self.assertIs(box.get_box(), box.box)

    def test_conflicting_symbol_sources(self):
        with self.assertRaisesRegex(ValueError, "not both"):
            list(script_sequencer("unused", Square(), scene_locals={}, symbols={}))
