from manim import *
from manim_digital_presenter import *


class Eye_Test(Scene):
    def construct(self):
        self.camera.background_color = DARK_BLUE
        ojitos = Eyes(eyelid_color_input=BLUE,
                      eyes_distance=1,
                      eyelid_stroke_color=BLACK,
                      eyelid_stroke_width=2).scale(0.5).move_to([0, 0, 0])
        self.add(ojitos)
        self.wait(3)
        self.play(ojitos.look_at(UL))
        self.play(ojitos.bored())
        self.play(ojitos.surprised())
        self.play(ojitos.joy())
        self.wait(3)


class Creature_Hands_Test(Scene):
    def construct(self):

        # Test objects
        point_1 = Square(color=RED, fill_opacity=1).scale(0.7).to_corner(RIGHT)
        point_2 = Triangle(color=BLUE, fill_opacity=0.8).scale(0.3).move_to([5, 3, 0])
        point_3 = Dot(color=GREEN, radius=0.2).move_to([-4, -2, 0])
        points = VGroup(point_1, point_2, point_3).set_z_index(-5)

        positions = [LEFT, RIGHT, DOWN, UP, UL, UR, DL, DR]
        # Creature body parts and definition

        my_creature = Creature(eyelid_color_input=BLUE,
                               relative_eye_position=0.1,
                               eye_body_ratio=0.3,
                               hand_body_ratio=0.5,
                               anchor_opacity=0,
                               eyelid_stroke_color=BLACK,
                               eyelid_stroke_width=1,
                               eyes_distance=+0.4,
                               shift_shoulder=4)

        #  Animations
        self.add(my_creature, points)
        for position in positions:
            self.play(my_creature.look_at(position))
            self.wait()
        for point in points:
            self.play(my_creature.point_at(point))

        self.play(my_creature.surprise())
        self.play(my_creature.thinking())
        self.play(my_creature.have_idea())
        self.play(my_creature.dont_know())
        self.play(my_creature.happy())
        self.wait(2)


class Creature_Letter_Test(Scene):
    def construct(self):

        # Test objects
        point_1 = Square(color=RED, fill_opacity=1).scale(0.7).to_corner(RIGHT)
        point_2 = Triangle(color=BLUE, fill_opacity=0.8).scale(0.3).move_to([5, 3, 0])
        point_3 = Dot(color=GREEN, radius=0.2).move_to([-4, -2, 0])
        points = VGroup(point_1, point_2, point_3).set_z_index(-5)

        # Creature body parts and definition
        body = Tex("$\\Sigma$", font_size=250, color=ORANGE)
        my_creature = Creature(eyelid_color_input=ORANGE,
                               relative_eye_position=[0.2, 0.1, 0],
                               eye_body_ratio=0.3,
                               anchor_opacity=0,
                               eyelid_stroke_color=BLACK,
                               eyelid_stroke_width=1,
                               core=body,
                               eyes_distance=0.2)

        #  Animations
        self.add(my_creature, points)

        for point in points:
            self.play(my_creature.look_at(point))

        self.play(my_creature.surprise())
        self.play(my_creature.thinking())
        self.play(my_creature.have_idea())
        self.play(my_creature.dont_know())
        self.wait(2)


class Timeline_Test(Scene):
    def construct(self):

        # Creature body parts and definition
        body = Tex("$\\Sigma$", font_size=250, color=ORANGE)
        my_creature = Creature(eyelid_color_input=ORANGE,
                               relative_eye_position=[0.2, -0.1, 0],
                               eye_body_ratio=0.3,
                               anchor_opacity=0,
                               eyelid_stroke_color=BLACK,
                               eyelid_stroke_width=1,
                               core=body,
                               eyes_distance=0.2)
        my_creature.to_corner(DL)

        # Test objects
        point_1 = Square(color=RED).scale(0.7).to_corner(RIGHT)
        point_2 = Triangle(color=BLUE).scale(0.3).move_to([5, 3, 0])
        point_3 = Circle(color=GREEN).to_corner(UL)

        # Timeline
        timeline = {
            1: FadeIn(my_creature),
            3: FadeIn(point_1),
            5: my_creature.look_at(point_1),
            8: FadeIn(point_2),
            10: my_creature.look_at(point_2),
            13: FadeIn(point_3),
            15: my_creature.look_at(point_3),
            18: my_creature.surprise(),
            21: my_creature.thinking(),
            24: my_creature.have_idea(),
            27: my_creature.animate.rotate(PI/2),
            30: [
                my_creature.animate.move_to(ORIGIN),
                FadeOut(VGroup(point_1, point_2, point_3)),
                FadeOut(my_creature)
            ]
        }

        # Running Timeline
        play_timeline(self, timeline)
        self.wait(2)


class Loader_Test(Scene):
    def construct(self):
        # Create objects
        box = Square(color=WHITE).scale(0.5).to_corner(UR)
        body = Ellipse(width=1.5, height=2, fill_opacity=1, color=RED)
        hand = SVGMobject("svg_files/blob_hand.svg").set_color(RED)
        my_creature = Creature(eyelid_color_input=body.get_fill_color(),
                               relative_eye_position=-0.2,
                               eye_body_ratio=0.3,
                               anchor_opacity=0,
                               eyelid_stroke_color=BLACK,
                               eyelid_stroke_width=1,
                               core=body,
                               hand=hand,
                               hand_body_ratio=0.5,
                               eyes_distance=0.2)
        my_creature.to_corner(DL)

        # Create text box
        text_box = Text_Box(
            box_position=DR,
            box_fill_color=[body.get_color(), BLACK],
            box_color=body.get_color()
        )

        # Create sequencer with text_box
        script_example = script_sequencer(
            csv_path="dialogue/example_script.csv",
            the_creature=my_creature,
            text_box=text_box,  # Pass the text box!
            animation_rt=5,
            scene_locals=locals()
        )

        # Add text_box to scene
        self.add(text_box)

        timeline = {
            2: next(script_example),
            5: next(script_example),
            8: next(script_example),
            11: next(script_example),
            14: next(script_example),
        }

        self.play(FadeIn(my_creature, box))
        play_timeline(self, timeline)


class Dialogue_Box_Test(Scene):
    def construct(self):
        body = Ellipse(width=1.5, height=2, fill_opacity=1, color=RED)
        hand = SVGMobject("svg_files/blob_hand.svg").set_color(RED)
        my_creature = Creature(eyelid_color_input=body.get_fill_color(),
                               relative_eye_position=-0.2,
                               eye_body_ratio=0.3,
                               anchor_opacity=0,
                               eyelid_stroke_color=BLACK,
                               eyelid_stroke_width=1,
                               core=body,
                               hand=hand,
                               hand_body_ratio=0.5,
                               eyes_distance=0.2)
        my_creature.to_corner(DL)
        custom_box = Text_Box(
            width=config["frame_width"]-3,
            height=my_creature.get_height()/2,
            box_color=body.get_color(),
            triangle_color=YELLOW,
            box_position=DR
        ).set_z_index(10)
        self.add(custom_box, my_creature)
        self.wait(2)


class CodeFromString(Scene):
    def construct(self):
        code = '''from manim import Scene, Square

class FadeInSquare(Scene):
    def construct(self):
        s = Square()
        self.play(FadeIn(s))
        self.play(s.animate.scale(2))
        self.wait()'''

        rendered_code = Code(
            code_string=code,
            language="python",
            background="window",
            background_config={"stroke_color": RED},
        )
        self.add(rendered_code)
