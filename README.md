<div align="center">

# Digital Presenter 

**A Manim extension for creating animated digital companions to improve your videos, slides, presentations!**

[Documentation](https://panopepino.github.io/digital_presenter/) • [Examples](#examples) • [Installation](#installation)

<a href="https://www.buymeacoffee.com/panopepino" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="30" />
</a>

</div>

## 📖 Overview

Digital Presenter is a Manim library that allows you to create animated creatures as digital companions for your videos, slides, and presentations. Animate them with simple commands directly in your Manim scripts!

<div align="center">
  <img src="docs/_static/media/videos/Logo_Demo.gif" alt="Digital Presenter Demo" width="700" />
</div>



## ✨ Features

Digital Presenter offers two flexible ways to animate your companion:

- **Direct scripting**: Call `Creature` in your Python script and animate using built-in methods like `Creature.happy()` or `Creature.point_at(target)` alongside your presentation code.

- **CSV-based automation**: Create a CSV file with animation/dialogue columns, then use `script_sequencer` to iterate through each line, animating your creature while displaying synchronized dialogue boxes.


## Examples

### Basic Demo
See the [documentation](https://panopepino.github.io/digital_presenter/) for the complete code of previous animation.

<div align="center">
  <img src="docs/_static/media/videos/Basics_Demo.gif" alt="Basics Demo" width="700" />
</div>




### Advanced Examples

Check out this [YouTube playlist](https://www.youtube.com/watch?v=MEuX53M5mBU&list=PL7qJnArvRQzHci5IAHRqCuS2eF4_baHTR) for more complex implementations.


## Installation

- In order to **install** this library, do the following:

```bash
git clone https://github.com/PanoPepino/digital_presenter

cd digital_presenter
pip install -e ".[examples]"
```

- To **use** within your manim files, call it with:

```python
from manim_digital_presenter import *
```

For detailed usage instructions and API reference, visit the [documentation](https://panopepino.github.io/digital_presenter/).

## Documentation deployment

In repository **Settings → Pages → Build and deployment**, set **Source** to
**GitHub Actions** once. Push package changes to `main` to build and publish the
documentation automatically. The **Deploy Sphinx Documentation** workflow runs
regression tests and a strict Sphinx build before deployment. Its deployment
environment shows the published URL. No personal access token is required.

You can also run the workflow manually from the **Actions** tab on `main`.
Ensure `.github/workflows/docs.yml` is committed at the repository root.
Static media under `docs/_static` is published as committed; deployment does not
rerender tutorial videos.

For local preview, activate your Manim environment and run:

```bash
python -m pip install -r docs/requirements.txt
python scripts/serve_docs.py --port 0
```

Open the exact URL printed by the script.

## Important Notes

> **⚙️ Customization**  
> Each creature design may require position adjustments for shoulders, eyes, body, and hands depending on its form. This can be easily configured using built-in parameters (see [documentation](https://panopepino.github.io/digital_presenter/) for details).


### 💖 Support My Work

If you find this project helpful, consider supporting me. Thank you!

<p align="center">
  <a href="https://www.buymeacoffee.com/panopepino" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50" />
  </a>
</p>

<!--
# TO DO:

- Fix Readme.md [_]
- If Mods say there is legal issue, fix logo (Substitute Manim for Digital Presenter). [_]
- Create + Add video and code for Timeline + Script Example [_]
- Create explanation slide [_]
- Add donation stuff to documentation and github [_]

-->
