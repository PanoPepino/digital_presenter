Digital Presenter
=================

Welcome to the documentation of Digital Presenter, a Manim package to create a simple digital companion that acts as a presenter of your video, slides, lecture, etc. 

With very simple commands, you will be able to animate a character that will guide your audience through the content you want to share.

This is a simple example of what your digital presenter can do:

.. raw:: html

   <div style="text-align: center;">
  <video
     src="_static/media/videos/Logo_Demo.mp4"
     autoplay
     loop
     muted
     playsinline
     controls
     style="max-width: 100%; height: auto; border: 2px solid #000000; border-radius: 8px;">
    Your browser does not support the video tag.
  </video>
   </div>


First Steps
-----------

You can find the repository of this package in  `Github <https://github.com/PanoPepino/digital_presenter>`_.

If you want to install the package, please follow the instructions in :doc:`installation`.

After installation, you can find the most straightforward explanation of the basic features of this package in :doc:`how_to_use`.

Advanced Examples
----------------------

The following `Youtube playlist <https://www.youtube.com/watch?v=MEuX53M5mBU&list=PL7qJnArvRQzHci5IAHRqCuS2eF4_baHTR>`_ correspond to a series of videos prepared with a rudimentary version of this package. However, they can give you an idea of the kind of animations you can create with it. You can also find more convoluted pieces of code in :doc:`examples`.

.. note::
    Note that the previous videos correspond to an older version of the package, so some things may have changed. (Syntaxis and package structure are way more straightforward and clean now!!)

Learning to Use the Package
---------------------------

If you want more detailed explanations, see :doc:`how_to_use` and the :doc:`api/modules`. For easy navigation, note that:

- :doc:`api/manim_digital_presenter.presenter` contains the main classes to create and animate the digital presenter.
- :doc:`api/manim_digital_presenter.script_controller` contains the classes to control the script of an automatic presentation, making use of a timeline where the actions of the presenter and the overall animations will be controlled iteratively

------------------------------------------------

.. warning::

   This is a package under construction. New features and a more optimised organisation will come. In case you find some and/or have some suggestions, please report at `github issues <https://github.com/PanoPepino/beanim/issues>`_.
   
.. note::

   I would like to thank Abulafia (the creator of the `timeline <https://github.com/abul4fia/manim-play-timeline>`_ Manim plugging) and Uwezi (and all the `Manim CE Discord <https://discord.gg/nfJXC2qh>`_ by extension) for unvaluable help when I was crafting this package.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   how_to_use
   examples
   api/modules


----

.. raw:: html

   <div style="text-align: center; margin: 30px 0;">
     <p style="font-size: 16px; margin-bottom: 15px;">
       💖 <strong>If you find this project helpful, consider supporting its development. Thank you!</strong>
     </p>
     <a href="https://www.buymeacoffee.com/panopepino" target="_blank">
       <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
            alt="Buy Me A Coffee" 
            style="height: 50px; border-radius: 10px;">
     </a>
   </div>

