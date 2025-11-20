from manim import *


def code_exporter(code_string):
    to_export = Code(
        code_string=code_string,
        language="python",
        background="window",
        background_config={"stroke_color": DARK_BLUE,
                           "fill_color": BLACK,
                           "fill_opacity": 0.8}).to_corner(LEFT)
    return to_export


code_import = '''from manim import *
from manim_digital_presenter import * '''

cc = code_exporter(code_import)
