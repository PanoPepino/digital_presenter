from manim import *
from manim_digital_presenter import *


class Simple_Demo(Scene):
    def construct(self):

        # Creature parts
        body = SVGMobject("svg_files/blob_body.svg").set_color(GREEN)
        hand = SVGMobject("svg_files/blob_hand.svg").set_color(GREEN)

        my_creature = Creature(
            eyelid_color_input=body.get_fill_color(),
            relative_eye_position=0.1,
            eye_body_ratio=0.4,
            hand_body_ratio=0.6,
            anchor_opacity=0,
            eyelid_stroke_color=BLACK,
            eyelid_stroke_width=2,
            core=body,
            hand=hand,
            eyes_distance=0.2,
            shift_shoulder=0.5,
        )

        # Create text box
        text_box = Text_Box(
            width=config["frame_width"] - 3,
            height=1,
            box_position=DOWN,
            box_fill_color=[body.get_fill_color(), BLACK],
            box_fill_opacity=0.1,
            box_color=body.get_fill_color(),
            box_buff=0.2,
            corner_box=0.2
        )

        # Define some dots to look at
        dot_1 = Circle(color=RED, radius=0.1).to_corner(UL)
        dot_2 = Circle(color=BLUE, radius=0.1).to_corner(RIGHT).shift(UP)

        # Loading script
        script = script_sequencer(
            csv_path="dialogue/simple_demo.csv",
            the_creature=my_creature,
            text_box=text_box,
            animation_rt=2.5,
            tex_color=body.get_fill_color(),
            font_size=36,
            scene_locals=locals()
        )

        # Load animations and timeline
        timeline = {
            0: next(script),      # Hi! I'm a Manim Creature!
            4: next(script),      # I can look anywhere...
            8: next(script),      # ... look at objects
            12: next(script),     # ... and also point at them!
            16: next(script),     # I have expressions too!
            20: next(script),     # Like surprise!
            24: next(script),     # And excitement!
            28: next(script),     # I think and hesitate...
            32: next(script),     # ... then solve some of my problems with...
            36: next(script),     # Some other times I cannot ...
            40: next(script),     # You can learn more about in my documentation.
            44: next(script),     # Thanks for watching!
            48: next(script),     # Extra to remove any text at the end
        }
        self.play(
            FadeIn(my_creature),
            FadeIn(text_box),
            FadeIn(dot_1, dot_2)
        )
        play_timeline(self, timeline)
        self.wait(1)

        self.play(
            FadeOut(my_creature),
            FadeOut(text_box, dot_1, dot_2)
        )
        self.wait(0.5)


class Slides_Demo(Scene):
    def construct(self):
        # Creature parts
        body = SVGMobject("svg_files/blob_body.svg").set_color(GREEN)
        hand = SVGMobject("svg_files/blob_hand.svg").set_color(GREEN)

        my_creature = Creature(
            eyelid_color_input=body.get_fill_color(),
            relative_eye_position=0.1,
            eye_body_ratio=0.4,
            hand_body_ratio=0.6,
            anchor_opacity=0,
            eyelid_stroke_color=BLACK,
            eyelid_stroke_width=2,
            eyes_distance=0.2,
            shift_shoulder=0.5,
        )
        my_creature.to_corner(DL)
        text_box = Text_Box(
            width=config["frame_width"] - 3,
            height=1,
            box_position=DOWN,
            box_fill_color=[body.get_fill_color(), BLACK],
            box_fill_opacity=0.1,
            box_color=body.get_fill_color(),
            box_buff=0.2,
            corner_box=0.2
        )
