# About Digital_presenter
---------------------------------------------------------------------

[TO BE IMPROVED]

Repository of Manim libraries to create digital presenter creature which writes and acts as written in a script (csv). 

Bla bla bla

-----------------------------------------------------------------------

[!NOTE]
- Note that you may have to change the position of shoulders, eyes, body, hands, depending on the new figures you add.
- The .csv file must not have an extra line in the end. It gives error. This requires to be fixed.
- The .csv file will be read and two lists will be created; one with emotions that the creature will represent and one with things to say, that will be written on the screen with Type animation (Abulafia)

-----------------------------------------------------------------------

[!WARNING]

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

- Fix eye_lid thickness or similar. Eyes are quite solid there. [_]
- Reestructure the animation class and methods inside creature class. [_]
    - animation class will be used inside timeline (Recall issue with passing class that are not animation) [_]
    - Methods within the class are for convinient, non-timelined projects. [_]
- Reestructure how the textbox and similar objects are called through the script function [_]
- Create simple logo to add to github and webpage. [_]
- To write down good docstrings for documentation. [_]
- To create documentation and deploy in webpage. Use beanim-like structure. [_]


