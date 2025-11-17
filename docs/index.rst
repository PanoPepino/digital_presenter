Digital Presenter
=================

Welcome to the documentation of Digital Presenter, a Manim package to create a simple digital creature that acts as a presenter of your video, slides, or lecture. 

With very simple commands, you will be able to animate a character that will guide your audience through the content you want to share.

This is a simple example of what can be done with this package:

(THINK HOW TO ADD A VIDEO HERE)


First Steps
-----------

You can find the repository of this package in  `Github <https://github.com/PanoPepino/digital_presenter>`_.

If you want to install the package, please follow the instructions in :doc:`installation`.

After installation, you can find the most straightforward explanation of the basic features of this package in :doc:`how_to_use`.

More Advanced Examples
----------------------

The following `Youtube playlist <https://www.youtube.com/watch?v=MEuX53M5mBU&list=PL7qJnArvRQzHci5IAHRqCuS2eF4_baHTR>`_ correspond to a series of videos prepared with a rudimentary version of this package. However, they can give you an idea of the kind of animations you can create with it.

.. note::
    Note that the previous videos correspond to an older version of the package, so some things may have changed. (Syntaxis and package structure are way more straightforward and clean now!!)

Learning to Use the Package
---------------------------

If you want more detailed explanations, see :doc:`how_to_use` and the :doc:`api/modules`. For easy navigation, note that:

- :doc:`api/manim_digital_presenter.presenter` contains the main classes to create and animate the digital presenter.
- :doc:`api/manim_digital_presenter.script_controller` contains the classes to control the script of an automatic presentation, making use of a timeline where the actions of the presenter and the overall animations will be controlled iteratively

---------------------------------------------------------------------------------------------

.. warning::

   This is a package under construction. New features and a more optimised organisation will come. Also, if you are an expert in this kind of things, and want to collaborate, you are more than welcome to enhance this humble library! In case you find some and/or have some suggestions, please
   report at `github issues <https://github.com/PanoPepino/beanim/issues>`_.
   
.. note::

   I would like to thank Abulafia (the creator of the `timeline <https://github.com/abul4fia/manim-play-timeline> _` Manim plugging) and Uwezi (and all the `Manim CE Discord <https://discord.gg/nfJXC2qh>`_ by extension) for unvaluable help when I was crafting this package.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   how_to_use
   api/modules
   
   