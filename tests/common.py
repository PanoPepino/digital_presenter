"""Isolated Manim fixtures and deterministic scene playback."""

import tempfile
import unittest
from math import ceil

from manim import Scene, tempconfig


class ManimTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="presenter-test-")
        self.addCleanup(directory.cleanup)
        context = tempconfig({"media_dir": directory.name, "disable_caching": True,
                              "write_to_movie": False, "save_last_frame": False,
                              "pixel_width": 320, "pixel_height": 180,
                              "frame_rate": 15})
        context.__enter__()
        self.addCleanup(context.__exit__, None, None, None)


class SteppedScene(Scene):
    """Use real scene membership and update logic without rendering."""

    def __init__(self):
        super().__init__()
        self.elapsed = 0.0
        self.sounds = []

    def play(self, animation, **kwargs):
        self.add_mobjects_from_animations([animation])
        animation._setup_scene(self)
        animation.begin()
        count = max(1, ceil(animation.run_time * 120))
        dt = animation.run_time / count
        for step in range(1, count + 1):
            animation.update_mobjects(dt)
            animation.interpolate(step / count)
            self.update_mobjects(dt)
        animation.finish()
        animation.clean_up_from_scene(self)
        self.elapsed += animation.run_time

    def wait(self, duration=1, **kwargs):
        self.update_mobjects(duration)
        self.elapsed += duration

    def add_sound(self, sound, **kwargs):
        self.sounds.append((self.elapsed, sound))
