import ast
from ..my_imports import *
from .loader import *


__all__ = ["script_sequencer"]


def script_sequencer(
        csv_path: str,
        the_creature: VMobject,
        text_box: VMobject = None,
        animation_rt: float = 3,
        tex_template: type = TexFontTemplates.comic_sans,
        tex_color: ParsableManimColor = RED,
        font_size: int = 35,
        fade_last: bool = True,
        scene_locals: dict = None):
    """
    Process CSV file to create synchronized dialogue and animation sequences. :func:`load_csv_dialogue` and :func:`create_dialogue_tex` are used internally. 

    :param csv_path: Path to the CSV file containing three columns: dialogue, actions, and args.
    :type csv_path: str

    :param the_creature: The Manim VMobject (creature) to animate.
    :type the_creature: VMobject

    :param text_box: Optional Text_Box object to display dialogue. If provided, text will be positioned inside the box with automatic triangle animations.
    :type text_box: Text_Box, optional

    :param animation_rt: Run time for animations in seconds. Defaults to 3 seconds.
    :type animation_rt: float, optional

    :param tex_template: TeX template class for rendering dialogue text.
    :type tex_template: type, optional

    :param tex_color: Color for the dialogue text. Defaults to RED.
    :type tex_color: str, optional

    :param font_size: Font size in points. Defaults to 35.
    :type font_size: int, optional

    :param fade_last: If True, fade out the last text entry. Defaults to True.
    :type fade_last: bool, optional

    :param scene_locals: Dictionary of local variables from the scene (pass ``locals()``). This allows referencing any variable defined in the scene by name in the CSV.
    :type scene_locals: dict, optional

    .. note::
        This function is a generator that yields lists of Manim animations for each dialogue entry. In order to execute the animations, you need to iterate through the generator and play each list of animations in your Manim scene. This can be done using a loop or by manually calling `next()` on the generator.

        You can find more information in the how_to_use documentation.

    **Example usage:**

    .. code-block:: python

        from manim import *
        from manim_digital_creature import *

        class Script_Iterator_Example(Scene):
            def construct(self):

                my_creature = Creature(...)  # Initialize your creature here
                text_box = Text_Box(...)    # Initialize your text box here
                ...
                script = script_sequencer(
                    csv_path="path/to/your_script.csv",
                    the_creature=my_creature,
                    text_box=text_box,
                    animation_rt=2.5,
                    tex_color=BLUE,
                    font_size=36,
                    scene_locals=locals())

    """

    dialogue, actions, args = load_csv_dialogue(csv_path)
    sentences_tex = create_dialogue_tex(
        dialogue,
        tex_template=tex_template,
        tex_color=tex_color,
        font_size=font_size
    )

    # Get text_box components if provided
    if text_box is not None:
        box_obj = text_box.get_box()

        # Position each text inside the box
        for tex in sentences_tex:
            tex.move_to(box_obj.get_center())

    # Iterate through all entries
    for iteration in range(len(sentences_tex) + bool(fade_last)):

        if iteration < len(sentences_tex):
            # Get creature animation
            creature_act = _create_method_animation(
                the_creature,
                actions[iteration],
                args[iteration],
                scene_locals)

            text_write_time = 1/2 * animation_rt

            if iteration == 0:
                # First iteration: just write text, animate creature, then show triangle
                if text_box is not None:
                    counter_script = [
                        Create(sentences_tex[iteration], run_time=text_write_time),
                        creature_act]
                else:
                    counter_script = [
                        Create(sentences_tex[iteration], run_time=text_write_time),
                        creature_act]
            else:
                # Subsequent iterations: fade out old text and triangle, then write new text and animate
                if text_box is not None:
                    counter_script = [
                        # First: fade out previous text and triangle together
                        FadeOut(sentences_tex[iteration-1], run_time=0.08),
                        # Then: write new text and animate creature simultaneously
                        Create(sentences_tex[iteration], run_time=text_write_time),
                        creature_act,
                        # Finally: show triangle with la
                    ]
                else:
                    counter_script = [
                        FadeOut(sentences_tex[iteration-1], run_time=0.08),
                        Create(sentences_tex[iteration], run_time=text_write_time),
                        creature_act
                    ]

        # Final iteration: fade out last text and triangle
        elif iteration == len(sentences_tex):
            if text_box is not None:
                counter_script = [
                    AnimationGroup(
                        FadeOut(sentences_tex[iteration-1], run_time=0.08),

                    )
                ]
            else:
                counter_script = [FadeOut(sentences_tex[iteration-1], run_time=0.08)]

        # Fallback
        else:
            counter_script = [Wait(0.001)]

        yield counter_script


def _create_method_animation(
        the_object: VMobject,
        the_method: str,
        the_arg: str,
        scene_locals: dict = None):
    """
    Create animation by dynamically calling a method on an object.

    :param the_object: The Manim object on which to call the method.
    :type the_object: VMobject

    :param the_method: Name of the method to call.
    :type the_method: str

    :param the_arg: Argument string from CSV file.
    :type the_arg: str

    :param scene_locals: Dictionary of local variables for object lookup.
    :type scene_locals: dict, optional

    """

    if not the_arg or the_arg.strip() == "":
        method = getattr(the_object, the_method)
        animation = method()
    else:
        parsed_arg = _parse_value(the_arg.strip(), scene_locals)
        method = getattr(the_object, the_method)
        animation = method(parsed_arg)

    return animation


def _parse_value(arg_to_eval: str, scene_locals: dict = None):
    """
    Parse string argument into appropriate Python type.

    :param arg_to_eval: String to parse.
    :type arg_to_eval: str

    :param scene_locals: Dictionary of local variables for object lookup.
    :type scene_locals: dict, optional

    """

    VECTOR_MAP = {
        'UP': UP,
        'DOWN': DOWN,
        'LEFT': LEFT,
        'RIGHT': RIGHT,
        'UL': UL,
        'UR': UR,
        'DL': DL,
        'DR': DR,
        'IN': IN,
        'OUT': OUT,
        'ORIGIN': ORIGIN,
    }

    arg_str = arg_to_eval.strip()

    if not arg_str:
        return None

    if arg_str in VECTOR_MAP:
        return VECTOR_MAP[arg_str]

    if scene_locals and arg_str in scene_locals:
        return scene_locals[arg_str]

    if arg_str.startswith('[') and arg_str.endswith(']'):
        try:
            parsed_list = ast.literal_eval(arg_str)
            return np.array(parsed_list)
        except (ValueError, SyntaxError):
            pass

    try:
        return ast.literal_eval(arg_str)
    except (ValueError, SyntaxError):
        return arg_str
