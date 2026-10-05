import unittest

import numpy as np
from manim import Circle, DOWN, LEFT, PI, RIGHT, UP, linear
from manim_digital_presenter import Creature, Eyes
from manim_digital_presenter.presenter.geometry import direction_vector, signed_planar_angle

from common import ManimTest, SteppedScene


class GeometryTests(ManimTest):
    def test_gaze_displacement_coefficient_and_scaling(self):
        for scale in (0.5, 1, 2):
            for object_target in (False, True):
                with self.subTest(scale=scale, object_target=object_target):
                    eyes = Eyes(blink_seed=1).scale(scale)
                    eyes.set_blinking(False)
                    target = (Circle().move_to(eyes.eye_group.get_center() + UP * 3)
                              if object_target else UP)
                    before = eyes.sight.get_center().copy()
                    distance = 0.15 * eyes.eye.width * eyes.pupil_to_eye_rate
                    scene = SteppedScene()
                    scene.add(eyes)
                    scene.play(eyes.look_at(target, rf=linear, rt=0.1))
                    np.testing.assert_allclose(eyes.sight.get_center() - before,
                                               distance * UP, atol=1e-7)

    def test_signed_angles_and_degenerate_inputs(self):
        self.assertAlmostEqual(signed_planar_angle(DOWN, RIGHT), PI / 2)
        self.assertAlmostEqual(abs(signed_planar_angle(DOWN, UP)), PI)
        self.assertAlmostEqual(signed_planar_angle(DOWN, LEFT), -PI / 2)
        self.assertEqual(signed_planar_angle(DOWN, [0, 0, 0]), 0)
        with self.assertRaisesRegex(ValueError, "nonzero"):
            signed_planar_angle([0, 0, 0], UP)
        for bad in ([1, 2], [np.nan, 0, 0], [0, np.inf, 0]):
            with self.assertRaises(ValueError):
                direction_vector(bad, [0, 0, 0])

    def test_pointing_tracks_transformed_axis(self):
        creature = Creature().scale(0.4).rotate(PI / 4)
        scene = SteppedScene()
        scene.add(creature)
        for direction in (RIGHT, UP, LEFT, DOWN, np.array([2, 3, 0])):
            vector, hand, _, _ = creature._get_position_and_hand(direction)
            scene.play(creature.point_at(direction, rf=linear, rt=0.1))
            axis = hand._presenter_pointing_axis
            actual = axis.get_end() - axis.get_start()
            np.testing.assert_allclose(actual / np.linalg.norm(actual), vector, atol=1e-7)

    def test_handless_and_coincident_targets(self):
        creature = Creature(core=Circle())
        target = Circle().move_to(creature.eye_group)
        scene = SteppedScene()
        scene.add(creature)
        before = creature.sight.get_center().copy()
        scene.play(creature.point_at(target, rt=0.2))
        np.testing.assert_allclose(before, creature.sight.get_center())
        self.assertEqual(creature.point_at([1, 0, 0], rt=0.2).run_time, 0.2)

    def test_invalid_parts_and_ratios(self):
        for kwargs in ({"eye_body_ratio": 0}, {"hand_body_ratio": -1},
                       {"relative_eye_position": [1, 2]}, {"anchor_opacity": 2}):
            with self.assertRaises(ValueError):
                Creature(**kwargs)


if __name__ == "__main__":
    unittest.main()
