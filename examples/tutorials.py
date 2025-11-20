from manim import *
from manim_digital_presenter import *
from manim_mobject_svg import *


class Logo_Demo(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # Creature
        my_creature = Creature(
            eyelid_color_input="#81b29a",
            relative_eye_position=[0, 0.1, 0],
            eye_body_ratio=0.35,
            hand_body_ratio=0.5,
            anchor_opacity=0,
            eyelid_stroke_color=BLACK,
            eyelid_stroke_width=2,
            eyes_distance=0.2,
            shift_shoulder=0.5)

        my_creature.to_corner(DL)

        # Manim Logo and rectangle
        ml = ManimBanner(dark_theme=True).scale(0.7).shift(UP)

        self.play(LaggedStart(ml.create(), FadeIn(my_creature, shift=10*DOWN, run_time=0.7), lag_ratio=0.5))
        self.play(LaggedStart(ml.expand(),
                              my_creature.point_at(ml, rt=2),
                              lag_ratio=0.5))
        self.play(my_creature.animate.move_to([0, -0.7, 0]))
        self.play(AnimationGroup(ml.animate.scale(0.6),
                                 my_creature.look_at(UP, rf=linear, rt=1),
                                 Rotate(mobject=my_creature.r_hand,
                                        angle=(0.8*PI),
                                        about_point=my_creature.r_shoulder.get_center(),
                                        run_time=1),
                                 Rotate(mobject=my_creature.l_hand,
                                        angle=(-0.8*PI),
                                        about_point=my_creature.l_shoulder.get_center(),
                                        run_time=1)))

        rec = RoundedRectangle(width=VGroup(ml, my_creature).get_width()+1,
                               height=VGroup(ml, my_creature).get_height()+1,
                               corner_radius=0.3,
                               stroke_color="#2730e6",
                               ).move_to(VGroup(ml, my_creature).get_center())
        self.play(Create(rec))
        self.wait(2)
        svg_file = VGroup(my_creature, ml, rec)
        svg_file.to_svg("logo.svg", crop=True, padding=0.2)


class Basics_Demo(Scene):
    def construct(self):

        # Creature
        my_creature = Creature(
            eyelid_color_input=DARK_BLUE,
            relative_eye_position=[0, 0.2, 0],
            eye_body_ratio=0.4,
            hand_body_ratio=0.6,
            anchor_opacity=0,
            eyelid_stroke_color=BLACK,
            eyelid_stroke_width=2,
            eyes_distance=0.2,
            shift_shoulder=0.5)

        # Define some moving objects to look at
        cir = Circle(color=RED, radius=0.5, fill_opacity=1).to_corner(UL)
        squ = Square(color=BLUE, side_length=0.5).to_corner(RIGHT).shift(UP)

        # Updaters for objects
        def move_dot(mob, dt):
            mob.shift(DOWN*np.sin(2 * PI * self.time / 2) * dt * 2)

        def rotate_dot(mob, dt):
            mob.rotate(dt * 2 * PI)

        cir.add_updater(move_dot)
        squ.add_updater(rotate_dot)

        # -- Actions --
        self.play(FadeIn(my_creature, cir, squ))
        self.wait()

        # Looking and pointing
        self.play(my_creature.look_at(LEFT))
        self.play(my_creature.look_at(squ))
        self.play(my_creature.point_at(cir))

        # Emotions
        self.play(my_creature.surprise())
        self.play(my_creature.happy())
        self.play(my_creature.thinking())
        self.play(my_creature.have_idea())
        self.play(my_creature.thinking())
        self.play(my_creature.dont_know())

        # End Basics_Demo
        self.play(FadeOut(my_creature, cir, squ))


class Explanation_Creature_Features(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # Presenter Creature
        body_teacher = Tex("$\\Sigma$", font_size=250)
        teacher_creature = Creature(
            eyelid_color_input=DARK_BLUE,
            relative_eye_position=[0.4, -0.1, 0],
            eye_body_ratio=0.3,
            hand_body_ratio=0.6,
            anchor_opacity=0,
            eyelid_stroke_color=BLACK,
            eyelid_stroke_width=2,
            core=body_teacher,
            eyes_distance=0.1
        )

        # Test Creature
        test_creature = Creature(
            eyelid_color_input=GREEN,
            relative_eye_position=[0, 0, 0],
            eye_body_ratio=0.4,
            hand_body_ratio=0.6,
            anchor_opacity=0,
            eyelid_stroke_color=BLACK,
            eyelid_stroke_width=2,
            eyes_distance=0.3,
            shift_shoulder=0.5,
        )

        # information boxes
        text_box = Text_Box(
            width=config["frame_width"] - body_teacher.get_width()-2,
            height=body_teacher.get_height(),
            box_position=DOWN,
            box_fill_color=[DARK_BLUE, BLACK],
            box_fill_opacity=0.1,
            box_color=DARK_BLUE,
            box_buff=0.2,
            corner_box=0.2
        )

        # Defining position of things on screen
        teacher_creature.to_corner(DL)
        test_creature.to_corner(RIGHT).shift(UP)
        text_box.to_corner(DR)

        self.add(teacher_creature,
                 test_creature,
                 text_box,
                 a := code_exporter(third_block))
        self.play(FadeOut(a))
        self.play(test_creature.frown.animate.set_opacity(1))
        self.play(test_creature.frown.animate.set_opacity(0),
                  test_creature.l_shoulder.animate.set_opacity(1))


# ------------------------------------------------------------------------- #

def code_exporter(code_string):
    to_export = Code(
        code_string=code_string,
        language="python",
        background="window",
        background_config={"stroke_color": DARK_BLUE,
                           "fill_color": BLACK,
                           "fill_opacity": 0.8,
                           "stroke_width": 3}).to_corner(LEFT).shift(UP)
    return to_export


first_block = '''from manim import *
from manim_digital_presenter import * '''

second_block = '''test = Creature(eyelid_color_input=RED,
                relative_eye_position=[0, 0, 0],
                eye_body_ratio=0.4,
                hand_body_ratio=0.6,
                anchor_opacity=0,
                eyelid_stroke_color=BLACK,
                eyelid_stroke_width=2,
                eyes_distance=0.3,
                shift_shoulder=0.5)'''

third_block = '''self.play(test.look_at(UP)),
self.play(test.point_at(LEFT)),
self.play(test.excited()),
self.play(test.thinking()),
self.play(test.have_idea())'''
