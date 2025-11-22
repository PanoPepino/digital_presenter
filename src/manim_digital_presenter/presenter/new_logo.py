"""Modified Manim Banner for Digital Presenter with pixelated style."""

from __future__ import annotations

__all__ = ["DigitalPresenterBanner"]

from scipy.fftpack import shift
import svgelements as se

from manim.animation.updaters.update import UpdateFromAlphaFunc
from manim.mobject.geometry.arc import Circle
from manim.mobject.geometry.polygram import Square, Triangle, Rectangle
from manim import *
from manim.animation.animation import override_animation
from manim.animation.composition import AnimationGroup, Succession
from manim.animation.creation import Create, SpiralIn
from manim.animation.fading import FadeIn
from manim.mobject.svg.svg_mobject import VMobjectFromSVGPath
from manim.mobject.types.vectorized_mobject import VGroup
from manim.utils.rate_functions import ease_in_out_cubic, smooth


def create_pixelated_letter(letter, width=1.0, height=1.5):
    """Create a pixelated version of a letter using small squares."""

    # Define pixel patterns for each letter (1 = filled, 0 = empty)
    # Each letter is represented as a grid
    patterns = {
        'D': [
            [1, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 0],
        ],
        'i': [
            [1],
            [0],
            [1],
            [1],
            [1],
            [1],
            [1],
        ],
        'g': [
            [0, 1, 1, 1],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 1],
        ],
        'i2': [  # second 'i'
            [1],
            [0],
            [1],
            [1],
            [1],
            [1],
            [1],
        ],
        't': [
            [0, 1, 0],
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 1],
        ],
        'a': [
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
        ],
        'l': [
            [1, 0,0],
            [1, 0,0],
            [1, 0,0],
            [1, 0,0],
            [1, 0,0],
            [1, 0,0],
            [1, 1,0],
        ],
        'P': [
            [1, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
        ],
        'r': [
            [1, 1, 1],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
        ],
        'e': [
            [0, 1, 1, 1],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 1, 1, 1],
        ],
        's': [
            [0, 1, 1, 1],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [1, 1, 1, 0],
        ],
        'n': [
            [1, 0, 0, 1],
            [1, 1, 0, 1],
            [1, 0, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
        ],
    }

    if letter not in patterns:
        return VGroup()

    pattern = patterns[letter]
    rows = len(pattern)
    cols = len(pattern[0]) if rows > 0 else 0

    # Calculate pixel size
    pixel_size = min(width / cols, height / rows) * 0.9

    pixels = VGroup()
    for i, row in enumerate(pattern):
        for j, pixel in enumerate(row):
            if pixel == 1:
                square = Square(side_length=pixel_size)
                square.set_fill(opacity=1)
                square.set_stroke(width=0)
                # Position the pixel
                x_pos = (j - cols/2 + 0.5) * pixel_size
                y_pos = (rows/2 - i - 0.5) * pixel_size
                square.move_to([x_pos, y_pos, 0])
                pixels.add(square)

    return pixels


