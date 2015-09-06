===
ped
===

Open a python module in your text editor.

::

    $ ped django
    $ ped flask -e vim


``ped`` will find your modules in the currently-active virtual environment.


Get it now
----------
::

    $ pip install ped


Changing the default editor
---------------------------

``ped`` will try to find your favorite text editor. If you want to override the editor ``ped`` uses, set the ``PED_EDITOR`` environment variable.

::

    # .zshrc or .bashrc
    # Use Sublime Text with ped
    export PED_EDITOR=subl
