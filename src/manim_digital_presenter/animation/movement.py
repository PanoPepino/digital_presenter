from ..my_imports import *

__all__ = ["An_Cre"]


class An_Cre(AnimationGroup):
    r""" This is an animation class to animate the creature to present results. It eats the creature "creature" and the input_action. The input_action must be a string. Listed actions below. 

    Parameters
    ----------

    - input_action:

        - none: It waits.
        - look_left(right): Move the eyes in that direction.
        - look_uleft(uright): Move the eyes to UL or UR.
        - point_left(right): Move the eyes and arm to LEFT oRIGHT.
        - point_uleft(uright): Move the eyes and arm to UL or UR.
        - suspicion: like Fry in futurama meme.
        - boredom: like Tony Stark meme.
        - susprise: both hands to mouth, and small eyes. 
        - explanation: both hand are raised to shoulder height.
        - thinking: eyes up and hand to mouth.
        - anger: suspicion eyes and color of lower part changes.

    - animation_rate_func: Defaults to there_and_back_with_pause. If changed, careful, the different parts of the body will not come back to original position.
    - animation_run_time: Defaults to 4 seconds. Careful! If new animation is called after 4 seconds, something strange happens.
    """

    def __init__(self,
                 creature,
                 input_action: str = None,
                 animation_rate_func: float = there_and_back_with_pause,
                 animation_run_time: float = 4,
                 **kwargs):

        # Can this be fixed?

        # Note that some of the angles of rotation for the hands should be changed if the anatomy of the creature changes.

        if input_action == "none":
            super().__init__(
                Wait(),
                **kwargs)

        if input_action == "look_left":
            super().__init__(
                AnimationGroup(
                    creature.sight.animate(rate_func=animation_rate_func).shift(0.06*LEFT), suspend_updating=True),
                run_time=animation_run_time,
                **kwargs)

        if input_action == "look_right":
            super().__init__(
                AnimationGroup(
                    creature.sight.animate(rate_func=animation_rate_func).shift(0.06*RIGHT), suspend_updating=True), run_time=animation_run_time,
                **kwargs)

        if input_action == "look_uleft":
            super().__init__(
                AnimationGroup(
                    creature.sight.animate(rate_func=animation_rate_func).shift(0.06*UL), suspend_updating=True), run_time=animation_run_time,
                **kwargs)

        if input_action == "look_uright":
            super().__init__(
                AnimationGroup(
                    creature.sight.animate(rate_func=animation_rate_func).shift(0.06*UR), suspend_updating=True), run_time=animation_run_time,
                **kwargs)

        if input_action == "point_left":
            super().__init__(
                LaggedStart(
                    creature.sight.animate(rate_func=animation_rate_func).shift(0.06*LEFT),
                    creature.l_hand.animate(rate_func=animation_rate_func).rotate(-PI/2,
                                                                                  about_point=creature.l_shoulder.get_center(), axis=[0, 0, 1]),
                    lag_ratio=0.2), run_time=animation_run_time,
                **kwargs)

        if input_action == "point_right":
            super().__init__(
                LaggedStart(
                    creature.sight.animate(rate_func=animation_rate_func).shift(0.06*RIGHT),
                    creature.r_hand.animate(rate_func=animation_rate_func).rotate(
                        PI/2, about_point=creature.r_shoulder.get_center(), axis=[0, 0, 1]),
                    lag_ratio=0.2), run_time=animation_run_time,
                **kwargs)

        if input_action == "point_uleft":
            super().__init__(
                LaggedStart(
                    creature.sight.animate(rate_func=animation_rate_func).shift(0.06*UL),
                    creature.l_hand.animate(rate_func=animation_rate_func).rotate(-2*PI/3,
                                                                                  about_point=creature.l_shoulder.get_center(), axis=[0, 0, 1]),
                    lag_ratio=0.2), run_time=animation_run_time,
                **kwargs)

        if input_action == "point_uright":
            super().__init__(
                LaggedStart(
                    creature.sight.animate(rate_func=animation_rate_func).shift(0.06*UR),
                    creature.r_hand.animate(rate_func=animation_rate_func).rotate(
                        2*PI/3, about_point=creature.r_shoulder.get_center(), axis=[0, 0, 1]),
                    lag_ratio=0.2), run_time=animation_run_time,
                **kwargs)

        if input_action == "salute":
            super().__init__(
                creature.l_hand.animate(rate_func=animation_rate_func).rotate(-5.5*PI/6, about_point=creature.l_shoulder.get_center(), axis=[0, 0, 1]), run_time=animation_run_time, **kwargs)

        if input_action == "suspicion":
            super().__init__(
                AnimationGroup(creature.oculii[0][3:5].animate(rate_func=animation_rate_func).set_opacity(1),
                               creature.oculii[1][3:5].animate(rate_func=animation_rate_func).set_opacity(1)), run_time=animation_run_time,
                **kwargs)

        if input_action == "boredom":
            super().__init__(
                AnimationGroup(creature.oculii[0][3:4].animate(rate_func=animation_rate_func).set_opacity(1),
                               creature.oculii[1][3:4].animate(rate_func=animation_rate_func).set_opacity(1),
                               creature.sight.animate(rate_func=animation_rate_func).shift(0.07*UP)), run_time=animation_run_time,
                **kwargs)

        if input_action == "surprise":
            super().__init__(
                AnimationGroup(creature.sight[0].animate(rate_func=animation_rate_func).scale(0.5),
                               creature.sight[-1].animate(rate_func=animation_rate_func).scale(0.5),
                               creature.r_hand.animate(rate_func=animation_rate_func).rotate(-5*PI/6,
                                                                                             about_point=creature.r_shoulder.get_center(), axis=[0, 0, 1]),
                               creature.l_hand.animate(rate_func=animation_rate_func).rotate(5*PI/6, about_point=creature.l_shoulder.get_center(), axis=[0, 0, 1])), run_time=animation_run_time,
                **kwargs)

        if input_action == "explanation":
            super().__init__(
                AnimationGroup(
                    creature.r_hand.animate(rate_func=animation_rate_func).rotate(
                        2*PI/3, about_point=creature.r_shoulder.get_center(), axis=[0, 0, 1]),
                    creature.l_hand.animate(rate_func=animation_rate_func).rotate(-2*PI/3, about_point=creature.l_shoulder.get_center(), axis=[0, 0, 1])), run_time=animation_run_time,
                **kwargs)

        if input_action == "thinking":
            super().__init__(
                AnimationGroup(
                    creature.sight.animate(rate_func=animation_rate_func).shift(0.09*UP),
                    creature.l_hand.animate(rate_func=animation_rate_func).rotate(3.5*PI/6, about_point=creature.l_shoulder.get_center(), axis=[0, 0, 1])), run_time=animation_run_time,
                **kwargs)

        if input_action == "introduce":
            super().__init__(
                AnimationGroup(
                    creature.l_hand.animate(rate_func=animation_rate_func).rotate(PI/2, about_point=creature.l_shoulder.get_center(), axis=[0, 0, 1])), run_time=animation_run_time,
                **kwargs)
