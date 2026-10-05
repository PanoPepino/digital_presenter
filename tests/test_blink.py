"""Regression checks for scene membership and passive blink lifecycle."""

from manim import Animation, Circle, Succession, UP
from manim_digital_presenter import Creature, Eyes, play_timeline
from manim_digital_presenter.presenter.blink import BlinkController
from manim_digital_presenter.presenter.eyes import _ExpressionGroup

from common import ManimTest, SteppedScene


class BlinkTests(ManimTest):
    def test_every_eye_animation_keeps_owner_and_updater(self):
        for name in ("look_at", "joy", "bored", "surprised", "excited"):
            with self.subTest(method=name):
                eyes = Eyes(blink_seed=1)
                scene = SteppedScene()
                scene.add(eyes)
                animation = (eyes.look_at(UP, rt=0.1) if name == "look_at"
                             else getattr(eyes, name)(rt=0.1))
                scene.play(animation)
                self.assertIn(eyes, scene.get_mobject_family_members())
                before = eyes._blink_controller.elapsed
                scene.wait(0.1)
                self.assertAlmostEqual(eyes._blink_controller.elapsed, before + 0.1)
                self.assertEqual(eyes._expression_depth, 0)

    def test_every_creature_gesture_keeps_owner(self):
        for handless in (False, True):
            for name in ("point_at", "surprise", "thinking", "dont_know", "have_idea", "happy"):
                with self.subTest(handless=handless, method=name):
                    creature = Creature(core=Circle() if handless else None, blink_seed=1)
                    scene = SteppedScene()
                    scene.add(creature)
                    animation = (creature.point_at(UP, rt=0.1) if name == "point_at"
                                 else getattr(creature, name)(rt=0.1))
                    scene.play(animation)
                    self.assertIn(creature, scene.get_mobject_family_members())
                    before = creature._blink_controller.elapsed
                    scene.wait(0.1)
                    self.assertAlmostEqual(creature._blink_controller.elapsed, before + 0.1)
                    self.assertEqual(creature._expression_depth, 0)

    def test_gaze_advances_blink_but_eyelid_expression_pauses(self):
        eyes = Eyes(blink_seed=1)
        scene = SteppedScene()
        scene.add(eyes)
        scene.play(eyes.look_at(UP, rt=0.5))
        self.assertAlmostEqual(eyes._blink_controller.elapsed, 0.5)
        deadline = eyes._blink_controller.next_event
        scene.play(eyes.joy(rt=0.5))
        self.assertAlmostEqual(eyes._blink_controller.elapsed, 0.5)
        self.assertEqual(eyes._blink_controller.next_event, deadline)

    def test_repeated_expressions_do_not_postpone_pending_blink(self):
        eyes = Eyes(blink_seed=1)
        scene = SteppedScene()
        scene.add(eyes)
        deadline = eyes._blink_controller.next_event
        for _ in range(3):
            scene.play(eyes.joy(rt=0.2))
            scene.wait(0.5)
        self.assertEqual(eyes._blink_controller.next_event, deadline)
        scene.wait(deadline - eyes._blink_controller.elapsed + 0.01)
        self.assertTrue(eyes.blinking)
        self.assertTrue(all(lid.get_fill_opacity() == 1 for lid in eyes._blink_lids))
        scene.wait(0.15)
        self.assertFalse(eyes.blinking)
        self.assertTrue(all(lid.get_fill_opacity() == 0 for lid in eyes._blink_lids))

    def test_enabling_is_idempotent_and_disabled_time_does_not_advance(self):
        eyes = Eyes(blink_seed=1)
        deadline = eyes._blink_controller.next_event
        eyes.set_blinking(True).set_blinking(True)
        self.assertEqual(eyes._blink_controller.next_event, deadline)
        eyes.update(1)
        eyes.set_blinking(False).set_blinking(False)
        eyes.update(20)
        eyes.set_blinking(True)
        self.assertEqual(eyes._blink_controller.next_event, deadline)
        self.assertEqual(eyes._blink_controller.elapsed, 1)
        eyes.update(deadline - 1 + 0.01)
        self.assertTrue(eyes.blinking)
        eyes.set_blinking(True)
        self.assertTrue(eyes.blinking)

    def test_expression_interrupts_closed_phase_safely(self):
        eyes = Eyes(blink_seed=1)
        eyes.update(2.45)
        self.assertTrue(eyes.blinking)
        scene = SteppedScene()
        scene.add(eyes)
        elapsed = eyes._blink_controller.elapsed
        scene.play(eyes.bored(rt=0.2))
        self.assertFalse(eyes.blinking)
        self.assertAlmostEqual(eyes._blink_controller.elapsed, elapsed)
        self.assertGreater(eyes._blink_controller.next_event, elapsed)
        self.assertEqual(eyes._expression_depth, 0)

    def test_nested_and_repeated_finish_release_pause_once(self):
        eyes = Eyes(blink_seed=1)
        inner = eyes.joy(rt=0.2)
        outer = _ExpressionGroup(eyes, inner)
        outer.begin()
        self.assertEqual(eyes._expression_depth, 2)
        outer.finish()
        self.assertEqual(eyes._expression_depth, 0)
        outer.finish()
        inner.finish()
        self.assertEqual(eyes._expression_depth, 0)
        eyes.update(0.1)
        self.assertAlmostEqual(eyes._blink_controller.elapsed, 0.1)

    def test_failed_begin_releases_pause_and_suspension(self):
        eyes = Eyes(blink_seed=1)
        class Failed(Animation):
            def begin(self):
                self.mobject.suspend_updating()
                raise ValueError("begin failed")
        animation = _ExpressionGroup(eyes, Failed(eyes._half_lids))
        with self.assertRaisesRegex(ValueError, "begin failed"):
            animation.begin()
        self.assertEqual(eyes._expression_depth, 0)
        self.assertFalse(eyes._half_lids.updating_suspended)
        animation.finish()
        self.assertEqual(eyes._expression_depth, 0)

    def test_succession_and_timeline_keep_blink_alive(self):
        eyes = Eyes(blink_seed=1)
        scene = SteppedScene()
        scene.add(eyes)
        scene.play(Succession(eyes.joy(rt=0.1), eyes.bored(rt=0.1)))
        play_timeline(scene, {0: lambda: eyes.look_at(UP, rt=0.1),
                              0.2: lambda: eyes.joy(rt=0.1)})
        self.assertIn(eyes, scene.get_mobject_family_members())
        self.assertEqual(eyes._expression_depth, 0)
        before = eyes._blink_controller.elapsed
        scene.wait(0.1)
        self.assertAlmostEqual(eyes._blink_controller.elapsed, before + 0.1)

    def test_explicitly_unsuspended_body_motion_reopens_blink(self):
        eyes = Eyes(blink_seed=1)
        eyes.update(2.45)
        scene = SteppedScene()
        scene.add(eyes)
        scene.play(eyes.animate(run_time=0.4, suspend_mobject_updating=False).shift(UP).build())
        self.assertFalse(eyes.blinking)
        self.assertAlmostEqual(eyes._blink_controller.elapsed, 2.85)

    def test_invalid_time_values_and_coarse_steps(self):
        for duration in (0, -0.1, float("nan"), float("inf")):
            with self.subTest(duration=duration), self.assertRaises(ValueError):
                BlinkController(duration=duration)
        for dt in (-0.1, float("nan"), float("inf")):
            controller = BlinkController(seed=1)
            with self.subTest(dt=dt), self.assertRaises(ValueError):
                controller.advance(dt)
            self.assertEqual(controller.elapsed, 0)
        coarse, fine = BlinkController(seed=1), BlinkController(seed=1)
        coarse.advance(30)
        for _ in range(3000):
            fine.advance(0.01)
        self.assertEqual(coarse.closed, fine.closed)
        self.assertAlmostEqual(coarse.next_event, fine.next_event)
        self.assertFalse(BlinkController(seed=1).advance(0))
