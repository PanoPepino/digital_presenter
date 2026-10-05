"""Orchestrate dialogue transitions and independently resolved actions."""

import math

from manim import Create, FadeOut, RED, TexFontTemplates

from .actions import parse_value, resolve_action
from .loader import load_entries
from .models import DialogueEntry
from .rendering import create_dialogue_tex, fit_dialogue

__all__ = ["script_sequencer"]


def script_sequencer(csv_path: str, the_creature, text_box=None,
                     animation_rt: float = 3,
                     tex_template=TexFontTemplates.comic_sans,
                     tex_color=RED, font_size: int = 35,
                     fade_last: bool = True, scene_locals: dict | None = None,
                     *, symbols=None, actions=None):
    """Yield lists usable with scene.play or a deferred timeline factory.

    CSV columns are dialogue/action[/argument]. ``symbols`` names scene objects;
    ``scene_locals`` remains a legacy alternative. ``actions`` can supply custom
    callables. Every action receives ``animation_rt`` as its total duration.
    Empty scripts yield nothing. Text is rendered eagerly on first iteration.
    """
    if symbols is not None and scene_locals is not None:
        raise ValueError("Supply symbols or scene_locals, not both")
    if not math.isfinite(animation_rt) or animation_rt <= 0:
        raise ValueError("animation_rt must be finite and positive")
    symbols = scene_locals if symbols is None else symbols
    entries = load_entries(csv_path)
    if not entries:
        return
    texts = create_dialogue_tex([entry.dialogue for entry in entries],
                                tex_template, tex_color, font_size)
    if text_box is not None:
        for text in texts:
            fit_dialogue(text, text_box.box)
    for index, entry in enumerate(entries):
        animation = resolve_action(the_creature, entry, symbols=symbols,
                                   actions=actions, run_time=animation_rt,
                                   source=str(csv_path))
        step = [] if index == 0 else [FadeOut(texts[index - 1], run_time=0.08)]
        step.extend([Create(texts[index], run_time=animation_rt / 2), animation])
        yield step
    if fade_last:
        yield [FadeOut(texts[-1], run_time=0.08)]


# Compatibility for callers that imported these formerly private helpers.
def _parse_value(arg_to_eval, scene_locals=None):
    return parse_value(arg_to_eval, scene_locals)


def _create_method_animation(the_object, the_method, the_arg, scene_locals=None):
    return resolve_action(the_object, DialogueEntry("", the_method, the_arg),
                          symbols=scene_locals)
