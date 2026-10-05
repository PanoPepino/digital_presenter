"""Resolve script arguments and actions without presenter-class dependencies."""

import ast
from collections.abc import Mapping

import numpy as np
from manim import (Animation, UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR,
                   IN, OUT, ORIGIN)
from manim.animation.animation import prepare_animation

_VECTORS = {"UP": UP, "DOWN": DOWN, "LEFT": LEFT, "RIGHT": RIGHT,
            "UL": UL, "UR": UR, "DL": DL, "DR": DR,
            "IN": IN, "OUT": OUT, "ORIGIN": ORIGIN}


def parse_value(argument: str, symbols: Mapping | None = None):
    """Resolve constants, named objects, Python literals, or literal strings."""
    argument = argument.strip()
    if not argument:
        return None
    if argument in _VECTORS:
        return _VECTORS[argument].copy()
    if symbols is not None and argument in symbols:
        return symbols[argument]
    try:
        value = ast.literal_eval(argument)
    except (ValueError, SyntaxError):
        return argument
    return np.array(value) if isinstance(value, list) else value


def resolve_action(owner, entry, *, symbols=None, actions=None,
                   run_time=None, source="script") -> Animation:
    """Invoke a public action and verify its animation result with line context."""
    context = f"{source}:{entry.line_number}: action {entry.action!r}"
    try:
        if entry.action.startswith("_"):
            raise ValueError("private actions are not allowed")
        method = (actions[entry.action] if actions is not None and entry.action in actions
                  else getattr(owner, entry.action))
        if not callable(method):
            raise TypeError("action must be callable")
        result = (method(parse_value(entry.argument, symbols))
                  if entry.argument.strip() else method())
        animation = prepare_animation(result)
        if run_time is not None:
            animation.set_run_time(run_time)
        return animation
    except (AttributeError, TypeError, ValueError, KeyError) as error:
        raise ValueError(f"{context}: {error}") from error
