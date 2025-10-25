# About Digital_presenter
---------------------------------------------------------------------


Repository of Manim to create a digital companion to present your videos, slides, etc. This creature can be manually animated calling some methods of the class. In addition, it can also be animated following a script, in the form of .csv or .txt file. This script will contain some text to be displayed on the screen. At the same time, it will contain a column with the action the creature will display. In this way, one can synchronise text and action for a more natural and fluid presentation.

The creature will be composed with a pair of eyes, a core and, optionally, a pair of hands. Each of this pieces can be animated to make the creature feel alive (see EXAMPLES for more information.)


-----------------------------------------------------------------------

:memo: **Note**
- Note each creature you may design will require adjusting the position of shoulders, eyes, body, hands, depending on its form. This can be easily done with the inbuilt parameters (See DOCUMENTATION)

-----------------------------------------------------------------------

:warning: **Warning**

[TO BE IMPROVED]

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

- Fix eye_lid and rimmel thickness and strange issue going on there. [_]
- Reestructure the animation class to be used with timeline. Add same animations as inbuilt methods of class Creature[_]
- Reestructure how the textbox and similar objects are called through the script function. Better to define a set of classes? [_]
- Create simple logo to add to github and webpage. [_]
- To write down good docstrings for documentation. [_]
- To create documentation and deploy in webpage. Use beanim-like structure. [_]


