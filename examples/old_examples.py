from manim import *
from manim_digital_presenter import *


class Example (Scene):
    def construct(self):
        # Do not forget to change the position of the .svg files. I cannot manage to place the .svg files inside the body folder. It seems they have to be place inside a folder at the level of the example file.

        # There seems to be a problem such that there will be an error if there is no folder called media when this file is executed for first time.

        # The creature to be animated
        bloby = Creature(eyelid_color_input=DARK_BLUE, pupillary_vector=[1.2, 0, 0]).scale(2).to_corner(DL, buff=0.3)

        # Loading the commands with load_script_tex. Each iteration of the counter will
        rt = 2.5  # how much time do you want the animations to last.
        script_example = load_script_tex(bloby, text_example, actions_example, triangle_next_text, animation_rt=rt)

        timeline = {
            2: next(script_example),  # Call line 1 in csv file,
            5: next(script_example),  # 2
            8: next(script_example),  # 3
            11: next(script_example),  # 4
            14: next(script_example),  # 5
            17: next(script_example),  # 6
            20: next(script_example),  # 7
            23: next(script_example),  # 8
            26: next(script_example),  # 9
            29: next(script_example),  # 10
            32: next(script_example),  # 11
            35: next(script_example),  # 12
            38: next(script_example),  # 13
            41: next(script_example),  # 14
            44: next(script_example),  # 15
            47: next(script_example),  # 16
            50: next(script_example),  # 17
            53: next(script_example),  # 18
            56: next(script_example),  # 19
            59: next(script_example),  # 20
            61: next(script_example)  # 21
        }
        self.play(FadeIn(bloby, text_box))
        play_timeline(self, timeline)
        self.play(FadeOut(bloby, text_box))
