from manim import *
import csv

__all__ = ["Text_Box"]

class Text_Box(VGroup):
    """
    A composite UI element representing a dialogue box with a next text indicator, similar to old school RPG and adventure games.

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

    :param triangle_color: Color(s) for the triangle. Defaults to [DARK_BLUE, BLACK]
    :type triangle_color: list | str, optional

    :param triangle_fill_opacity: Fill opacity for the triangle. Defaults to 0.8
    :type triangle_fill_opacity: float, optional

    :param triangle_scale: Scale factor for the triangle. Defaults to 0.15
    :type triangle_scale: float, optional

    :param box_position: Position of the box using corner names like 'DR', 'DL', 'UR', 'UL'.
                         Defaults to 'DR'
    :type box_position: str, optional

    :param box_buff: Buffer distance from the specified corner. Defaults to 0.1
    :type box_buff: float, optional

    :ivar box: The RoundedRectangle component of the dialogue box
    :vartype box: RoundedRectangle

    :ivar triangle: The Triangle component serving as the next indicator
    :vartype triangle: Triangle

    Example usage:

    .. code-block:: python

       from manim_digital_presenter import *
       from manim import *

       class MyScene(Scene):
           def construct(self):
               # Create with default settings
               text_box_ui = Text_Box()
               self.add(text_box_ui)

    Example with custom settings:

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

    .. note::
       The Text_Box automatically positions the triangle next to the box.
       The sheen direction is set to create a 3D effect on the box.

    """

    def __init__(
        self,
        width: float = None,
        height: float = None,
        box_fill_color: list | str = [DARK_BLUE, BLACK],
        box_fill_opacity: float = 0.1,
        box_color: str = DARK_BLUE,
        triangle_color: list | str = [DARK_BLUE, BLACK],
        triangle_fill_opacity: float = 0.8,
        triangle_scale: float = 0.15,
        box_position: list = DR,
        box_buff: float = 0.1,
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
            color=box_color
        )
        self.box.to_corner(box_position, buff=box_buff)
        self.box.set_sheen_direction(0.5 * DOWN)

        self.triangle = Triangle(
            color=triangle_color,
            fill_opacity=triangle_fill_opacity
        )
        self.triangle.rotate(PI / 3).scale(triangle_scale)
        self.triangle.next_to(self.box, RIGHT, buff=-0.6)

        super().__init__(self.box, self.triangle, **kwargs)

    def get_box(self) -> RoundedRectangle:
        """
        Return the dialogue box component.

        :return: The RoundedRectangle serving as the dialogue box
        :rtype: RoundedRectangle

        Example:

        .. code-block:: python

           text_box = Text_Box()
           box = text_box.get_box()
           box.set_fill(BLUE, opacity=0.5)

        """
        return self.box

    def get_triangle(self) -> Triangle:
        """
        Return the next text indicator triangle.

        :return: The Triangle serving as the "next text" indicator
        :rtype: Triangle

        """
        return self.triangle

    def get_center(self) -> np.ndarray:
        """
        Return the center position of the dialogue box.

        :return: The center coordinates of the box in 3D space
        :rtype: np.ndarray

        """
        return self.box.get_center()



