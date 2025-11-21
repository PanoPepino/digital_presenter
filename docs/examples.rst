Examples
=========

In this page you will find several examples and their code, so that you can easily reproduce in your own terminal and modify at will.

Simple Demo
--------------

.. raw:: html

   <div style="text-align: center;">
     <video
        src="_static/media/videos/Basics_Demo.mp4"
        autoplay
        loop
        muted
        playsinline
        controls
        style="max-width: 100%; height: auto; border: 2px solid #000000; border-radius: 8px;">
       Your browser does not support the video tag.
     </video>
   </div>

.. code-block:: python

    from manim import *
    from manim_digital_presenter import *

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

Timeline Demo
----------------

.. raw:: html

   <div style="text-align: center;">
     <video
        src="_static/media/videos/Timeline_Demo.mp4"
        autoplay
        loop
        muted
        playsinline
        controls
        style="max-width: 100%; height: auto; border: 2px solid #000000; border-radius: 8px;">
       Your browser does not support the video tag.
     </video>
   </div>

.. code-block:: python

    from manim import *
    from manim_digital_presenter import *

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
            ]}

            # Running Timeline
            play_timeline(self, timeline)
            self.wait(2)


Timeline + Scripter Demo
---------------------------

.. raw:: html

   <div style="text-align: center;">
     <video
        src="_static/media/videos/Timeline_Script_Demo.mp4"
        autoplay
        loop
        muted
        playsinline
        controls
        style="max-width: 100%; height: auto; border: 2px solid #000000; border-radius: 8px;">
       Your browser does not support the video tag.
     </video>
   </div>
.. note::
    Observe that you will have to change the path to the csv if you use your own!!

.. code-block:: python

    from manim import *
    from manim_digital_presenter import *

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
