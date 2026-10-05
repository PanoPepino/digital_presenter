from collections.abc import Callable

import numpy as np
from manim import (
    BLACK, WHITE, UR, UP, DOWN, PI, TAU, Animation, AnimationGroup,
    Arc, ArcBetweenPoints, Circle, Mobject, ParsableManimColor, VGroup,
    VMobject, there_and_back_with_pause,
)

from .blink import BlinkController, update_blink
from .geometry import direction_vector, positive, vector3


class _ExpressionGroup(AnimationGroup):
    """Pause passive eyelids only while an expression is playing."""

    def __init__(self, owner, *animations, **kwargs):
        self.owner = owner
        self._pause_acquired = False
        # Keep the updater owner in scene when animating aliased child groups.
        super().__init__(*animations, group=owner, suspend_mobject_updating=False, **kwargs)

    def begin(self):
        if self._pause_acquired:
            return
        if self.owner._expression_depth == 0:
            self.owner._blink_controller.open_for_pause()
            for lid in self.owner._blink_lids:
                lid.set_opacity(0)
        self.owner._expression_depth += 1
        self._pause_acquired = True
        try:
            super().begin()
        except Exception:
            # Partial begin may already have suspended child animations.
            for animation in self.animations:
                _abort_expression(animation)
            self.group.resume_updating()
            self._release_pause()
            raise

    def _release_pause(self):
        if self._pause_acquired:
            self.owner._expression_depth -= 1
            self._pause_acquired = False

    def finish(self):
        if not self._pause_acquired:
            return
        try:
            super().finish()
        finally:
            self._release_pause()


def _abort_expression(animation):
    """Release nested expression pauses and suspended alias groups on failure."""
    if isinstance(animation, AnimationGroup):
        for child in animation.animations:
            _abort_expression(child)
    if isinstance(animation, _ExpressionGroup):
        animation._release_pause()
    if animation.mobject is not None:
        animation.mobject.resume_updating()


__all__ = ["Eyes"]


