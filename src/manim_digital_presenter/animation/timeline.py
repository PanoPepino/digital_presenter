from ..my_imports import *

__all__ = []


def play_timeline(scene, timeline):
    r"""Famous Abulafia Timeline. Check the following link for further information:

    https://github.com/abul4fia/manim-play-timeline

    """

    previous_t = 0
    ending_time = 0
    for t, anims in sorted(timeline.items()):
        to_wait = t - previous_t
        if to_wait > 0:
            scene.wait(to_wait)
        previous_t = t
        if not isinstance(anims, Iterable):
            anims = [anims]
        for anim in anims:
            turn_animation_into_updater(anim)
            scene.add(anim.mobject)
            # added line to check if the animation has an attribute called sound_to_play (I guess that it can be modfidied to be .add object)
            if hasattr(anim, "sound_to_play") and anim.sound_to_play:
                scene.add_sound(anim.sound_to_play)
            ending_time = max(ending_time, t + anim.run_time)
    if ending_time > t:
        scene.wait(ending_time-t)
