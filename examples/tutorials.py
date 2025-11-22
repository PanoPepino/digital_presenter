from manim import *
from manim_digital_presenter import *
from manim_mobject_svg import *
from manim_slides import *


class Logo_Demo(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # Creature
        my_creature = Creature(
            eyelid_color_input=GREEN,
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
        ml = DigitalPresenterBanner(dark_theme=True).shift(1.5*UP)

        self.play(LaggedStart(ml.create(), FadeIn(my_creature, shift=10*DOWN, run_time=0.7), lag_ratio=0.5))
        self.play(LaggedStart(ml.expand(),
                              my_creature.point_at(ml, rt=2),
                              lag_ratio=0.5))
        self.play(my_creature.animate.move_to([0, -1.5, 0]), run_time=0.7)
        self.play(AnimationGroup(ml.animate.scale(0.6, about_edge=DOWN),
                                 my_creature.look_at(UP, rf=linear, rt=1),
                                 Rotate(mobject=my_creature.r_hand,
                                        angle=(0.8*PI),
                                        about_point=my_creature.r_shoulder.get_center(),
                                        run_time=1),
                                 Rotate(mobject=my_creature.l_hand,
                                        angle=(-0.8*PI),
                                        about_point=my_creature.l_shoulder.get_center(),
                                        run_time=1)))
        self.wait(2)
        svg_file = VGroup(my_creature, ml)
        svg_file.to_svg("logo.svg", crop=True, padding=0.8)


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


class Timeline_Demo(Scene):
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


class Timeline_Script_Demo(Scene):
    def construct(self):
        # Creature body parts and definition
        body = Tex("$\\Sigma$", font_size=250, color=ORANGE)
        my_creature = Creature(
            eyelid_color_input=ORANGE,
            relative_eye_position=[0.2, -0.1, 0],
            eye_body_ratio=0.3,
            anchor_opacity=0,
            eyelid_stroke_color=BLACK,
            eyelid_stroke_width=1,
            core=body,
            eyes_distance=0.2
        )
        my_creature.to_corner(DL)

        # Test objects
        point_1 = Square(color=ORANGE, fill_opacity=1).scale(0.7).to_corner(RIGHT)
        point_2 = Triangle(color=BLUE, fill_opacity=1).scale(0.3).move_to([5, 3, 0])
        point_3 = Circle(color=GREEN, fill_opacity=1).to_corner(UL)

        # Create text box for dialogue
        text_box = Text_Box(
            width=config["frame_width"] - 3,
            height=1.5,
            box_color=ORANGE,
            box_fill_color=[ORANGE, BLACK],
            box_position=DR,
            box_buff=0.2
        ).set_z_index(10)

        # Create script sequencer
        script_demo = script_sequencer(
            csv_path="dialogue/timeline_script_demo.csv",
            the_creature=my_creature,
            text_box=text_box,
            animation_rt=4,
            tex_template=TexFontTemplates.comic_sans,
            tex_color=WHITE,
            font_size=30,
            scene_locals=locals()
        )

        # Add initial objects
        self.add(text_box, my_creature)
        self.wait(1)

        # Timeline with script_sequencer integration
        timeline = {
            2: next(script_demo),      # Introduction
            6: FadeIn(point_1),
            7: next(script_demo),       # First shape appears
            11: FadeIn(point_2),
            12: next(script_demo),      # Second shape appears
            16: FadeIn(point_3),
            17: next(script_demo),      # Third shape appears
            21: next(script_demo),      # Getting surprised
            25: next(script_demo),      # Thinking about it
            29: next(script_demo),      # Hesitate
            33: next(script_demo),      # Cleaning
            36: FadeOut(VGroup(point_1, point_2, point_3)),
            38: next(script_demo),      # Extra to erase text
            39: FadeOut(VGroup(my_creature, text_box))

        }

        # Running Timeline
        play_timeline(self, timeline)
        self.wait(2)


class Explanation_Creature_Features(Slide):
    def construct(self):
        self.wait_time_between_slides = 0.1

        # Presenter Creature (NO HANDS)
        body_teacher = Tex("$\\Sigma$", font_size=250)
        teacher_creature = Creature(
            eyelid_color_input=DARK_BLUE,
            relative_eye_position=[0.4, -0.1, 0],
            eye_body_ratio=0.3,
            anchor_opacity=0,
            eyelid_stroke_color=BLACK,
            eyelid_stroke_width=2,
            core=body_teacher,
            eyes_distance=0.1
        )

        # Test Creature (WITH HANDS)
        test_creature = Creature(
            eyelid_color_input=GREEN,
            relative_eye_position=[0, 0, 0],
            eye_body_ratio=0.3,
            hand_body_ratio=0.5,
            anchor_opacity=0,
            eyelid_stroke_color=BLACK,
            eyelid_stroke_width=2,
            eyes_distance=0.3,
            shift_shoulder=0.5,
        )

        # Information boxes
        text_box = Text_Box(
            width=config["frame_width"] - body_teacher.get_width() - 2,
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
        test_creature.to_corner(RIGHT).shift(UP+LEFT)
        text_box.to_corner(DR)

        # Create script sequencer
        script_demo = script_sequencer(
            csv_path="dialogue/creature_tutorial.csv",
            the_creature=teacher_creature,
            text_box=text_box,
            animation_rt=4,
            tex_template=TexFontTemplates.comic_sans,
            tex_color=WHITE,
            font_size=30,
            scene_locals=locals()
        )

        # ----Presentation Script-----

        # Add initial objects
        self.next_slide(auto_next=True)
        self.play(FadeIn(teacher_creature, text_box))
        self.next_slide(loop=True)
        self.wait(1)

        # Introduction (I)
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 1
        self.next_slide(loop=True)
        self.wait(1)

        # Introduction (II)
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 2
        self.next_slide(loop=True)
        self.wait(1)

        # Show first code block (imports)
        code_1 = code_exporter(first_block)
        self.next_slide(auto_next=True)
        self.play(FadeIn(code_1))
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 3
        self.next_slide(loop=True)
        self.wait(1)
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 4
        self.next_slide(loop=True)
        self.wait(1)

        # Show code for creature
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 4
        self.next_slide(loop=True)
        self.wait(1)
        self.next_slide(auto_next=True)
        code_2 = code_exporter(second_block)
        self.play(ReplacementTransform(code_1, code_2))
        self.next_slide(loop=True)
        self.wait(1)
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 5
        self.next_slide(loop=True)
        self.wait(1)

        # Show the test creature
        self.next_slide(auto_next=True)
        self.play(FadeIn(test_creature))
        self.next_slide(loop=True)
        self.wait(1)
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 6
        self.next_slide(loop=True)
        self.wait(1)

        # Explain parameters General
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 7
        self.next_slide(loop=True)
        self.wait(1)
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 8
        self.next_slide(loop=True)
        self.wait(1)

        # Explain eyelid_color
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 9
        self.next_slide(loop=True)
        self.wait(1)

        # Explain eye_body_ratio
        self.next_slide(auto_next=True)
        self.play(Circumscribe(test_creature.oculii, time_width=4, color=RED))
        self.next_slide(loop=True)
        self.play(Circumscribe(test_creature.oculii, time_width=4, color=RED))
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 10
        self.next_slide(loop=True)
        self.wait(1)

        # Explain relative_eye_position
        self.next_slide(auto_next=True)
        self.play(test_creature.frown.animate.set_opacity(1))
        self.next_slide(auto_next=True)
        self.play(Circumscribe(test_creature.frown, time_width=4, color=RED))
        self.next_slide(loop=True)
        self.play(Circumscribe(test_creature.frown, time_width=4, color=RED))
        self.wait()
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 11
        self.next_slide(loop=True)
        self.wait(1)
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 12
        self.next_slide(loop=True)
        self.wait(1)
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 13
        self.next_slide(loop=True)
        self.wait(1)

        # Explain eyes_distance
        self.next_slide(auto_next=True)
        self.play(Circumscribe(test_creature.frown, time_width=4, color=RED))
        self.next_slide(loop=True)
        self.play(Circumscribe(test_creature.frown, time_width=4, color=RED))
        self.wait(1)
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 14
        self.next_slide(loop=True)
        self.wait(1)
        self.next_slide(auto_next=True)
        self.play(test_creature.frown.animate.set_opacity(0))

        # Explain hand_body_ratio and hands
        self.next_slide(auto_next=True)
        self.play(Circumscribe(test_creature.l_hand, time_width=4, color=RED))
        self.next_slide(loop=True)
        self.wait()
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 15
        self.next_slide(loop=True)
        self.wait()

        # Explain shoulder position
        self.next_slide(auto_next=True)
        self.play(test_creature.r_shoulder.animate.set_opacity(1),
                  test_creature.l_shoulder.animate.set_opacity(1))
        self.next_slide(auto_next=True)
        self.play(Indicate(test_creature.l_shoulder, color=RED),
                  Indicate(test_creature.r_shoulder, color=RED))
        self.next_slide(loop=True)
        self.play(Indicate(test_creature.l_shoulder, color=RED),
                  Indicate(test_creature.r_shoulder, color=RED))
        self.wait()
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 16
        self.next_slide(loop=True)
        self.wait()

        # Talking about not adding hands
        self.next_slide(auto_next=True)
        self.play(test_creature.r_shoulder.animate.set_opacity(0),
                  test_creature.l_shoulder.animate.set_opacity(0))
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 17
        self.next_slide(loop=True)
        self.wait()
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 18
        self.next_slide(loop=True)
        self.wait()

        # Animations intro
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 19
        self.next_slide(loop=True)
        self.wait()
        self.next_slide(auto_next=True)
        code_3 = code_exporter(third_block)
        self.play(ReplacementTransform(code_2, code_3))

        # Explain looking capability, THEN demonstrate
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 20
        self.next_slide(loop=True)
        self.wait(1)
        self.next_slide(auto_next=True)
        self.play(test_creature.look_at(UP))
        self.next_slide(loop=True)
        self.play(test_creature.look_at(UP))
        self.wait(1)

        # Explain pointing capability, THEN demonstrate
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 21
        self.next_slide(loop=True)
        self.wait(1)
        self.next_slide(auto_next=True)
        self.play(test_creature.point_at(teacher_creature))
        self.next_slide(loop=True)
        self.play(test_creature.point_at(teacher_creature))
        self.wait(1)

        # About arguments of point and look
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 22
        self.next_slide(loop=True)
        self.wait(1)

        # Explain expressions
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 23
        self.next_slide(loop=True)
        self.wait(1)

        # Explain excited, THEN show
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 24
        self.next_slide(auto_next=True)
        self.play(test_creature.excited())
        self.next_slide(loop=True)
        self.play(test_creature.excited())
        self.wait(1)

        # Explain thinking, THEN show
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 25
        self.next_slide(auto_next=True)
        self.play(test_creature.thinking())
        self.next_slide(loop=True)
        self.play(test_creature.thinking())
        self.wait(1)

        # Explain have_idea, THEN show
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 26
        self.next_slide(auto_next=True)
        self.play(test_creature.have_idea())
        self.next_slide(loop=True)
        self.play(test_creature.have_idea())
        self.wait(1)

        # Explain dont_know, THEN show
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 27
        self.next_slide(auto_next=True)
        self.play(test_creature.dont_know())
        self.next_slide(loop=True)
        self.play(test_creature.dont_know())
        self.wait(1)

        # Explain bored, THEN show
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 28
        self.next_slide(auto_next=True)
        self.play(test_creature.bored())
        self.next_slide(loop=True)
        self.play(test_creature.bored())
        self.wait(1)

        # Explain joy, THEN show
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 29
        self.next_slide(auto_next=True)
        self.play(test_creature.happy())
        self.next_slide(loop=True)
        self.play(test_creature.happy())
        self.wait(1)

        # Conclusion
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 30
        self.next_slide(loop=True)
        self.wait(1)

        # Cleanup
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 31
        self.next_slide(loop=True)
        self.wait(1)
        self.next_slide(auto_next=True)
        self.play(*next(script_demo))  # line 31
        self.next_slide(auto_next=True)
        self.play(
            FadeOut(VGroup(code_3, test_creature, teacher_creature, text_box))
        )


# ------------------------------------------------------------------------- #

# Code exporter definition and strings of code


def code_exporter(code_string):
    to_export = Code(
        code_string=code_string,
        language="python",
        background="window",
        background_config={
            "stroke_color": DARK_BLUE,
            "fill_color": BLACK,
            "fill_opacity": 0.8,
            "stroke_width": 3
        }
    ).to_corner(LEFT).shift(UP)
    return to_export


first_block = '''from manim import *
from manim_digital_presenter import *'''


second_block = '''test = Creature(
    eyelid_color_input=GREEN,
    eye_body_ratio=0.4,
    anchor_opacity=0,
    relative_eye_position=[0, 0, 0],
    eyes_distance=0.3,
    hand_body_ratio=0.6, 
    shift_shoulder=0.5,
    core=Mobject(),
    hand=Mobject())'''


third_block = '''# Creature Capabilities
self.play(test.look_at(UP))
self.play(test.point_at(object))
self.play(test.excited())
self.play(test.thinking())
self.play(test.have_idea())
self.play(test.dont_know())
self.play(test.bored())
self.play(test.happy())'''


# ------------------------------------------------------------------------- #
