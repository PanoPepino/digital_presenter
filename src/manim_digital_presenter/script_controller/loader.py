"""CSV parsing with a compatibility facade for dialogue rendering."""

import csv
from os import PathLike

from .models import DialogueEntry

__all__ = ["load_csv_dialogue", "create_dialogue_tex"]


def load_entries(csv_path: str | PathLike, delimiter: str = "/") -> list[DialogueEntry]:
    """Read dialogue/action[/argument] rows; ignore blank rows."""
    entries = []
    with open(csv_path, encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source, delimiter=delimiter, strict=True)
        try:
            for row in reader:
                if not row or all(not value.strip() for value in row):
                    continue
                # Legacy tutorial files include an extra trailing delimiter.
                if len(row) > 3 and all(not value.strip() for value in row[3:]):
                    row = row[:3]
                if len(row) not in (2, 3):
                    raise ValueError(f"{csv_path}:{reader.line_num}: expected 2 or 3 columns")
                if not row[1].strip():
                    raise ValueError(f"{csv_path}:{reader.line_num}: action must not be empty")
                entries.append(DialogueEntry(row[0], row[1].strip(),
                                             row[2] if len(row) == 3 else "",
                                             reader.line_num))
        except csv.Error as error:
            raise ValueError(f"{csv_path}:{reader.line_num}: {error}") from error
    return entries


def load_csv_dialogue(csv_path: str | PathLike, delimiter: str = "/") -> tuple[
    list[str], list[str], list[str]
]:
    """Return (dialogue, actions, arguments); omitted arguments become empty strings."""
    entries = load_entries(csv_path, delimiter)
    return ([entry.dialogue for entry in entries],
            [entry.action for entry in entries],
            [entry.argument for entry in entries])


def __getattr__(name):
    # Keep parsing itself free of rendering imports.
    if name == "create_dialogue_tex":
        from .rendering import create_dialogue_tex
        return create_dialogue_tex
    raise AttributeError(name)
