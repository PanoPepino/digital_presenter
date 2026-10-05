"""Verify passive blinking survives gestures and body movement in rendered frames."""

from manim import Scene, UP
from manim_digital_presenter import Eyes


class BlinkSmoke(Scene):
    def construct(self):
        eyes = Eyes(blink_seed=1).scale(0.5)
        self.add(eyes)
        observed = []

        def sample(dt):
            if dt > 0:
                assert eyes in self.get_mobject_family_members(), "Blink owner disappeared"
                opacities = tuple(lid.get_fill_opacity() for lid in eyes._blink_lids)
                assert opacities[0] == opacities[1], "Eyelids blink out of sync"
                observed.append(eyes.blinking)

        self.add_updater(sample)
        self.play(eyes.look_at(UP, rt=0.3))
        self.play(eyes.joy(rt=0.2))
        self.wait(3)
        assert any(observed), "Scheduled blink was never displayed"
        assert not observed[-1], "Blink did not reopen"
        self.play(eyes.animate(suspend_mobject_updating=False).shift(UP), run_time=0.4)
        self.wait(0.3)
        self.remove_updater(sample)