class DigitalPresenterBanner(VGroup):
    """
    Digital Presenter Banner with pixelated letters.

    Similar to ManimBanner but displays "Digital Presenter" with
    pixelated letters and shows only D and P initially.

    Parameters
    ----------
    dark_theme
        If ``True`` (the default), the dark theme version of the logo
        (with light text font) will be rendered. Otherwise, if ``False``,
        the light theme version (with dark theme text font) is used.

    Examples
    --------
    .. manim:: DigitalPresenterExample

        class DigitalPresenterExample(Scene):
            def construct(self):
                banner = DigitalPresenterBanner()
                self.play(banner.create())
                self.play(banner.expand())
                self.wait()

    """

    def __init__(self, dark_theme: bool = True):
        super().__init__()

        logo_green = GREEN
        logo_blue = BLUE
        logo_red = RED

        self.font_color = "#ece6e2" if dark_theme else "#343434"
        self.scale_factor = 1

        # Create D (capital D)
        self.D = create_pixelated_letter('D', width=0.8, height=1.2)
        self.D.set_fill(color=self.font_color, opacity=1)
        self.D.scale(1.8)
        self.D.shift(2.25 * LEFT + 2 * UP)

        # Create P (capital P) - will be below D initially
        self.P = create_pixelated_letter('P', width=0.8, height=1.2)
        self.P.set_fill(color=self.font_color, opacity=1)
        self.P.scale(1.8)
        self.P.next_to(self.D, DR, buff=0.1)

        # Create the initial D-P stack
        self.DP = VGroup(self.D, self.P)
        self.DP.move_to(2 * LEFT + 0.05 * DOWN)

        # Create shapes (same as original)
        self.circle = Circle(color=logo_green, fill_opacity=1).shift(LEFT)
        self.square = Square(color=logo_blue, fill_opacity=1).shift(UP)
        self.triangle = Triangle(color=logo_red, fill_opacity=1).shift(RIGHT)
        self.shapes = VGroup(self.triangle, self.square, self.circle)

        self.add(self.shapes, self.DP)
        self.move_to(ORIGIN)

        # Create "igital" text (without 'D')
        digital_letters = VGroup()
        letters_digital = ['i', 'g', 'i2', 't', 'a', 'l']
        for letter in letters_digital:
            pixel_letter = create_pixelated_letter(letter, width=1, height=1.3)
            pixel_letter.set_fill(color=self.font_color, opacity=1)
            pixel_letter
            if len(digital_letters) > 0:
                pixel_letter.next_to(digital_letters, RIGHT, buff=0.05).set_z_index(10)
            digital_letters.add(pixel_letter)

        # Create "resenter" text (without 'P')
        presenter_letters = VGroup()
        letters_presenter = ['r', 'e', 's', 'e', 'n', 't', 'e', 'r']
        for letter in letters_presenter:
            pixel_letter = create_pixelated_letter(letter, width=1, height=1.3)
            pixel_letter.set_fill(color=self.font_color, opacity=1)
            pixel_letter
            if len(presenter_letters) > 0:
                pixel_letter.next_to(presenter_letters, RIGHT, buff=0.05).set_z_index(10)
            presenter_letters.add(pixel_letter)

        # Position the expanding text
        # "igital" should expand from D
        # "resenter" should expand from P

        # Create combined text group for "Digital Presenter"
        self.digital_text = digital_letters
        self.presenter_text = presenter_letters

        # Position text relative to D and P
        self.digital_text.next_to(self.D, RIGHT, buff=0.01)
        self.digital_text.align_to(self.D, DOWN)

        self.presenter_text.next_to(self.P, RIGHT, buff=0.01)
        self.presenter_text.align_to(self.P, DOWN)

        # Combine both expanding texts
        self.expanding_text = VGroup(self.digital_text, self.presenter_text)

        # Note: expanding_text is only shown in the expanded state
        # and thus not yet added to the submobjects of self.

    def scale(self, scale_factor: float, **kwargs) -> "DigitalPresenterBanner":
        """Scale the banner by the specified scale factor."""
        self.scale_factor *= scale_factor
        # Note: self.expanding_text is only added to self after expand()
        if self.expanding_text not in self.submobjects:
            self.expanding_text.scale(scale_factor, **kwargs)
        return super().scale(scale_factor, **kwargs)

    @override_animation(Create)
    def create(self, run_time: float = 2) -> AnimationGroup:
        """The creation animation for the Digital Presenter logo."""
        return AnimationGroup(
            FadeIn(self.shapes, run_time=run_time, shift=5*RIGHT),
            FadeIn(self.DP, run_time=run_time, shift=5*LEFT),
            lag_ratio=0,
        )

    def expand(self, run_time: float = 1.5, direction="center") -> Succession:
        """An animation that expands the logo into its banner.

        The returned animation transforms the banner from its initial
        state (showing only D and P) to its expanded state 
        (showing "Digital Presenter").
        """
        if direction not in ["left", "right", "center"]:
            raise ValueError("direction must be 'left', 'right' or 'center'.")

        dp_shape_offset = 6.25 * self.scale_factor
        shape_sliding_overshoot = self.scale_factor * 0.8
        dp_text_buff = 0.06

        self.digital_text.next_to(self.D, RIGHT, buff=dp_text_buff).align_to(self.D, DOWN)
        self.presenter_text.next_to(self.P, RIGHT, buff=dp_text_buff).align_to(self.P, DOWN)
        self.expanding_text.set_opacity(0)

        self.shapes.save_state()

        # Clone for animation effect
        p_clone = self.presenter_text[-1].copy()
        self.add(p_clone)
        p_clone.move_to(self.shapes)

        self.DP.save_state()

        left_group = VGroup(self.DP, self.expanding_text, p_clone)

        def shift(vector):
            self.shapes.restore()
            left_group.align_to(self.DP.saved_state, LEFT)
            if direction == "right":
                self.shapes.shift(vector)
            elif direction == "center":
                self.shapes.shift(vector / 4)
                left_group.shift(-vector / 4)
            elif direction == "left":
                left_group.shift(-vector)

        def slide_and_uncover(mob, alpha):
            shift(alpha * (dp_shape_offset + shape_sliding_overshoot) * RIGHT)
            # Add letters when they are uncovered
            for letter in mob.expanding_text:
                if mob.square.get_center()[0] > letter.get_center()[0]:
                    letter.set_opacity(1)
                    self.add_to_back(letter)
            # Finish animation
            if alpha == 1:
                self.remove(*[self.expanding_text])
                self.add_to_back(self.expanding_text)
                mob.shapes.set_z_index(1)
                mob.shapes.save_state()
                mob.DP.save_state()

        def slide_back(mob, alpha):
            if alpha == 0:
                p_clone.set_opacity(1)
                p_clone.move_to(mob.presenter_text[-1])
                mob.expanding_text.set_opacity(1)
            shift(alpha * shape_sliding_overshoot *0.9* LEFT)
            if alpha == 1:
                mob.remove(p_clone)
                mob.add_to_back(mob.shapes)

        return Succession(
            UpdateFromAlphaFunc(
                self,
                slide_and_uncover,
                run_time=run_time * 1 / 3,
                rate_func=ease_in_out_cubic,
            ),
            UpdateFromAlphaFunc(
                self,
                slide_back,
                run_time=run_time * 1 / 3,
                rate_func=ease_in_out_cubic,
            ),
        )
