"""Short render checks without optional tutorial dependencies."""

import tempfile
from pathlib import Path

from manim import (BLUE, GREEN, Circle, Create, FadeOut, LEFT, RIGHT, Scene, Square,
                   TexTemplate, UP, VGroup)
from manim_digital_presenter import (
    Creature, DigitalPresenterBanner, Eyes, Text_Box, play_timeline, script_sequencer,
)


class EyesAndCreatureSmoke(Scene):
    def construct(self):
        eyes = Eyes(blink_seed=1).scale(0.25).shift(UP)
        creature = Creature(copy_parts=True, blink_seed=1, eyelid_color_input=BLUE).scale(0.4).shift(LEFT)
        handless = Creature(core=Circle(fill_opacity=1), copy_parts=True, eyelid_color_input=GREEN).scale(0.4).shift(RIGHT)
        self.add(eyes, creature, handless)
        self.play(eyes.joy(rt=2), creature.point_at(UP, rt=2),
                  handless.point_at(LEFT, rt=2))
        self.play(creature.surprise(rt=2))
        self.play(creature.thinking(rt=2))
        self.play(creature.have_idea(rt=2))
        self.play(creature.dont_know(rt=2))
        self.play(creature.happy(rt=2))
        self.wait(0.2)


class DialogueTimelineSmoke(Scene):
    def construct(self):
        creature = Creature(copy_parts=True, eyelid_color_input=BLUE).scale(0.3).shift(LEFT)
        box = Text_Box(width=5, height=1.2)
        target = Square().scale(0.3).shift(2 * RIGHT)
        self.add(creature, box)
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "dialogue.csv"
            script.write_text('Hello/happy\nLook at target/look_at/target\n')
            steps = script_sequencer(script, creature, box, animation_rt=2,
                                      tex_template=TexTemplate(),
                                      symbols={"target": target})
            play_timeline(self, {
                0: lambda: Create(target, run_time=0.2),
                0.2: lambda: next(steps),
                0.5: lambda: next(steps),
                0.8: lambda: next(steps),
                1: lambda: FadeOut(VGroup(creature, box, target), run_time=0.2),
            })
        assert not any(mob.has_points() for mob in self.get_mobject_family_members()), \
            "Timeline left removed objects in scene"


class BannerSmoke(Scene):
    def construct(self):
        banner = DigitalPresenterBanner().scale(0.4).shift(UP)
        self.play(banner.create(run_time=0.2))
        self.play(banner.expand(run_time=0.3))
        self.play(FadeOut(banner, run_time=0.2))
