from manim import *
import csv

__all__ = ["load_csv_dialogue", "create_dialogue_tex"]

def load_csv_dialogue(csv_path: str, 
                      delimiter: str = '/') -> tuple[list[str], list[str]]:
    """
    Extract dialogue and actions from a CSV file.

    This function reads a CSV file containing a script with two columns:
    the first column contains action identifiers, and the second contains
    dialogue text. Both are returned as separate lists.

    :param csv_path: Path to the CSV file containing the script
    :type csv_path: str

    :param delimiter: Delimiter used in the CSV file. Defaults to '/'.
    :type delimiter: str

    :return: A tuple containing (actions, dialogue)
    :rtype: tuple[list[str], list[str]]
    
    :raises FileNotFoundError: If the CSV file is not found at the specified path
    :raises ValueError: If any row has fewer than 2 columns

    .. warning::
       Do NOT include empty lines at the end of the CSV file.
       Trailing empty rows will cause the function to fail.

    Example usage:

    .. code-block:: python

       from manim_digital_presenter import *
       actions, dialogue = load_csv_dialogue('your_paty/your_script.csv')

    The CSV file format should be::

        action_1/dialogue_1
        action_2/dialogue_2
        action_3/dialogue_3

    """

    actions = []
    dialogue = []

    try:
        with open(csv_path) as file_to_read:
            script = csv.reader(file_to_read, delimiter=delimiter)
            for row in script:
                if len(row) < 2:
                    raise ValueError(f"Row does not have 2 columns: {row}")
                actions.append(row[0])
                dialogue.append(row[1])
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at path: {csv_path}")

    return actions, dialogue

def create_dialogue_tex(
    dialogue: list[str],
    tex_template: type = TexFontTemplates.comic_sans,
    tex_color: str = WHITE,
    font_size: int = 35,
    position = None) -> list[VMobject]:
    """
    Convert a list of dialogue strings to Tex objects.

    :param dialogue: List of dialogue strings to convert to Tex objects
    :type dialogue: list[str]
    
    :param tex_template: LaTeX template to use for rendering. Defaults to TexFontTemplates.comic_sans
    :type tex_template: type, optional

    :param tex_color: Color for the text. Defaults to WHITE
    :type tex_color: str, optional

    :param font_size: Font size for the text in points. Defaults to 35
    :type font_size: int, optional

    :param position: Position to place all text objects. If None, no positioning is applied.
    :type position: np.ndarray, optional

    :return: List of Tex objects created from the dialogue strings
    :rtype: list[VMobject]

    Example usage:

    .. code-block:: python

       from manim_digital_presenter import *
       from manim import *

       dialogue = ["Hello!", "How are you?", "Nice to meet you!"]
       tex_objects = create_dialogue_tex(
           dialogue,
           font_size=40,
           tex_color=YELLOW
       )

    """

    Tex.set_default(tex_template=tex_template)
    Tex.set_default(color=tex_color)

    tex_objects = [Tex(line, font_size=font_size) for line in dialogue]

    if position is not None:
        for tex in tex_objects:
            tex.move_to(position)

    return tex_objects
