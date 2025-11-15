from manim import *
import csv

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
    :type box_position: str, optional

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
           triangle_color=YELLOW,
           box_position="DL"
       )
       scene.add(custom_box)

    """

    def __init__(
        self,
        width: float = None,
        height: float = None,
        box_fill_color: list | str = [DARK_BLUE, BLACK],
        box_fill_opacity: float = 0.1,
        box_color: str = DARK_BLUE,
        box_position: list = DR,
        box_buff: float = 0.1,
        corner_box: float = 0.2,
        **kwargs):
        super().__init__(**kwargs)

        if width is None:
            width = config["frame_width"] - 3
        if height is None:
            height = config["frame_height"] / 5

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



