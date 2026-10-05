"""Read-only Sphinx configuration; resolve paths relative to this file."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

project = "Digital Presenter"
copyright = "2025, Pano"
author = "Pano"
extensions = [
    "sphinx.ext.autodoc", "sphinx.ext.autosummary", "sphinx.ext.viewcode",
    "sphinx.ext.napoleon", "sphinx.ext.intersphinx", "sphinx.ext.mathjax",
    "sphinx_copybutton",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"
html_theme = "furo"
html_static_path = ["_static"]
html_logo = "_static/media/logo.svg"
html_baseurl = "https://panopepino.github.io/digital_presenter/"
html_file_suffix = ".html"
html_link_suffix = ".html"
add_module_names = False
toc_object_entries = True
toc_object_entries_show_parents = "hide"
autodoc_class_signature = "separated"
autoclass_content = "class"
autodoc_default_options = {"members": True, "exclude-members": "__weakref__, __init__"}
autosummary_generate = False
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
mathjax3_config = {
    "tex": {
        "inlineMath": [["$", "$"], [r"\(", r"\)"]],
        "displayMath": [["$$", "$$"], [r"\[", r"\]"]],
    }
}
