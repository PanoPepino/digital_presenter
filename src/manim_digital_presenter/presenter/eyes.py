from manim import *
from ..my_imports import *

__all__ = ["Eyes"]


class Eyes(VMobject):
    """
    This class creates a pair of eyes with a natural blinking animation. They can be animated with :class:`Animate_Creature` or methods of :class:`Eyes`. 

    :param eyelid_color_input: Color of the eye_lid. Defaults to BLACK.
    :type eyelid_color_input: ParsableManimColor, str, optional

    :param eyeball_color: Color of the eye itself. Defaults to WHITE.
    :type eyeball_color: ParsableManimColor, str, optional

    :param pupil_to_eye_rate: How big the pupil is respect to the whole eye. Defaults to 0.5.
    :type pupil_to_eye_rate: float, optional

    :param pupil_color_input: Defaults to BLACK.
    :type pupil_color_input: ParsableManimColor, str, optional

    :param reflection_direction: Where the light comes from to illuminate the pupils. Defaults to Up + Right.
    :type reflection direction: list[float], optional

    :param eyes_distance: A vector that indicates the distance between the eyes (measured from each pupil center). Defaults to [1,0,0].
    :type eyes_distance: list[float]


    .. note::

    **Example usage:**

    .. code-block:: python

        from manim import *
        from manim_digital_creature import *

        -----------TO BE CONSTRUCTED---------------

    """

    def __init__(self,
                 eyelid_color_input: ParsableManimColor = BLACK,
                 eyelid_stroke_width: float=0.1,
                 eyeball_color_input: ParsableManimColor = WHITE,
                 pupil_to_eye_rate: float=0.5,
                 pupil_color_input: ParsableManimColor = BLACK,
                 reflection_direction: list[float] = UR,
                 eyes_distance: str = 0.1,  # If 0, the eyes will be touching.
                 **kwargs):
        super().__init__(**kwargs)

        self.eyelid_color_input = eyelid_color_input
        self.eyelid_stroke_width = eyelid_stroke_width
        self.eyeball_color_input = eyeball_color_input
        self.pupil_to_eye_rate = pupil_to_eye_rate
        self.pupil_color_input = pupil_color_input
        self.reflection_direction = reflection_direction
        self.eyes_distance = eyes_distance

        # eyes
        self.eye = Circle(color=self.eyeball_color_input,
                          fill_opacity=1,
                          stroke_color=self.eyelid_color_input,
                          radius=1)

        self.rimel = Circle(color=self.eyeball_color_input,
                            fill_opacity=0,
                            stroke_color=self.eyelid_color_input,
                            stroke_width=self.eyelid_stroke_width,
                            radius=1).set_z_index(3)

        self.pupil = Circle(color=self.pupil_color_input,
                            fill_opacity=1,
                            radius=self.pupil_to_eye_rate).move_to(self.eye.get_center())

        self.reflection = Circle(color=WHITE,
                                 stroke_color=WHITE,
                                 fill_opacity=1,
                                 radius=0.1).move_to(self.pupil.get_center() + 0.1*self.reflection_direction)

        self.eyelid = Circle(color=self.eyelid_color_input,
                             fill_opacity=0,
                             stroke_color=self.eyelid_color_input,
                             stroke_width=self.eyelid_stroke_width,
                             radius=1).move_to(self.eye.get_center()).set(z_index=2)  # for creature to blink!

        # This is extra, to make the creature close the eyes, but not completely, so it manages a suspicion or boredom look
        half_eyelid_up = Arc(angle=PI,
                             color=self.eyelid_color_input,
                             fill_opacity=0,
                             stroke_color=self.eyelid_color_input,
                             stroke_width=self.eyelid_stroke_width,
                             fill_color=self.eyelid_color_input).move_to(self.eye.get_corner(UP), aligned_edge=UP).set(z_index=4)

        half_eyelid_down = Arc(angle=-PI,
                               color=self.eyelid_color_input,
                               fill_opacity=0,
                               stroke_color=self.eyelid_color_input,
                               stroke_width=self.eyelid_stroke_width,
                               fill_color=self.eyelid_color_input).move_to(self.eye.get_corner(DOWN), aligned_edge=DOWN).set(z_index=4)

        self.sight = VGroup(self.pupil, self.reflection)  # The composite VGroup for creature to look at things!
        self.full_eye = VGroup(self.eye, self.rimel, self.eyelid, half_eyelid_up,
                               half_eyelid_down, self.sight)
        self.full_eye_2 = self.full_eye.copy().next_to(self.full_eye, buff=eyes_distance)

        self.oculii = always_redraw(lambda:
                                    VGroup(self.full_eye, self.full_eye_2))
        self.sight = always_redraw(lambda: VGroup(self.full_eye[-1], self.full_eye_2[-1]))
        self.oculii.move_to([0, 0, 0])
        self.add(self.oculii)
        self.to_blink()  # self function to start the blinking of the eyes.

    def to_blink(self):
        """
        Method to make the eyes blink. It uses its own timer (nonlocal) to make the blinking. Its main feature is the counter "time" that increments independently and it is used in the following functions.
        """

        time = 0
        self.blinking = False
        dummy_element = VMobject()

        def living(mob, dt):
            nonlocal time
            time += dt
            self.blink(time)
        dummy_element.add_updater(living)
        self.add(dummy_element)

    def blink(self, time):
        """
        Conditional function. If a random number gets greater than some value, the creature will move its eyelid (i.e. will set opacity to them). Observe that has to be done to both eyelids separatly. Some issues with animation interaction.
        """

        if time < 0.2:  # No blinking at the beginning of the scene
            return
        window = time % 1
        if window < 0.2:
            if not self.blinking:
                if random.random() < 0.2:
                    self.oculii[0][2].set_opacity(1)
                    self.oculii[1][2].set_opacity(1)
                    self.blinking = True
        else:
            if self.blinking:
                self.oculii[0][2].set_opacity(0)
                self.oculii[1][2].set_opacity(0)
                self.blinking = False

    def look_at(self,
                direction: list | Mobject,
                rf: float=there_and_back_with_pause,
                rt: float=3) -> Animation:
        """
        Method to make the :class:`Eyes` look in a given direction. It will compute the normalised vector between the eyes of the creature and the object/direction to display a more realistic look.

        :param direction: The direction or the object to look at.
        :type direction: list | Mobject

        :param rf: Animation rate function. Defaults to :meth: `there_and_back_with_pause`.
        :type rf: `func`

        :param rt: Animation duration. Defaults to 3".
        :type rt: float

        :returns: The animation of the eyes looking at the specific direction.
        :rtype: `Animation`

        """

        if isinstance(direction, Mobject):
            vector = (direction.get_center()-self.oculii.get_center())
            new_direction = vector/np.linalg.norm(vector)
            print(np.array(new_direction))
        else:
            new_direction = direction
            print(new_direction)

        return AnimationGroup(self.sight.animate(rate_func=rf, run_time=rt).shift(0.25*self.pupil_to_eye_rate*new_direction))

    def bored(self,
              rf: float=there_and_back_with_pause,
              rt: float=3) -> Animation:
        return AnimationGroup(self.oculii[0][3:4].animate(rate_func=rf).set_opacity(1),
                              self.oculii[1][3:4].animate(rate_func=rf).set_opacity(1),
                              self.sight.animate(rate_func=rf).shift(0.05*UP), 
                              run_time=rt)
    def surprised(self,
                 rf: float=there_and_back_with_pause,
                 rt: float=3) -> Animation:
        return  AnimationGroup(self.sight[0].animate(rate_func=rf, run_time=rt).scale(0.5),
                               self.sight[-1].animate(rate_func=rf, run_time=rt).scale(0.5),
                               )
    

                