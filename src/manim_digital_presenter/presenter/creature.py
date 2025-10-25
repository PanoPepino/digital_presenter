from ..my_imports import *
from .eyes import *


__all__ = ["Creature"]


class Creature(Eyes, VMobject):
    """
    This class creates a creature composed of eyes, body, and hands by combining 
    functionality from :class:`Eyes` and :class:`Mobject`.

    :param eye_body_ratio: Ratio of eye size relative to the body. Defaults to 0.6.
    :type eye_body_ratio: float

    :param hand_body_ratio: Ratio of hand size relative to the body. Defaults to 0.5.
    :type hand_body_ratio: float

    :param relative_eye_position: Relative vertical positioning of the eyes. Defaults to -0.2.
    :type relative_eye_position: float

    :param anchor_opacity: Opacity of the anchor (joint) dots. Defaults to 0.
    :type anchor_opacity: float

    :param anchor_color: Color of the anchor dots. Defaults to :attr:`RED`.
    :type anchor_color: :class:`ParsableManimColor`

    :param core: Core body Mobject. Defaults to empty :class:`Mobject`. This parameter can be any Manim Mobject or an SVG file.
    :type core: :class:`Mobject`

    :param hand: Hand Mobject to attach to the creature. Defaults to None. 
    :type hand: (Optional) :class:`Mobject` or None.

    :param shift_shoulder: Relative vertical position of the :param: anchor_opacity with respect to the creature body center (positive values will shift DOWN. Negative values will shift shoulder up)
    :type shift_shoulder: float

    **Example usage:**

    .. code-block:: python

        from manim import *
        from manim_digital_creature import *

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
                body = SVGMobject("svg_files/blob_body.svg")
                lh = SVGMobject("svg_files/blob_hand.svg")
                my_creature = Creature(eyelid_color_input=BLUE,
                                       relative_eye_position=0.1,
                                       eye_body_ratio=0.3,
                                       hand_body_ratio=0.5,
                                       anchor_opacity=0,
                                       eyelid_stroke_color=DARK_BLUE,
                                       eyelid_stroke_width=1,
                                       core=body,
                                       hand=lh,
                                       eyes_distance=0.4,
                                       shift_shoulder=0.4)
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




    """

    def __init__(self,
                 eye_body_ratio: float = 0.6,
                 hand_body_ratio: float = 0.5,
                 relative_eye_position: float = -0.2,
                 anchor_opacity: float = 0,
                 anchor_color: ParsableManimColor = RED,
                 core: Mobject = Mobject(),
                 hand: Mobject = None,
                 shift_shoulder: float = 0,
                 **kwargs):

        super().__init__(**kwargs)
        self.eye_body_ratio = eye_body_ratio
        self.hand_body_ratio = hand_body_ratio
        self.relative_eye_position = relative_eye_position
        self.anchor_opacity = anchor_opacity
        self.anchor_color = anchor_color
        self.hand = hand
        self.core = core
        self.shift_shoulder= shift_shoulder

        # Set fill opacity to see the joints of the creature.
        Dot().set_default(color=self.anchor_color, fill_opacity=self.anchor_opacity)

        # Eyes
        self.frown = Dot().next_to(self.core.get_corner(UP), UP, buff=self.relative_eye_position).set_z_index(10)
        self.oculii.move_to(self.frown.get_center())
        self.chosen_eye_ratio = self.eye_body_ratio*self.core.get_height()/self.oculii.get_height()
        self.oculii.scale(self.chosen_eye_ratio)

        # Body
        self.core.set(color=self.eyelid_color_input, 
                      stroke_color=self.eyelid_stroke_color, 
                      stroke_width=self.eyelid_stroke_width)
        self.core.set_z_index(-3)

        # Hands
        self.l_shoulder = Dot().next_to(self.core.get_corner(LEFT), LEFT+self.shift_shoulder*DOWN, buff=0.05).set_z_index(10)
        self.r_shoulder = Dot().next_to(self.core.get_corner(RIGHT), RIGHT+self.shift_shoulder*DOWN, buff=0.05).set_z_index(10)


        # Extra accessories
        get_bulb_path = path.join(path.dirname(__file__), "body_parts/lightbulb.svg")
        get_question_path = path.join(path.dirname(__file__), "body_parts/question_mark.svg")

        self.question = SVGMobject(get_question_path).set_color(self.eyelid_color_input)
        self.question.scale(0.2).next_to(self.oculii, UP, buff=0.2)
        self.question.set_opacity(0)

        self.bulb = SVGMobject(get_bulb_path)
        self.bulb.scale(0.3).next_to(self.oculii, UP, buff=0.2)
        self.bulb.set_opacity(0)
        

        # Loading creature

        if self.hand is not None:
            self.chosen_hand_ratio = self.hand_body_ratio*self.core.get_height()/self.hand.get_height()
            self.l_hand = self.hand.set(color=self.eyelid_color_input)
            self.l_hand.set(color=self.eyelid_color_input, 
                                      stroke_color=self.eyelid_stroke_color, 
                                      stroke_width=self.eyelid_stroke_width)
            self.l_hand.scale(self.chosen_hand_ratio).next_to(self.l_shoulder, DOWN, aligned_edge=UP, buff=0.1)
            self.r_hand = self.l_hand.copy().flip().next_to(self.r_shoulder, DOWN, aligned_edge=UP, buff=0.1)

            self.add(self.core, self.frown, self.l_shoulder, self.r_shoulder, self.l_hand, self.r_hand, self.question, self.bulb)

        else:
            print("---------- Warning ----------\n",
                  "The creature has no hands\n",
                  "All creature animations will load without hand animations\n",
                  "-----------------------------")
            self.add(self.core, self.frown, self.l_shoulder, self.r_shoulder, self.question, self.bulb)

        self.go_live() 

    def go_live(self):
        """
        Dummy function to make the creature alive. It uses its own timer to make the creature blink and any other passive changes on the creature (for example, one can adapt an updater to make the creature breath, or shine based on this dummy element)
        
        """

        time = 0
        dummy_element = VMobject()

        def living(mob, dt):
            nonlocal time
            time += dt
            self.pulse(time)
        dummy_element.add_updater(living)
        self.add(dummy_element)

    def pulse(self, time):
        """
        Obsolet function to use previous :meth:`go_live` and make the creature glow. It requires a glow mobject to iluminate.
        """

        # self.glow.set_opacity(1-0.6*np.cos(time)**2)
        # This can perhaps be improved to make the whole creature levitate (oscillate around a point depending on a time parameter or any other time dependence)


    def point_at(self,
                direction: list | Mobject, # That bar allows for either class
                rf: float = there_and_back_with_pause,
                rt: float = 3) -> Animation:   
        """
        Method to make the creature point to any direction or object in the screen. It makes use of :meth:`get_position_and_hand` and :meth:`angle_hand_rotation` to determine which hand and the direction in which this will point to.

        :param direction: The direction or object to point to.
        :type direction: np.array | Mobject

        :param rf: The rate function at which it will do it. Defaults to :func:`there_and_back_with_pause`.
        :type rf: func

        :param rt: run_time of the animation. Defaults to 3".
        :type rt: float

        :return: The pointing animation
        :rtype: :class:`Animation`

        .. note::
            This method will not be valid for a creature without hands.
        
        """

        pointing_at, the_hand, the_shoulder, delta = self.get_position_and_hand(direction)
        the_angle = self.angle_hand_rotation(the_hand, pointing_at)
        
        return LaggedStart(
                super().look_at(self.pupil_to_eye_rate*pointing_at),
                    Rotate(mobject=the_hand, 
                           angle=(1-2*delta)*(the_angle), 
                           about_point=the_shoulder.get_center(), 
                           rate_func=rf, 
                           run_time=rt),
                           lag_ratio=0.1)
    
    def surprise(self,
                  rf: float = there_and_back_with_pause,
                  rt: float = 3) -> Animation:
        """
        Method to make the creature look surprised. It takes the :meth:`surprised` from :class:`Eyes` and add the hands covering the "mouth" of the creature.

        :param rf: The rate function at which it will do it. Defaults to :func:`there_and_back_with_pause`.
        :type rf:`func`

        :param rt: run_time of the animation. Defaults to 3".
        :type rt: float

        :return: The surprise animation.
        :rtype: :class:`Animation`

        .. note::
            This method will just move the eyes (and any other properties) if the creature has no hands.
        
        """

        if self.hand:
            return AnimationGroup(
                    super().surprised(), #This is to invoque the animation of the eyes.
                        Rotate(mobject=self.l_hand, 
                               angle=(0.6*PI), 
                               about_point=self.l_shoulder.get_center(), 
                               rate_func=rf, 
                               run_time=rt),
                        Rotate(mobject=self.r_hand, 
                               angle=-(0.6*PI), 
                               about_point=self.r_shoulder.get_center(), 
                               rate_func=rf, 
                               run_time=rt))
        else:
            return AnimationGroup(super().surprised())

    def thinking(self,
                 rf: float = there_and_back_with_pause,
                 rt: float = 3) -> Animation:
        """
        Method to make the creature think. A question mark will appear on top of its eyes

        :param rf: The rate function at which it will do it. Defaults to :func:`there_and_back_with_pause`.
        :type rf: func

        :param rt: run_time of the animation. Defaults to 3".
        :type rt: float

        :return: The thinking animation.
        :rtype: :class:`Animation`

        .. note::
            This method will just move the eyes (and any other properties) if the creature has no hands.

        """

        if self.hand:
            return AnimationGroup(
                    super().look_at(self.pupil_to_eye_rate*UP),
                    self.question.animate(run_time=rt, rate_func=rf).set_opacity(1),
                    Rotate(mobject=self.l_hand, 
                               angle=(0.6*PI), 
                               about_point=self.l_shoulder.get_center(), 
                               rate_func=rf, 
                               run_time=rt)
                    )
        else:
            return AnimationGroup(
                    super().look_at(self.pupil_to_eye_rate*UP),
                    self.question.animate(run_time=rt, rate_func=rf).set_opacity(1))

    
    def dont_know(self,
                 rf: float = there_and_back_with_pause,
                 rt: float = 3) -> Animation:
        """
        Method to make the creature look hesitant, including a shoulder shrug.

        :param rf: The rate function at which it will do it. Defaults to :func:`there_and_back_with_pause`.
        :type rf: func

        :param rt: run_time of the animation. Defaults to 3".
        :type rt: float

        :return: The dont_know animation.
        :rtype: :class:`Animation`

        .. note::
            This method will just move the eyes (and any other properties) if the creature has no hands.

        """

        if self.hand:
            return AnimationGroup(
                    super().look_at(self.pupil_to_eye_rate*UP),
                    self.l_hand.animate(run_time=rt, rate_func=rf).shift(0.2*UP),
                    self.r_hand.animate(run_time=rt, rate_func=rf).shift(0.2*UP)
                    )
        else:
            return AnimationGroup(
                    super().look_at(self.pupil_to_eye_rate*UP))

    
    def have_idea(self,
                 rf: float = there_and_back_with_pause,
                 rt: float = 3) -> Animation:
        
        """
        Method to make the creature have an Eureka moment.

        :param rf: The rate function at which it will do it. Defaults to :func:`there_and_back_with_pause`.
        :type rf: func

        :param rt: run_time of the animation. Defaults to 3".
        :type rt: float

        :return: The have_idea animation.
        :rtype: :class:`Animation`

        .. note::
            This method will just move the eyes (and any other properties) if the creature has no hands.

        """

        if self.hand:
            return AnimationGroup(
                    super().excited(),
                    self.bulb.animate(run_time=rt, rate_func=rf).set_opacity(1),
                    Rotate(mobject=self.r_hand, 
                               angle=(0.9*PI), 
                               about_point=self.r_shoulder.get_center(), 
                               rate_func=rf, 
                               run_time=rt)
                    )
        else:
            return AnimationGroup(super().excited(),
                                  self.bulb.animate(run_time=rt, rate_func=rf).set_opacity(1))

                

    
    def get_position_and_hand(self, input):
        """
        Method to select which hand the creature will move given an input.

        :param input: The direction or object the creature will be looking at.
        :type input: list | Mobject

        :return: A tuple containing:
            - numpy.ndarray: The normalized direction vector.
            - hand: The chosen hand object (`self.r_hand` or `self.l_hand`).
            - shoulder: The chosen shoulder to which rotate with (`self.r_shoulder` or `self.l_shoulder`).
            - delta: A delta function indicator (0 if right hand, 1 if left).
        :rtype: tuple(numpy.ndarray, Hand, int)

        """

        if isinstance(input, Mobject):
            vector = (input.get_center()-self.oculii.get_center())
            new_direction = vector/np.linalg.norm(vector)
            print(np.array(new_direction))
        else:
            new_direction = input

        if new_direction[0] > 0:
            print("greater")
            chosen_hand = self.r_hand
            chosen_shoulder = self.r_shoulder
            delta_func = 0
        else:
            print("smaller")
            chosen_hand = self.l_hand
            chosen_shoulder = self.l_shoulder
            delta_func= 1
        return np.array(new_direction), chosen_hand, chosen_shoulder, delta_func

    
     
    def angle_hand_rotation(self, hand, look_vec):
        """
        Method to determine the angle of rotation of the hand given a point where to look at.

        :param hand: The hand to be moved.
        :type hand: Mobject.

        :param look_vec: The direction to look and point at.
        :type look_vec: list | Mobject.

        :return: The angle of rotation
        :rtype: float

        """
        
        vec_hand = hand.get_corner(DOWN)-hand.get_corner(UP)
        norm_vec_hand = vec_hand/np.linalg.norm(vec_hand)
        print(norm_vec_hand, look_vec)
        angle_rot = np.arccos((norm_vec_hand @ look_vec)/(np.linalg.norm(vec_hand)*np.linalg.norm(look_vec)))
        return angle_rot

