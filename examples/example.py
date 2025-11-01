from manim import *
from manim_digital_presenter import *
import csv


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
        body = Ellipse(width=1.5, height=2, fill_opacity=1)
        lh = SVGMobject("svg_files/blob_hand.svg")
        my_creature = Creature(eyelid_color_input=YELLOW,
                               relative_eye_position=-0.3,
                               eye_body_ratio=0.3,
                               hand_body_ratio=0.5,
                               anchor_opacity=0,
                               eyelid_stroke_color=BLACK,
                               eyelid_stroke_width=1,
                               core=body,
                               hand=lh,
                               eyes_distance=0.4,
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
                               relative_eye_position=-0.2,
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
                               relative_eye_position=-0.2,
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
                Uncreate(point_1, point_2, point_3)
            ]
        }
        play_timeline(self, timeline)
        self.wait(2)
