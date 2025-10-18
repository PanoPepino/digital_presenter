from manim import *
from manim_digital_presenter import *
import csv


class Eye_Test(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        ojitos = Eyes(eyelid_color_input=BLUE, eyes_distance=1).scale(0.5).move_to([0, 0, 0])
        self.add(ojitos)
        self.wait(3)
        self.play(ojitos.look_at(UL))
        self.play(ojitos.bored())
        self.play(ojitos.surprised())
        self.wait(3)


class Creature_Test(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        body = Tex("$\\Psi$", font_size=300)
        lh = Tex("$\\theta$", font_size=100)
        ref = Dot(color=RED).move_to(lh.get_corner(LEFT))
        pp = Dot(color=RED).move_to([5, 3, 0])
        pp2 = Dot(color=GREEN).move_to([-4, -2, 0])
       # lh = SVGMobject("svg_files/blob_hand.svg")
        cc = Creature(eyelid_color_input=BLUE,
                      relative_eye_position=-0.4,
                      eye_body_ratio=0.4,
                      hand_body_ratio=0.5,
                      anchor_opacity=1,
                      core=body,
                      hand=lh,
                      eyes_distance=0.4)
        cc.to_corner(LEFT)
        self.add(cc, pp, pp2, ref)
        # self.play(cc.look_at(LEFT))
        # self.wait(5)
        self.play(cc.point_at(pp))
        # self.play(cc.point_at(pp2))
        # self.play(cc.animate.to_corner(RIGHT))
        # self.play(cc.point_at(pp2))
        # for dir in [UL, LEFT, DR, UR, RIGHT-0.2*UP]:
        #   self.play(cc.animate.to_corner(dir))
        #  self.play(cc.point_at(dir))
        self.play(cc.bored())
        self.play(cc.surprise())
