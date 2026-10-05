Installation
============

These instructions assume familiarity with git and pip. For setup help, see
`Manim Installation <https://docs.manim.community/en/stable/installation.html>`_.

What is required?
-----------------

* Python 3.11+
* `Manim Community Edition <https://docs.manim.community/en/stable/index.html>`_
* Any other package required by previous ones

How to install?
---------------

.. code-block:: bash

   cd path/to/desired/location
   git clone https://github.com/PanoPepino/digital_presenter.git
   cd digital_presenter
   pip install -e ".[examples]"

In order to check that the installation was fruitful, you can just type:

.. code-block:: bash

   pip show manim_digital_presenter

.. note::

   While the name of the repository remains as **Digital Presenter**, note that the package you are installing will be called **manim_digital_presenter**. This will group all your manim packages and addons in appropiate alphabetic order when using pip show.

Optional notebook integration
-----------------------------

Ordinary rendering uses ``from manim_slides import Slide``. Avoid wildcard
imports: these also load notebook magic and require IPython. For Jupyter usage,
install the separate notebook extra:

.. code-block:: bash

   pip install "manim-slides[magic]"

Tutorial scenes do not require an SVG exporter or write SVG files automatically.

Local documentation website
---------------------------

Run these commands from the package root using your Manim environment:

.. code-block:: bash

   python -m pip install -r docs/requirements.txt
   python scripts/serve_docs.py

Open the exact URL printed by the command. Each server uses its own fresh build,
so another build cannot remove pages from a running server. Removed-page
bookmarks redirect to the homepage. Build errors leave existing HTML intact.
Stop with Ctrl+C. After editing documentation, stop and rerun the command.
Use ``--port 0`` to select an available port or ``--port 8001`` for a specific
port. Port conflicts stop before building. Use ``--build-only`` to export fresh
HTML to ``docs/_build/html`` without starting a server. Restart older servers
launched from inside that directory after exporting; prefer this script for
serving instead.
