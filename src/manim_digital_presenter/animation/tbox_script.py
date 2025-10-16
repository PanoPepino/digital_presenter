from manim import *
import csv

__all__ = []

# ---------------- THIS SEEMS TO BE REQUIRED TO BE TRANSFORMED INTO A CLASS.-----------------------

# Tex properties. Important to adjust enviroment and font depending on the size of the box.
Tex.set_default(tex_template=TexFontTemplates.comic_sans)
Tex.set_default(color=WHITE)
tex_env = "{minipage}"
font_tex = 35

# Dialogue and Actions
# This will create two list, read from a csv file that contains the script of what the creature should do and say. Each line corresponds to one action/thing to say. The second entry (thing to say) will be transformed into tex, stored in VGroup of tex and displayed inside the textbox.

# CAREFUL WITH CSV. IF EMPTY LINE AT THE END, IT WILL COMPLAIN!
actions_example = []
dialogue_example = []

with open('dialogue/example_script.csv') as file_to_read:
    script = csv.reader(file_to_read, delimiter='/')
    for row in script:
        actions_example.append(row[0])
        dialogue_example.append(row[1])

# The text box where the text will be placed
text_box = RoundedRectangle(width=config["frame_width"]-3, height=config['frame_height']/5,
                            fill_color=[DARK_BLUE, BLACK], fill_opacity=0.1, color=DARK_BLUE).to_corner(DR, buff=0.1)
text_box.set_sheen_direction(0.5*DOWN)

# The triangle to simulate next text (similar to next dialogue in videogames)
triangle_next_text = Triangle(color=[DARK_BLUE, BLACK], fill_opacity=0.8).rotate(
    PI/3).scale(0.15).next_to(text_box, RIGHT, buff=-0.6)

# Creating the tex group with the text
text_example = VGroup(*[Tex(line,  font_size=font_tex) for line in dialogue_example]).move_to(text_box.get_center())
