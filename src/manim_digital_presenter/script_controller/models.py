"""Script records independent of rendering and presenter implementations."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DialogueEntry:
    """One script row with its original source line."""

    dialogue: str
    action: str
    argument: str = ""
    line_number: int = 0
