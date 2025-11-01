# About Digital_presenter
---------------------------------------------------------------------

Repository of Manim to create a digital companion to present your videos, slides, etc. You can animate it with simple commands in your Manim files!

--[ADD IMAGE HERE]--

This animated creature can be used in two different ways:

- You call it into your python script with `Creature` and animate with the inbuilt methods `Creature.animate_methods()` along the script of your video, slices, etc.
- Alternatively, you can create a .csv file with two columns as animaton/dialogue. You can then use `script_sequencer` to iterate through each of the csv lines to animate your creature and the same time it "talks" in a dialogue box on the screen.

(SEE documentation for further information)

-----------------------------------------------------------------------

:memo: **Note**
- Note each creature you may design will require adjusting the position of shoulders, eyes, body, hands, depending on its form. This can be easily done with the inbuilt parameters (See DOCUMENTATION)

-----------------------------------------------------------------------

:warning: **Warning**

- The package will be displayed in pip as **manim_digital_presenter**. This is also the way to import the package in the preamble of your python files. However, documentation and webpage will just keep the name as **digital_presenter** for simplicity.

-----------------------------------------------------------------------

## Examples

- Here you can see a demo:

https://github.com/PanoPepino/digital_presenter/assets/106378545/485839cf-4118-4f7c-86d0-20bcb2fefef4

- A more advanced example can be found in: https://www.youtube.com/watch?v=MEuX53M5mBU&list=PL7qJnArvRQzHci5IAHRqCuS2eF4_baHTR

-----------------------------------------------------------------------

## Installation and use

- In order to **install** this library, do the following:

```bash
git clone https://github.com/PanoPepino/digital_presenter

pip install digital_presenter/ .

```

- To **use** within your manim files, call it with:

```python
from manim_digital_presenter import *
```

-----------------------------------------------------------------------

# TO DO:

- Reestructure how the textbox and similar objects are called through the script function. Better to define a set of classes? [_]
- Create simple logo to add to github and webpage. [_]
- To write down good docstrings for documentation. [_]
- To create documentation and deploy in webpage. Use beanim-like structure. [_]


