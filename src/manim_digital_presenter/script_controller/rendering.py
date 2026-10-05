"""Dialogue rendering with local styles and bounded layout."""

from manim import Tex, TexFontTemplates, VGroup, WHITE

__all__ = ["create_dialogue_tex"]


def create_dialogue_tex(dialogue: list[str],
                        tex_template=TexFontTemplates.comic_sans,
                        tex_color=WHITE, font_size: int = 35, position=None) -> VGroup:
    """Create dialogue Tex objects without changing Manim's global defaults."""
    objects = VGroup(*(Tex(line, font_size=font_size, tex_template=tex_template,
                           color=tex_color) for line in dialogue))
    if position is not None:
        for text in objects:
            text.move_to(position)
    return objects


def fit_dialogue(text, box, padding: float = 0.15):
    """Shrink oversized text proportionally and center it inside the box."""
    width, height = box.width - 2 * padding, box.height - 2 * padding
    if width <= 0 or height <= 0:
        raise ValueError("Text box must exceed twice the dialogue padding")
    ratios = [1.0]
    if text.width:
        ratios.append(width / text.width)
    if text.height:
        ratios.append(height / text.height)
    text.scale(min(ratios)).move_to(box.get_center())
