import math

from manim import BLACK, DARK_BLUE, DOWN, DR, RoundedRectangle, VGroup, config

import numpy as np

__all__ = ["Text_Box"]

class Text_Box(VGroup):
    """
    A simple rectangle UI element representing a dialogue box.

    :param width: Width of the dialogue box. If None, defaults to frame width - 3 units
    :type width: float, optional

    :param height: Height of the dialogue box. If None, defaults to frame height / 5
    :type height: float, optional

    :param box_fill_color: Fill color(s) for the box. Defaults to [DARK_BLUE, BLACK]
    :type box_fill_color: list | str, optional

    :param box_fill_opacity: Fill opacity for the box. Defaults to 0.1
    :type box_fill_opacity: float, optional

    :param box_color: Border color for the box. Defaults to DARK_BLUE
    :type box_color: str, optional

    :param box_position: Position of the box using corner constants (e.g., DR, DL). Defaults to DR.
    :type box_position: list | numpy.ndarray, optional

    :param box_buff: Buffer distance from the specified corner. Defaults to 0.1
    :type box_buff: float, optional

    :param corner_box: corner radius of the box. Defaults to 0.2.
    :type corner_box: float, optional

    **Example usage:**

    .. code-block:: python

       # Create with custom colors and size
       custom_box = Text_Box(
           width=10,
           height=3,
           box_fill_color=RED,
           box_position=DL
       )
       scene.add(custom_box)

    """

    def __init__(
        self,
        width: float | None = None,
        height: float | None = None,
        box_fill_color: list | str | None = None,
        box_fill_opacity: float = 0.1,
        box_color: str = DARK_BLUE,
        box_position: list | np.ndarray = DR,
        box_buff: float = 0.1,
        corner_box: float = 0.2,
        **kwargs):
        super().__init__(**kwargs)

        if width is None:
            width = config["frame_width"] - 3
        if height is None:
            height = config["frame_height"] / 5

        if any(not math.isfinite(value) or value <= 0 for value in (width, height)):
            raise ValueError("Text box width and height must be finite and positive")
        if not math.isfinite(box_fill_opacity) or not 0 <= box_fill_opacity <= 1:
            raise ValueError("box_fill_opacity must be between 0 and 1")
        if not math.isfinite(corner_box) or corner_box < 0:
            raise ValueError("corner_box must be finite and nonnegative")
        if not math.isfinite(box_buff) or box_buff < 0:
            raise ValueError("box_buff must be finite and nonnegative")
        box_position = np.array(box_position, dtype=float, copy=True)
        if box_position.shape != (3,) or not np.isfinite(box_position).all():
            raise ValueError("box_position must contain three finite coordinates")
        if box_fill_color is None:
            box_fill_color = [DARK_BLUE, BLACK]
        self.box = RoundedRectangle(
            width=width,
            height=height,
            fill_color=box_fill_color,
            fill_opacity=box_fill_opacity,
            color=box_color,
            corner_radius=corner_box
        )
        self.box.to_corner(box_position, buff=box_buff)
        self.box.set_sheen_direction(0.5 * DOWN)
        self.add(self.box)

    def get_box(self) -> RoundedRectangle:
        """Return owned dialogue rectangle without relying on Manim's fallback."""
        return self.box
