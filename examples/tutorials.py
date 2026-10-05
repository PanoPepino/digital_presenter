from pathlib import Path

from manim import *
from manim_digital_presenter import *
from manim_slides import Slide


class Logo_Demo(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # Creature
        my_creature = Creature(copy_parts=True,
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
        self.play(my_creature.animate(suspend_mobject_updating=False).move_to([0, -1.5, 0]), run_time=0.7)
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


class Basics_Demo(Scene):
    def construct(self):

        # Creature
        my_creature = Creature(copy_parts=True,
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
        my_creature = Creature(copy_parts=True, eyelid_color_input=ORANGE,
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
            1: lambda: FadeIn(my_creature),
            3: lambda: FadeIn(point_1),
            5: lambda: my_creature.look_at(point_1),
            8: lambda: FadeIn(point_2),
            10: lambda: my_creature.look_at(point_2),
            13: lambda: FadeIn(point_3),
            15: lambda: my_creature.look_at(point_3),
            18: lambda: my_creature.surprise(),
            21: lambda: my_creature.thinking(),
            24: lambda: my_creature.have_idea(),
            27: lambda: my_creature.animate(suspend_mobject_updating=False).rotate(PI/2),
            30: lambda: [
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
        my_creature = Creature(copy_parts=True,
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
            csv_path=Path(__file__).parent / "dialogue/timeline_script_demo.csv",
            the_creature=my_creature,
            text_box=text_box,
            animation_rt=4,
            tex_template=TexFontTemplates.comic_sans,
            tex_color=WHITE,
            font_size=30,
            symbols={"point_1": point_1, "point_2": point_2, "point_3": point_3}
        )

        # Add initial objects
        self.add(text_box, my_creature)
        self.wait(1)

        # Timeline with script_sequencer integration
        timeline = {
            2: lambda: next(script_demo),      # Introduction
            6: lambda: FadeIn(point_1),
            7: lambda: next(script_demo),       # First shape appears
            11: lambda: FadeIn(point_2),
            12: lambda: next(script_demo),      # Second shape appears
            16: lambda: FadeIn(point_3),
            17: lambda: next(script_demo),      # Third shape appears
            21: lambda: next(script_demo),      # Getting surprised
            25: lambda: next(script_demo),      # Thinking about it
            29: lambda: next(script_demo),      # Hesitate
            33: lambda: next(script_demo),      # Cleaning
            36: lambda: FadeOut(VGroup(point_1, point_2, point_3)),
            38: lambda: next(script_demo),      # Extra to erase text
            39: FadeOut(VGroup(my_creature, text_box))

        }

        # Running Timeline
        play_timeline(self, timeline)
        self.wait(2)


class Explanation_Creature_Features_Short(Scene):
    """Nineteen four-second beats covering parameters and every creature gesture."""

    BEAT_SECONDS = 4
    FADE_SECONDS = 0.5
    TEXT_FONT = "Comic Sans MS"

    def construct(self):
        def creature(x=0, **changes):
            options = dict(eyelid_color_input=GREEN, eye_body_ratio=0.3,
                           relative_eye_position=[0, -0.2, 0], blink_seed=1,
                           eyelid_stroke_width=1, copy_parts=True)
            options.update(changes)
            result = Creature(**options)
            result.scale(2 / result.core.height)
            result.shift([x, -0.6, 0] - result.core.get_center())
            return result

        def caption(title, explanation, code):
            lines = VGroup(
                Text(title, font=self.TEXT_FONT, font_size=34),
                Text(explanation, font=self.TEXT_FONT, font_size=24),
                Text(code, font="monospace", font_size=21, color=YELLOW),
            ).arrange(DOWN, buff=0.22)
            if lines.width > config.frame_width - 1:
                lines.scale_to_fit_width(config.frame_width - 1)
            return lines.to_edge(UP, buff=0.25)

        def fade_out():
            if self.mobjects:
                self.play(*(FadeOut(obj) for obj in list(self.mobjects)),
                          run_time=self.FADE_SECONDS)

        def beat(text, objects, animation_factory=None):
            fade_out()
            self.play(*(FadeIn(obj) for obj in [text, *objects]),
                      run_time=self.FADE_SECONDS)
            if animation_factory is None:
                self.wait(self.BEAT_SECONDS)
            else:
                self.play(animation_factory(), run_time=self.BEAT_SECONDS)

        first = creature()
        beat(caption("Create a creature", "Default body, hands, and automatic blinking.",
                     "from manim_digital_presenter import Creature\ncreature = Creature()"),
             [first])

        comparisons = [
            ("Colors", "Colors change appearance; geometry stays unchanged.",
             "body_color=BLUE, hand_color=ORANGE",
             {}, dict(body_color=BLUE, hand_color=ORANGE)),
            ("Eye size", "Larger ratio makes eyes larger relative to body.",
             "eye_body_ratio: 0.3 -> 0.5", {}, dict(eye_body_ratio=0.5)),
            ("Eye anchor", "Eye position follows visible forehead anchor.",
             "relative_eye_position: [0,-0.2,0] -> [0,-0.6,0]",
             dict(anchor_opacity=1),
             dict(anchor_opacity=1, relative_eye_position=[0, -0.6, 0])),
            ("Eye spacing", "Larger gap moves eyes farther apart.",
             "eyes_distance: 0.1 -> 0.6", {}, dict(eyes_distance=0.6)),
            ("Hand size", "Larger ratio makes hands longer relative to body.",
             "hand_body_ratio: 0.5 -> 0.8", {}, dict(hand_body_ratio=0.8)),
            ("Shoulder joints", "Shoulder anchors move together with attached hands.",
             "shift_shoulder: 0 -> 8  |  anchor_opacity=1",
             dict(anchor_opacity=1), dict(anchor_opacity=1, shift_shoulder=8)),
            ("Custom geometry", "Provide both core and hand for a custom body with hands.",
             "core=Ellipse(width=1.2, height=2, fill_opacity=1)\n"
             "hand=Ellipse(width=0.3, height=1, fill_opacity=1)",
             {}, dict(core=Ellipse(width=1.2, height=2, fill_opacity=1),
                      hand=Ellipse(width=0.3, height=1, fill_opacity=1))),
        ]
        for title, explanation, code, reference_options, changed_options in comparisons:
            reference = creature(-3, **reference_options)
            before = creature(3, **reference_options)
            after = creature(3, **changed_options)
            labels = VGroup(Text("Reference", font=self.TEXT_FONT, font_size=22).move_to([-3, -3.2, 0]),
                            Text("Modified", font=self.TEXT_FONT, font_size=22).move_to([3, -3.2, 0]))
            beat(caption(title, explanation, code), [reference, before, labels],
                 lambda: ReplacementTransform(before, after))

        gestures = [
            ("Gaze", "Look toward a direction vector or a scene object.",
             "creature.look_at(UP, rt=4)", lambda c, target: c.look_at(UP, rt=4)),
            ("Pointing", "Hands point toward target; eyes follow.",
             "creature.point_at(target, rt=4)", lambda c, target: c.point_at(target, rt=4)),
            ("Surprise", "Shrink pupils and bring hands toward the face.",
             "creature.surprise(rt=4)", lambda c, target: c.surprise(rt=4)),
            ("Thinking", "Combine eye and hand movements in one gesture.",
             "creature.thinking(rt=4)", lambda c, target: c.thinking(rt=4)),
            ("Uncertainty", "Look upward and raise hands in a shrug.",
             "creature.dont_know(rt=4)", lambda c, target: c.dont_know(rt=4)),
            ("An idea", "Show a lightbulb and gesture toward an idea.",
             "creature.have_idea(rt=4)", lambda c, target: c.have_idea(rt=4)),
            ("Happiness", "Express happiness with eyelids and hands.",
             "creature.happy(rt=4)", lambda c, target: c.happy(rt=4)),
            ("Bored eyes", "Lower eyelids for a bored expression.",
             "creature.bored(rt=4)", lambda c, target: c.bored(rt=4)),
            ("Surprised eyes", "Shrink pupils without moving hands.",
             "creature.surprised(rt=4)", lambda c, target: c.surprised(rt=4)),
            ("Excited eyes", "Enlarge pupils without moving hands.",
             "creature.excited(rt=4)", lambda c, target: c.excited(rt=4)),
            ("Joyful eyes", "Close eyelids into a happy curved expression.",
             "creature.joy(rt=4)", lambda c, target: c.joy(rt=4)),
        ]
        for title, explanation, code, action in gestures:
            example = creature()
            target = Dot([4, 0.5, 0], color=ORANGE)
            objects = [example, target] if title == "Pointing" else [example]
            beat(caption(title, explanation, code), objects,
                 lambda: action(example, target))
        fade_out()


class Explanation_Creature_Features(Slide):
    def construct(self):
        self.wait_time_between_slides = 0.1

        # Presenter Creature (NO HANDS)
        body_teacher = Tex("$\\Sigma$", font_size=250)
        teacher_creature = Creature(copy_parts=True,
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
        test_creature = Creature(copy_parts=True,
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
            csv_path=Path(__file__).parent / "dialogue/creature_tutorial.csv",
            the_creature=teacher_creature,
            text_box=text_box,
            animation_rt=4,
            tex_template=TexFontTemplates.comic_sans,
            tex_color=WHITE,
            font_size=30,
            symbols={"test_creature": test_creature}
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


second_block = '''test = Creature(copy_parts=True,
    eyelid_color_input=GREEN,
    eye_body_ratio=0.4,
    anchor_opacity=0,
    relative_eye_position=[0, 0, 0],
    eyes_distance=0.3,
    hand_body_ratio=0.6,
    shift_shoulder=0.5,
    core=Circle(fill_opacity=1),
    hand=Square(fill_opacity=1))'''


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
