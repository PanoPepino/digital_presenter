from collections.abc import Callable
from importlib.resources import as_file, files

import numpy as np
from manim import (
    Animation, AnimationGroup, Dot, DOWN, LEFT, RIGHT, UP, PI, RED,
    LaggedStart, Line, Mobject, ParsableManimColor, Rotate, SVGMobject,
    there_and_back_with_pause,
)

from .eyes import Eyes
from .geometry import direction_vector, positive, signed_planar_angle, vector3


def _load_svg(name):
    resource = files(__package__ + ".default_svgs").joinpath(name)
    with as_file(resource) as filename:
        return SVGMobject(str(filename))



__all__ = ["Creature"]


class Creature(Eyes):
    """
    This class creates a creature composed of eyes, body, and hands by combining
    functionality from :class:`Eyes` and :class:`Mobject`.

    :param eye_body_ratio: Ratio of eye size relative to the body. Defaults to 0.6.
    :type eye_body_ratio: float

    :param hand_body_ratio: Ratio of hand size relative to the body. Defaults to 0.5.
    :type hand_body_ratio: float

    :param relative_eye_position: Vector for positioning the eyes relative to the body's top center. Defaults to [0, -0.2, 0] (slightly down from top).
    :type relative_eye_position: list[float] | np.ndarray

    :param anchor_opacity: Opacity of the anchor (joint) dots. Defaults to 0.
    :type anchor_opacity: float

    :param anchor_color: Color of the anchor dots. Defaults to :attr:`RED`.
    :type anchor_color: :class:`ParsableManimColor`

    :param core: Body Mobject. Defaults to bundled body SVG.
    :type core: :class:`Mobject`

    :param hand: Hand Mobject. Bundled hands accompany the default body; custom bodies have no hands unless supplied.
    :type hand: (Optional) :class:`Mobject` or None.

    :param shift_shoulder: Relative vertical position of the shoulder anchors with respect to the creature body center (positive values will shift DOWN. Negative values will shift shoulder up)
    :type shift_shoulder: float, optional

    :param copy_parts: Copy supplied body and hand before styling. Defaults to False for compatibility.
    :param body_color: Body colour, defaulting to eyelid colour.
    :param hand_color: Hand colour, defaulting to eyelid colour.

    .. note::
        You can find information on how to use this class in the main page of the `manimdigital-presenter` documentation.

    """

    def __init__(self,
                 eye_body_ratio: float = 0.6,
                 hand_body_ratio: float = 0.5,
                 relative_eye_position: list | np.ndarray | None = None,
                 anchor_opacity: float = 0,
                 anchor_color: ParsableManimColor = RED,
                 core: Mobject | None = None,
                 hand: Mobject | None = None,
                 shift_shoulder: float = 0,
                 *,
                 body_color: ParsableManimColor | None = None,
                 hand_color: ParsableManimColor | None = None,
                 copy_parts: bool = False,
                 **kwargs):

        super().__init__(**kwargs)
        self.eye_body_ratio = positive(eye_body_ratio, "eye_body_ratio")
        self.hand_body_ratio = positive(hand_body_ratio, "hand_body_ratio")
        self.relative_eye_position = vector3(
            [0, -0.2, 0] if relative_eye_position is None else relative_eye_position,
            "relative_eye_position",
        )
        if not np.isfinite(shift_shoulder):
            raise ValueError("shift_shoulder must be finite")
        if not np.isfinite(anchor_opacity) or not 0 <= anchor_opacity <= 1:
            raise ValueError("anchor_opacity must be between 0 and 1")
        self.anchor_opacity = anchor_opacity
        self.anchor_color = anchor_color
        self.shift_shoulder = shift_shoulder
        self.copy_parts = copy_parts
        # Resolve legacy style once; gesture code does not depend on eye styling.
        self.body_color = self.eyelid_color_input if body_color is None else body_color
        self.hand_color = self.eyelid_color_input if hand_color is None else hand_color

        self.core = _load_svg("default_body.svg") if core is None else (
            core.copy() if copy_parts else core
        )
        positive(self.core.height, "core height")
        self.core.set_color(self.body_color).set_stroke(
            color=self.eyelid_stroke_color, width=self.eyelid_stroke_width
        ).set_z_index(-3)
        self.hand = _load_svg("default_hand.svg") if hand is None and core is None else (
            hand.copy() if copy_parts and hand is not None else hand
        )

        def anchor():
            return Dot(color=anchor_color, fill_opacity=anchor_opacity,
                       stroke_opacity=anchor_opacity).set_z_index(10)

        self.l_shoulder = anchor().next_to(
            self.core.get_corner(LEFT), LEFT + shift_shoulder * DOWN, buff=0.05
        )
        self.r_shoulder = anchor().next_to(
            self.core.get_corner(RIGHT), RIGHT + shift_shoulder * DOWN, buff=0.05
        )
        self.frown = anchor().move_to(self.core.get_corner(UP) + self.relative_eye_position)
        self.eye_group.move_to(self.frown.get_center())
        self.chosen_eye_ratio = eye_body_ratio * self.core.height / self.eye_group.height
        self.eye_group.scale(self.chosen_eye_ratio)

        self.question = _load_svg("question_mark.svg").set_color(self.body_color)
        self.question.scale(0.2).next_to(self.eye_group, UP, buff=0.2).set_opacity(0)
        self.bulb = _load_svg("lightbulb.svg")
        self.bulb.scale(0.3).next_to(self.eye_group, UP, buff=0.2).set_opacity(0)
        self.add(self.core, self.frown, self.l_shoulder, self.r_shoulder,
                 self.question, self.bulb)

        if self.hand is not None:
            positive(self.hand.height, "hand height")
            self.chosen_hand_ratio = hand_body_ratio * self.core.height / self.hand.height
            self.l_hand = self.hand.set_color(self.hand_color).set_stroke(
                color=self.eyelid_stroke_color, width=self.eyelid_stroke_width
            )
            self.l_hand.scale(self.chosen_hand_ratio).next_to(
                self.l_shoulder, DOWN, aligned_edge=UP, buff=0.1
            )
            # Hidden axis follows rotations and scaling; bounding boxes do not.
            self.l_hand._presenter_pointing_axis = Line(
                self.l_hand.get_top(), self.l_hand.get_bottom(), stroke_opacity=0
            )
            self.l_hand.add(self.l_hand._presenter_pointing_axis)
            self.r_hand = self.l_hand.copy().flip().next_to(
                self.r_shoulder, DOWN, aligned_edge=UP, buff=0.1
            )
            self.add(self.l_hand, self.r_hand)

    # Animations for the creature
    def point_at(self,
                direction: list | Mobject, # That bar allows for either class
                rf: Callable[[float], float] = there_and_back_with_pause,
                rt: float = 3) -> Animation:
        """
        Method to make the creature point to any direction or object in the screen. It makes use of :meth:`_get_position_and_hand` and :meth:`_angle_hand_rotation` to determine which hand and the direction in which this will point to.

        :param direction: The direction or object to point to.
        :type direction: np.array | Mobject

        :param rf: The rate function at which it will do it. Defaults to :func:`there_and_back_with_pause`.
        :type rf: func

        :param rt: run_time of the animation. Defaults to 3".
        :type rt: float

        :return: The pointing animation
        :rtype: :class:`Animation`

        .. note::
            Without hands, this method returns a gaze animation.

        """

        positive(rt, "rt")
        if self.hand is None:
            return super().look_at(direction, rf=rf, rt=rt)
        pointing_at, the_hand, the_shoulder, _ = self._get_position_and_hand(direction)
        the_angle = self._angle_hand_rotation(the_hand, pointing_at)

        return LaggedStart(
                super().look_at(pointing_at, rf=rf, rt=rt),
                    Rotate(mobject=the_hand,
                           angle=the_angle,
                           about_point=the_shoulder.get_center(),
                           rate_func=rf,
                           run_time=rt),
                           lag_ratio=0.1, run_time=rt, group=self, suspend_mobject_updating=False)

    def surprise(self,
                  rf: Callable[[float], float] = there_and_back_with_pause,
                  rt: float = 3) -> Animation:
        """
        Method to make the creature look surprised. It takes the :meth:`surprised` from :class:`Eyes` and add the hands covering the "mouth" of the creature.

        :param rf: The rate function at which it will do it. Defaults to :func:`there_and_back_with_pause`.
        :type rf: callable

        :param rt: run_time of the animation. Defaults to 3".
        :type rt: float

        :return: The surprise animation.
        :rtype: :class:`Animation`

        .. note::
            This method will just move the eyes (and any other properties) if the creature has no hands.

        .. warning::
            This method is called surprise but it uses the :meth:`surprised` from :class:`Eyes` internally. That extra "d" is important!

        """

        if self.hand is not None:
            return AnimationGroup(
                    super().surprised(rf=rf, rt=rt), #This is to invoque the animation of the eyes.
                        Rotate(mobject=self.l_hand,
                               angle=(0.6*PI),
                               about_point=self.l_shoulder.get_center(),
                               rate_func=rf,
                               run_time=rt),
                        Rotate(mobject=self.r_hand,
                               angle=-(0.6*PI),
                               about_point=self.r_shoulder.get_center(),
                               rate_func=rf,
                               run_time=rt), group=self, suspend_mobject_updating=False)
        else:
            return AnimationGroup(super().surprised(rf=rf, rt=rt), group=self, suspend_mobject_updating=False)

    def thinking(self,
                 rf: Callable[[float], float] = there_and_back_with_pause,
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

        if self.hand is not None:
            return AnimationGroup(
                    super().look_at(UP, rf=rf, rt=rt),
                    self.question.animate(run_time=rt, rate_func=rf).set_opacity(1),
                    Rotate(mobject=self.l_hand,
                               angle=(0.6*PI),
                               about_point=self.l_shoulder.get_center(),
                               rate_func=rf,
                               run_time=rt), group=self, suspend_mobject_updating=False)
        else:
            return AnimationGroup(
                    super().look_at(UP, rf=rf, rt=rt),
                    self.question.animate(run_time=rt, rate_func=rf).set_opacity(1), group=self, suspend_mobject_updating=False)

    def dont_know(self,
                 rf: Callable[[float], float] = there_and_back_with_pause,
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

        if self.hand is not None:
            return AnimationGroup(
                    super().look_at(UP, rf=rf, rt=rt),
                    self.l_hand.animate(run_time=rt, rate_func=rf).shift(0.2*UP),
                    self.r_hand.animate(run_time=rt, rate_func=rf).shift(0.2*UP),
                group=self,
                suspend_mobject_updating=False,
            )
        else:
            return AnimationGroup(
                    super().look_at(UP, rf=rf, rt=rt), group=self, suspend_mobject_updating=False)

    def have_idea(self,
                 rf: Callable[[float], float] = there_and_back_with_pause,
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

        if self.hand is not None:
            return AnimationGroup(
                    super().excited(rf=rf, rt=rt),
                    self.bulb.animate(run_time=rt, rate_func=rf).set_opacity(1),
                    Rotate(mobject=self.r_hand,
                               angle=(0.9*PI),
                               about_point=self.r_shoulder.get_center(),
                               rate_func=rf,
                               run_time=rt),
                group=self,
                suspend_mobject_updating=False,
            )
        else:
            return AnimationGroup(super().excited(rf=rf, rt=rt),
                                  self.bulb.animate(run_time=rt, rate_func=rf).set_opacity(1), group=self, suspend_mobject_updating=False)

    def happy(self,
                 rf: Callable[[float], float] = there_and_back_with_pause,
                 rt: float = 3) -> Animation:

        """
        Method to make the creature look happy.

        :param rf: The rate function at which it will do it. Defaults to :func:`there_and_back_with_pause`.
        :type rf: func

        :param rt: run_time of the animation. Defaults to 3".
        :type rt: float

        :return: The have_idea animation.
        :rtype: :class:`Animation`

        .. note::
            This method will just close the eyes (and any other properties) if the creature has no hands.

        """

        if self.hand is not None:
            return AnimationGroup(
                    super().joy(rf=rf, rt=rt),
                    Rotate(mobject=self.r_hand,
                               angle=(0.7*PI),
                               about_point=self.r_shoulder.get_center(),
                               rate_func=rf,
                               run_time=rt),
                    Rotate(mobject=self.l_hand,
                               angle=(-0.7*PI),
                               about_point=self.l_shoulder.get_center(),
                               rate_func=rf,
                               run_time=rt),
                group=self,
                suspend_mobject_updating=False,
            )
        else:
            return AnimationGroup(super().joy(rf=rf, rt=rt), group=self, suspend_mobject_updating=False)

    def _get_position_and_hand(self, input):
        """
        Internal method to select which hand the creature will move given an input.

        :param input: The direction or object the creature will be looking at.
        :type input: list | Mobject

        :return: A tuple containing:
            - numpy.ndarray: The normalized direction vector.
            - hand: The chosen hand object (`self.r_hand` or `self.l_hand`).
            - shoulder: The chosen shoulder to which rotate with (`self.r_shoulder` or `self.l_shoulder`).
            - delta: A delta function indicator (0 if right hand, 1 if left).
        :rtype: tuple(numpy.ndarray, Hand, int)

        """

        new_direction = direction_vector(input, self.eye_group.get_center())
        if new_direction[0] > 0:
            return new_direction, self.r_hand, self.r_shoulder, 0
        return new_direction, self.l_hand, self.l_shoulder, 1

    def _angle_hand_rotation(self, hand, look_vec):
        """Compute signed rotation using the hand's transformed pointing axis."""
        axis = hand._presenter_pointing_axis
        return signed_planar_angle(axis.get_end() - axis.get_start(), look_vec)
