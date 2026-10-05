import ast
from pathlib import Path

import numpy as np
from manim import PI, UP
import manim_digital_presenter as package
from manim_digital_presenter.presenter.new_logo import DigitalPresenterBanner
from manim_digital_presenter.script_controller.loader import create_dialogue_tex

from common import ManimTest, SteppedScene


class PublicTests(ManimTest):
    def test_exports_and_legacy_modules(self):
        self.assertEqual(set(package.__all__), {
            "load_csv_dialogue", "create_dialogue_tex", "play_timeline", "Text_Box",
            "script_sequencer", "Creature", "Eyes", "DigitalPresenterBanner",
        })
        self.assertIs(create_dialogue_tex, package.create_dialogue_tex)
        self.assertIs(DigitalPresenterBanner, package.DigitalPresenterBanner)

    def test_internal_dependency_boundaries(self):
        root = Path(package.__file__).parent
        for file in root.rglob("*.py"):
            if file.name == "my_imports.py":
                continue
            for node in ast.walk(ast.parse(file.read_text())):
                if isinstance(node, ast.ImportFrom):
                    self.assertFalse(any(name.name == "*" for name in node.names), str(file))
                    self.assertNotEqual(node.module, "my_imports", str(file))
                    self.assertNotEqual(node.module, "manim_digital_presenter", str(file))
                    if file.parent.name == "presenter":
                        self.assertNotIn("script_controller", node.module or "", str(file))

    def test_hidden_banner_geometry_follows_transforms(self):
        banner = DigitalPresenterBanner()
        before = banner.expanding_text.get_center().copy()
        banner.shift(UP)
        np.testing.assert_allclose(banner.expanding_text.get_center(), before + UP)
        points = banner.expanding_text.get_all_points().copy()
        banner.rotate(PI / 2, about_point=[0, 0, 0])
        expected = points.copy()
        expected[:, 0], expected[:, 1] = -points[:, 1], points[:, 0]
        np.testing.assert_allclose(banner.expanding_text.get_all_points(), expected, atol=1e-7)

    def test_banner_deferred_expansion_duration_and_cleanup(self):
        banner = DigitalPresenterBanner().scale(0.4)
        count = len(banner.submobjects)
        animation = banner.expand(run_time=0.3)
        self.assertEqual(animation.run_time, 0.3)
        self.assertEqual(len(banner.submobjects), count)
        scene = SteppedScene()
        scene.add(banner)
        scene.play(animation)
        self.assertTrue(banner.expanded)
        self.assertEqual(len(banner.submobjects), count)

    def test_banner_expansion_separates_shapes_after_animated_scale(self):
        for direction in ("left", "right", "center"):
            banner = DigitalPresenterBanner()
            scene = SteppedScene()
            scene.add(banner)
            scene.play(banner.animate.scale(0.4).build())
            scene.play(banner.expand(run_time=0.2, direction=direction))
            self.assertGreater(banner.shapes.get_left()[0],
                               banner.expanding_text.get_right()[0])
