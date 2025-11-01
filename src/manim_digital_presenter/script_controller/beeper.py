from ..my_imports import *

__all__ = ["Fwc"]

class Fwc(FadeOut):
    """
    New class based on FadeOut. It now adds a beep sound when fading text. The idea is to simulate the sound when you press next in majority of RPG/ graphic adventure video games.

    """

    def __init__(self,
                 sound_to_play: str = "sounds/beep.wav", 
                 **kwargs):
        super().__init__(**kwargs)
        self.sound_to_play = sound_to_play

