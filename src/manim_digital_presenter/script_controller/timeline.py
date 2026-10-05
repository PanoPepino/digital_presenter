"""Overlapping timeline playback with normal Manim animation lifecycle."""

import math
import warnings
from dataclasses import dataclass

from manim import Animation, AnimationGroup, linear
from manim.animation.animation import prepare_animation

__all__ = ["play_timeline"]


@dataclass
class _Active:
    animation: Animation
    start: float
    end: float
    finished: bool = False


class _TimelineSegment(AnimationGroup):
    """Advance already-begun animations across one scheduler interval.

    AnimationGroup exposes child families to Manim's moving-object detection.
    Setup and completion belong to the scheduler, not to individual segments.
    """

    def __init__(self, active, start, duration, finish_due):
        self.active = tuple(active)
        self.start = start
        self._last_time = start
        self._finish_due = finish_due
        super().__init__(*(item.animation for item in active), run_time=duration,
                         rate_func=linear, introducer=True)

    def _setup_scene(self, scene):
        pass

    def begin(self):
        self.interpolate(0)

    def interpolate(self, alpha):
        time = self.start + max(0.0, min(1.0, alpha)) * self.run_time
        dt = max(0.0, time - self._last_time)
        for item in self.active:
            if item.finished:
                continue
            item.animation.update_mobjects(dt)
            item.animation.interpolate(min(1.0, (time - item.start) /
                                            item.animation.run_time))
        self._last_time = time
        self._finish_due(time)

    def update_mobjects(self, dt):
        # Updates use actual scheduler time in interpolate, including final frame.
        pass

    def finish(self):
        self.interpolate(1)

    def clean_up_from_scene(self, scene):
        pass


def _animations(value):
    if callable(value) and not isinstance(value, Animation) and not hasattr(value, "build"):
        value = value()
    if isinstance(value, (list, tuple)):
        for item in value:
            yield from _animations(item)
    else:
        yield prepare_animation(value)


def _family(animation):
    if isinstance(animation, AnimationGroup):
        return set().union(*(_family(child) for child in animation.animations))
    return set(animation.mobject.get_family()) if animation.mobject is not None else set()


def play_timeline(scene, timeline):
    """Play timestamped animations, builders, factories, or lists of these.

    Times are relative to this call. Factories run at their event start, so use
    ``lambda: mob.animate.shift(UP)`` when earlier events change the same object.
    Eager builders cannot recover targets overwritten before this call.
    Overlapping ownership warns; independent objects may overlap freely.
    """
    events = []
    for time, value in timeline.items():
        if not isinstance(time, (int, float)) or not math.isfinite(time) or time < 0:
            raise ValueError("Timeline timestamps must be finite and nonnegative")
        events.append((float(time), value))
    events.sort(key=lambda event: event[0])
    active = []
    cursor = 0.0

    def finish_due(time=None):
        for item in tuple(active):
            if item.end <= (cursor if time is None else time) + 1e-12:
                active.remove(item)
                item.finished = True
                try:
                    item.animation.finish()
                finally:
                    item.animation.clean_up_from_scene(scene)

    def advance_to(end):
        nonlocal cursor
        duration = end - cursor
        if duration > 1e-12:
            if active:
                scene.play(_TimelineSegment(active, cursor, duration, finish_due))
            else:
                scene.wait(duration)
        cursor = end
        finish_due()

    try:
        for time, value in events:
            advance_to(time)
            finish_due()
            for animation in _animations(value):
                duration = animation.run_time
                if not math.isfinite(duration) or duration < 0:
                    raise ValueError("Animation duration must be finite and nonnegative")
                family = _family(animation)
                if any(family & _family(item.animation) for item in active):
                    warnings.warn("Timeline animations overlap on the same mobject family",
                                  RuntimeWarning, stacklevel=2)
                scene.add_mobjects_from_animations([animation])
                animation._setup_scene(scene)
                item = _Active(animation, cursor, cursor + duration)
                try:
                    animation.begin()
                except Exception:
                    # A failed begin has no valid interpolation state to finish.
                    if animation.mobject is not None:
                        animation.mobject.resume_updating()
                    animation.clean_up_from_scene(scene)
                    raise
                active.append(item)
                sound = getattr(animation, "sound_to_play", None)
                if sound:
                    scene.add_sound(sound)
                finish_due()
        while active:
            advance_to(max(item.end for item in active))
    finally:
        # Recover suspended objects even when a factory or playback raises.
        for item in tuple(active):
            try:
                item.animation.finish()
            finally:
                item.animation.clean_up_from_scene(scene)
