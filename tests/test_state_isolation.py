from unittest.mock import patch

import numpy as np
from manim import BLUE, RED, Circle, Dot, Square
from manim_digital_presenter import Creature, Eyes, create_dialogue_tex
from manim_digital_presenter.presenter.blink import BlinkController

from common import ManimTest, SteppedScene


class IsolationTests(ManimTest):
    def test_anchor_defaults_do_not_leak(self):
        before = Dot()
        Creature(anchor_color=RED, anchor_opacity=0)
        after = Dot()
        self.assertEqual(after.get_fill_opacity(), before.get_fill_opacity())
        self.assertEqual(after.get_color(), before.get_color())

    def test_tex_styles_are_local(self):
        with patch("manim_digital_presenter.script_controller.rendering.Tex") as tex:
            tex.return_value = Square()
            create_dialogue_tex(["hello"], tex_color=RED)
            tex.set_default.assert_not_called()
            self.assertEqual(tex.call_args.kwargs["color"], RED)

    def test_copy_owns_controller_geometry_and_rng(self):
        original = Eyes(blink_seed=1)
        clone = original.copy()
        clone.update(2.45)
        self.assertTrue(clone.blinking)
        self.assertFalse(original.blinking)
        self.assertIsNot(original._blink_controller.rng, clone._blink_controller.rng)
        self.assertEqual(original._blink_lids[0].get_fill_opacity(), 0)
        self.assertEqual(clone._blink_lids[0].get_fill_opacity(), 1)
        original.set_blinking(False)
        self.assertTrue(clone._blink_controller.enabled)

    def test_blink_is_frame_rate_independent(self):
        states = []
        for fps in (15, 30, 60):
            controller = BlinkController(seed=7)
            for _ in range(fps * 10):
                controller.advance(1 / fps)
            states.append((controller.closed, controller.next_event))
        for state in states[1:]:
            self.assertEqual(state[0], states[0][0])
            self.assertAlmostEqual(state[1], states[0][1])

    def test_inputs_copy_only_when_requested(self):
        body, hand = Circle(color=BLUE), Square(color=BLUE)
        points = hand.get_all_points().copy()
        creature = Creature(core=body, hand=hand, copy_parts=True, body_color=RED)
        self.assertIsNot(creature.core, body)
        self.assertIsNot(creature.l_hand, hand)
        np.testing.assert_allclose(points, hand.get_all_points())
        self.assertEqual(body.get_color(), BLUE)
        legacy = Creature(core=body, hand=hand)
        self.assertIs(legacy.core, body)
        self.assertIs(legacy.l_hand, hand)

    def test_vectors_are_owned(self):
        vector = np.array([0.0, -0.2, 0.0])
        creature = Creature(relative_eye_position=vector)
        vector[0] = 100
        self.assertEqual(creature.relative_eye_position[0], 0)

    def test_expressions_pause_blinks_and_restore_transient_pose(self):
        creature = Creature(blink_seed=1)
        scene = SteppedScene()
        scene.add(creature)
        before = creature.eye_group.get_all_points().copy()
        for _ in range(2):
            scene.play(creature.happy(rt=0.15))
            self.assertEqual(creature._expression_depth, 0)
            self.assertEqual(creature._blink_lids[0].get_fill_opacity(), 0)
        np.testing.assert_allclose(before, creature.eye_group.get_all_points(), atol=1e-7)

    def test_timing_for_handless_and_full_creatures(self):
        for creature in (Creature(), Creature(core=Circle())):
            for name in ("surprise", "thinking", "dont_know", "have_idea", "happy"):
                self.assertAlmostEqual(getattr(creature, name)(rt=0.4).run_time, 0.4)

    def test_expression_references_survive_geometry_reordering(self):
        eyes = Eyes()
        eyes.eye_group.submobjects.reverse()
        scene = SteppedScene()
        scene.add(eyes)
        before = eyes.eye_group.get_all_points().copy()
        scene.play(eyes.joy(rt=0.1))
        np.testing.assert_allclose(before, eyes.eye_group.get_all_points(), atol=1e-7)