class Eyes(VMobject):
    """
    This class creates a pair of eyes with a natural blinking animation. They can be animated with methods of :class:`Eyes`.

    :param eyelid_color_input: Color of the eye_lid. Defaults to BLACK.
    :type eyelid_color_input: ParsableManimColor, str, optional

    :param eyeball_color: Color of the eye itself. Defaults to WHITE.
    :type eyeball_color: ParsableManimColor, str, optional

    :param pupil_to_eye_rate: How big the pupil is respect to the whole eye. Defaults to 0.5.
    :type pupil_to_eye_rate: float, optional

    :param pupil_color_input: Defaults to BLACK.
    :type pupil_color_input: ParsableManimColor, str, optional

    :param reflection_direction: Where the light comes from to illuminate the pupils. Defaults to Up + Right.
    :type reflection_direction: list[float], optional

    :param eyes_distance: Nonnegative gap between eyes. Defaults to 0.1.
    :type eyes_distance: float


    .. note::
        Animations of the :class:`Eyes` will be called in the :class:`Creature` by the :func:`super`.

    **Example usage:**

    .. code-block:: python

        from manim import *
        from manim_digital_presenter import *

        class Eye_Test(Scene):
            def construct(self):
                ojitos = Eyes(eyelid_color_input=BLUE,
                              eyes_distance=1).scale(0.5)
                ojitos.move_to([0, 0, 0])
                self.add(ojitos)
                self.wait(3)
                self.play(ojitos.look_at(UL))
                self.play(ojitos.bored())
                self.play(ojitos.surprised())
                self.wait(3)
                self.play(ojitos.excited())

    """

    def __init__(self,
                 eyelid_color_input: ParsableManimColor = BLACK,
                 eyelid_stroke_width: float = 0.1,
                 eyelid_stroke_color: ParsableManimColor = BLACK,
                 eyeball_color_input: ParsableManimColor = WHITE,
                 pupil_to_eye_rate: float = 0.5,
                 pupil_color_input: ParsableManimColor = BLACK,
                 reflection_direction: list[float] | np.ndarray = UR,
                 eyes_distance: float = 0.1,  # If 0, the eyes will be touching.
                 *,
                 blink_seed: int | None = None,
                 **kwargs):
        super().__init__(**kwargs)

        positive(pupil_to_eye_rate, "pupil_to_eye_rate")
        if pupil_to_eye_rate > 1:
            raise ValueError("pupil_to_eye_rate must not exceed 1")
        if not np.isfinite(eyes_distance) or eyes_distance < 0:
            raise ValueError("eyes_distance must be finite and nonnegative")
        if not np.isfinite(eyelid_stroke_width) or eyelid_stroke_width < 0:
            raise ValueError("eyelid_stroke_width must be finite and nonnegative")
        self.eyelid_color_input = eyelid_color_input
        self.eyelid_stroke_width = eyelid_stroke_width
        self.eyelid_stroke_color = eyelid_stroke_color
        self.eyeball_color_input = eyeball_color_input
        self.pupil_to_eye_rate = pupil_to_eye_rate
        self.pupil_color_input = pupil_color_input
        self.reflection_direction = vector3(reflection_direction, "reflection_direction")
        self.eyes_distance = eyes_distance

        # eyes
        self.eye = Circle(color=self.eyeball_color_input,
                          fill_opacity=1,
                          stroke_color=BLACK,
                          stroke_width=self.eyelid_stroke_width,
                          radius=1)

        self.rimel = Circle(color=self.eyeball_color_input,
                            fill_opacity=1,
                            stroke_width=self.eyelid_stroke_width, #To avoid strange eye
                            stroke_color=self.eyelid_stroke_color,
                            radius=1).set_z_index(-3)

        self.pupil = Circle(color=self.pupil_color_input,
                            fill_opacity=1,
                            radius=self.pupil_to_eye_rate).move_to(self.eye.get_center())

        self.reflection = Circle(color=WHITE,
                                 stroke_color=WHITE,
                                 fill_opacity=1,
                                 radius=0.1).move_to(self.pupil.get_center() + 0.1*self.reflection_direction)

        self.eyelid = Circle(color=self.eyelid_color_input,
                             fill_opacity=0,
                             stroke_width=self.eyelid_stroke_width,
                             stroke_color=self.eyelid_stroke_color,
                             radius=1).move_to(self.eye.get_center()).set(z_index=2)  # for creature to blink!
        left_point = self.eye.point_at_angle(PI)   # or circle.get_left()
        right_point = self.eye.point_at_angle(0)   # or circle.get_right()

        # Create arc with ArcBetweenPoints
        self.joy_line = ArcBetweenPoints(
            stroke_opacity=0,
            start=left_point,
            end=right_point,
            angle=-TAU/6,  # Controls the curvature
            stroke_color=BLACK,
            stroke_width=2*self.eyelid_stroke_width).set(z_index=10)

        # This is extra, to make the creature close the eyes, but not completely.
        half_eyelid_up = Arc(angle=PI,
                             color=self.eyelid_color_input,
                             fill_opacity=0,
                             stroke_width=self.eyelid_stroke_width,
                             stroke_color=self.eyelid_stroke_color,
                             fill_color=self.eyelid_color_input).move_to(self.eye.get_corner(UP), aligned_edge=UP).set(z_index=4)

        half_eyelid_down = Arc(angle=-PI,
                               color=self.eyelid_color_input,
                               fill_opacity=0,
                               stroke_width=self.eyelid_stroke_width,
                               stroke_color=self.eyelid_stroke_color,
                               fill_color=self.eyelid_color_input).move_to(self.eye.get_corner(DOWN), aligned_edge=DOWN).set(z_index=4)

        self.sight = VGroup(self.pupil, self.reflection)  # The composite VGroup for creature to look at things!
        self.full_eye = VGroup(self.eye,
                               self.rimel,
                               self.eyelid,
                               half_eyelid_up,
                               half_eyelid_down,
                               self.joy_line,
                               self.sight)

        self.full_eye_2 = self.full_eye.copy().next_to(self.full_eye, buff=eyes_distance)

        self.eye_group = VGroup(self.full_eye, self.full_eye_2)
        self.oculii = self.eye_group  # Legacy public alias
        self.sight = VGroup(self.full_eye[-1], self.full_eye_2[-1])
        # Capture named references once. Gesture methods never index geometry.
        self._blink_lids = (self.eyelid, self.full_eye_2[2])
        self._upper_lids = VGroup(half_eyelid_up, self.full_eye_2[3])
        self._half_lids = VGroup(
            half_eyelid_up, half_eyelid_down, self.full_eye_2[3], self.full_eye_2[4]
        )
        self._joy_lines = VGroup(self.joy_line, self.full_eye_2[5])
        self.eye_group.move_to([0, 0, 0])
        self.add(self.eye_group)
        self._expression_depth = 0
        self._blink_controller = BlinkController(seed=blink_seed)
        self.add_updater(update_blink)

    @property
    def blinking(self):
        """Whether passive eyelids are currently closed."""
        return self._blink_controller.closed

    def set_blinking(self, enabled: bool):
        """Enable/disable blinking, preserving the pending open-phase interval."""
        enabled = bool(enabled)
        if self._blink_controller.enabled == enabled:
            return self
        self._blink_controller.open_for_pause()
        self._blink_controller.enabled = enabled
        for lid in self._blink_lids:
            lid.set_opacity(0)
        return self

    # Animations for the eyes
    def look_at(self,
                direction: list | Mobject,
                rf: Callable[[float], float]=there_and_back_with_pause,
                rt: float=3) -> Animation:
        """
        Method to make the :class:`Eyes` look in a given direction. It will compute the normalised vector between the eyes of the creature and the object/direction to display a more realistic look.

        :param direction: The direction or the object to look at.
        :type direction: list | Mobject

        :param rf: Animation rate function. Defaults to :meth:`there_and_back_with_pause`.
        :type rf: `func`

        :param rt: Animation duration. Defaults to 3".
        :type rt: float

        :returns: The animation of the eyes looking at the specific direction.
        :rtype: `Animation`

        """

        positive(rt, "rt")
        new_direction = direction_vector(direction, self.eye_group.get_center())
        # Derive displacement from current eye size, so scaled eyes behave equally.
        displacement = 0.15 * self.eye.width * self.pupil_to_eye_rate * new_direction
        return AnimationGroup(
            self.sight.animate(rate_func=rf, run_time=rt).shift(displacement),
            run_time=rt,
            group=self,
            suspend_mobject_updating=False,
        )

    def bored(self,
              rf: Callable[[float], float] = there_and_back_with_pause,
              rt: float = 3) -> Animation:
        """
        Method to make the :class:`Eyes` look bored/annoyed (upper eyelid appears and rolling eyes)

        :param rf: Animation rate function. Defaults to :meth:`there_and_back_with_pause`.
        :type rf: `func`

        :param rt: Animation duration. Defaults to 3".
        :type rt: float

        :returns: The animation of bored/annoyed eyes.
        :rtype: `Animation`

        """

        positive(rt, "rt")
        return _ExpressionGroup(
            self,
            self._upper_lids.animate(rate_func=rf).set_opacity(1),
            self.sight.animate(rate_func=rf).shift(0.025 * self.eye.width * UP),
            run_time=rt,
        )

    def surprised(self,
                 rf: Callable[[float], float] = there_and_back_with_pause,
                 rt: float = 3) -> Animation:
        """
        Method to make the :class:`Eyes` look surprised (pupils shrink)

        :param rf: Animation rate function. Defaults to :meth:`there_and_back_with_pause`.
        :type rf: `func`

        :param rt: Animation duration. Defaults to 3".
        :type rt: float

        :returns: The animation of surprised eyes.
        :rtype: `Animation`

        """

        positive(rt, "rt")
        return AnimationGroup(
            *(sight.animate(rate_func=rf, run_time=rt).scale(0.5) for sight in self.sight),
            run_time=rt,
            group=self,
            suspend_mobject_updating=False,
        )

    def excited(self,
                 rf: Callable[[float], float] = there_and_back_with_pause,
                 rt: float = 3) -> Animation:

        """
        Method to make the :class:`Eyes` look amused by something. (Pupils grow)

        :param rf: Animation rate function. Defaults to :meth:`there_and_back_with_pause`.
        :type rf: `func`

        :param rt: Animation duration. Defaults to 3".
        :type rt: float

        :returns: The animation of excited eyes.
        :rtype: `Animation`

        """

        positive(rt, "rt")
        return AnimationGroup(
            *(sight.animate(rate_func=rf, run_time=rt).scale(1.2) for sight in self.sight),
            run_time=rt,
            group=self,
            suspend_mobject_updating=False,
        )


    def joy(self,
        rf: Callable[[float], float] = there_and_back_with_pause,
        rt: float = 3) -> Animation:

        """
        Method to make the :class:`Eyes` look joyful (both eyelids appear with a curved line simulating closed happy eyes)


        :param rf: Animation rate function. Defaults to :meth:`there_and_back_with_pause`.
        :type rf: `func`


        :param rt: Animation duration. Defaults to 3".
        :type rt: float


        :returns: The animation of joyful closed eyes.
        :rtype: `Animation`


        """

        positive(rt, "rt")
        return _ExpressionGroup(
            self,
            self._half_lids.animate(rate_func=rf).set_opacity(1),
            self._joy_lines.animate(rate_func=rf).set_stroke(opacity=1),
            run_time=rt,
        )
