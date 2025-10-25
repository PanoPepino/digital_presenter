from manim import *
from manim_digital_presenter import *
import csv

from scipy.fftpack import shift


class Eye_Test(Scene):
    def construct(self):
        self.camera.background_color = WHITE
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


class Creature_Test(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # Test objects
        point_1 = Dot(color=RED).to_corner(RIGHT)
        point_2 = Dot(color=RED).move_to([5, 3, 0])
        point_3 = Dot(color=GREEN).move_to([-4, -2, 0])
        points = VGroup(point_1, point_2, point_3).set_z_index(-5)

        positions = [LEFT, RIGHT, DOWN, UP, UL, UR, DL, DR]
        # Creature body parts and definition
        body = Star(n=25, fill_opacity=1)
        lh = SVGMobject("svg_files/blob_hand.svg")
        my_creature = Creature(eyelid_color_input=RED,
                               relative_eye_position=-0.5,
                               eye_body_ratio=0.3,
                               hand_body_ratio=0.5,
                               anchor_opacity=0,
                               eyelid_stroke_color=BLACK,
                               eyelid_stroke_width=2,
                               core=body,
                               hand=lh,
                               eyes_distance=0.4,
                               shift_shoulder=3)
        my_creature.to_corner(LEFT)

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
