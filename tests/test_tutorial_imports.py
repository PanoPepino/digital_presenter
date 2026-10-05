"""Tutorial definitions must import without notebook or SVG dependencies."""

import ast
import importlib.util
import inspect
import os
import subprocess
import sys
import unittest
from pathlib import Path

from manim_digital_presenter import Creature


class TutorialImportTests(unittest.TestCase):
    def test_short_tutorial_covers_all_public_creature_animations(self):
        root = Path(__file__).resolve().parents[1]
        module = ast.parse((root / "examples/tutorials.py").read_text())
        scene = next(node for node in module.body if isinstance(node, ast.ClassDef)
                     and node.name == "Explanation_Creature_Features_Short")
        self.assertEqual([base.id for base in scene.bases], ["Scene"])
        self.assertFalse(any(isinstance(node, ast.Attribute) and node.attr == "next_slide"
                             for node in ast.walk(scene)))
        demonstrated = [node.func.attr for node in ast.walk(scene)
                        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                        and isinstance(node.func.value, ast.Name) and node.func.value.id == "c"]
        public_animations = {name for name, method in inspect.getmembers(Creature, inspect.isfunction)
                             if not name.startswith("_")
                             and {"rf", "rt"} <= set(inspect.signature(method).parameters)}
        self.assertEqual(set(demonstrated), public_animations)
        self.assertEqual(len(demonstrated), len(public_animations))

    @unittest.skipUnless(importlib.util.find_spec("manim_slides"), "Manim Slides is optional")
    def test_tutorial_import_without_ipython_or_svg_exporter(self):
        root = Path(__file__).resolve().parents[1]
        code = '''
import importlib.abc
import runpy
import sys

class BlockOptional(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in {"IPython", "manim_mobject_svg"}:
            raise ModuleNotFoundError("Blocked optional dependency", name=fullname)

sys.meta_path.insert(0, BlockOptional())
namespace = runpy.run_path(sys.argv[1])
assert all(name in namespace for name in ("Logo_Demo", "Basics_Demo", "Timeline_Demo",
                                         "Explanation_Creature_Features_Short"))
assert "IPython" not in sys.modules
assert "manim_mobject_svg" not in sys.modules
'''
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        result = subprocess.run([sys.executable, "-c", code, str(root / "examples/tutorials.py")],
                                env=environment, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
