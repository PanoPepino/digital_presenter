import numpy as np
from manim import Animation, Create, FadeOut, ReplacementTransform, RIGHT, Square, UP
from manim_digital_presenter import play_timeline

from common import ManimTest, SteppedScene


class TimelineTests(ManimTest):
    def test_empty_and_bad_timestamps(self):
        scene = SteppedScene()
        play_timeline(scene, {})
        self.assertEqual(scene.elapsed, 0)
        for timestamp in (-1, float("nan"), float("inf"), "one"):
            with self.assertRaises(ValueError):
                play_timeline(scene, {timestamp: []})

    def test_factories_capture_current_geometry(self):
        scene = SteppedScene()
        square = Square()
        scene.add(square)
        play_timeline(scene, {
            0: lambda: square.animate(run_time=0.2).shift(RIGHT),
            0.2: lambda: square.animate(run_time=0.2).shift(UP),
        })
        np.testing.assert_allclose(square.get_center(), RIGHT + UP, atol=1e-7)
        self.assertAlmostEqual(scene.elapsed, 0.4)
        self.assertFalse(square.updating_suspended)

    def test_overlapping_independent_events_and_removal(self):
        scene = SteppedScene()
        first, second = Square(), Square().shift(2 * RIGHT)
        scene.add(first)
        play_timeline(scene, {0: FadeOut(first, run_time=0.4),
                              0.1: lambda: Create(second, run_time=0.5)})
        self.assertNotIn(first, scene.get_mobject_family_members())
        self.assertIn(second, scene.get_mobject_family_members())
        self.assertAlmostEqual(scene.elapsed, 0.6)

    def test_replacement_cleanup(self):
        scene = SteppedScene()
        first, second = Square(), Square().shift(RIGHT)
        scene.add(first)
        play_timeline(scene, {0: ReplacementTransform(first, second, run_time=0.2)})
        self.assertNotIn(first, scene.get_mobject_family_members())
        self.assertIn(second, scene.get_mobject_family_members())

    def test_overlap_warning(self):
        square = Square()
        with self.assertWarnsRegex(RuntimeWarning, "overlap"):
            play_timeline(SteppedScene(), {0: square.animate(run_time=1).shift(RIGHT),
                                          0.1: lambda: square.animate.shift(UP)})

    def test_exact_lifecycle_and_sound(self):
        calls = []
        class Tracked(Animation):
            sound_to_play = "test.wav"
            def begin(self):
                calls.append("begin")
                super().begin()
            def finish(self):
                calls.append("finish")
                super().finish()
            def clean_up_from_scene(self, scene):
                calls.append("cleanup")
                super().clean_up_from_scene(scene)
        scene = SteppedScene()
        play_timeline(scene, {0.2: Tracked(Square(), run_time=0.3),
                              0.3: lambda: Create(Square(), run_time=0.3)})
        self.assertEqual(calls, ["begin", "finish", "cleanup"])
        self.assertEqual(scene.sounds, [(0.2, "test.wav")])

    def test_exception_recovers_active_objects(self):
        square = Square()
        def bad():
            raise ValueError("factory failed")
        with self.assertRaisesRegex(ValueError, "factory failed"):
            play_timeline(SteppedScene(), {0: square.animate.shift(RIGHT), 0.2: bad})
        self.assertFalse(square.updating_suspended)

    def test_failed_begin_preserves_error_and_resumes_object(self):
        square = Square()
        class Failing(Animation):
            def begin(self):
                self.mobject.suspend_updating()
                raise ValueError("begin failed")
            def finish(self):
                raise AssertionError("Unstarted animation must not finish")
        with self.assertRaisesRegex(ValueError, "begin failed"):
            play_timeline(SteppedScene(), {0: Failing(square)})
        self.assertFalse(square.updating_suspended)

    def test_lists_and_zero_duration_events(self):
        scene = SteppedScene()
        first, second = Square(), Square().shift(RIGHT)
        play_timeline(scene, {0: [Create(first, run_time=0),
                                 lambda: Create(second, run_time=0.2)],
                              0.3: lambda: [FadeOut(first, run_time=0.1),
                                            FadeOut(second, run_time=0.1)]})
        self.assertNotIn(first, scene.get_mobject_family_members())
        self.assertNotIn(second, scene.get_mobject_family_members())
        self.assertAlmostEqual(scene.elapsed, 0.4)
