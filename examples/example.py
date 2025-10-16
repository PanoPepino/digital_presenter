from manim import *
from manim_digital_presenter import *
import csv


class Eye_Test(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        ojitos = Eyes(eyelid_color_input=BLUE, eyes_distance=1).scale(0.3).move_to([0, 0, 0])
        self.add(ojitos)
        self.wait(3)
        self.play(ojitos.look_at(UL))
        self.play(ojitos.bored())


class Creature_Test(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        body = SVGMobject("svg_files/blob_body.svg")
        lh = Line(start=[0, 0, 0], end=[0, 2, 0])
       # lh = SVGMobject("svg_files/blob_hand.svg")
        cc = Creature(eyelid_color_input=BLUE,
                      relative_eye_position=0,
                      eye_body_ratio=0.5,
                      anchor_opacity=1,
                      core=body,
                      hand=lh,
                      eyes_distance=0.4)
        self.add(cc)
        self.play(cc.look_at(LEFT))
        self.wait(5)
        self.play(cc.bored())
        self.play(cc.l_point(UL))


class Test(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        line = Line3D(start=[0, 0, 0], end=[0, 3, 0])
        self.add(ax, line)
        self.play(line.animate(run_time=5).rotate(PI, about_point=line.get_start(), axis=[1, 0, 1]))
