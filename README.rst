===
ped
===

Open a python module in your text editor.

::

    $ ped django
    $ ped django.core.urlresolvers
    $ ped django.shortcuts -e vim


``ped`` will find your modules in the currently-active virtual environment.


Get it now
**********
::

    $ pip install ped


Changing the default editor
***************************

``ped`` will try to find your favorite text editor. If you want to override the editor ``ped`` uses, set the ``PED_EDITOR`` environment variable.

::

    # .zshrc or .bashrc
    # Use Sublime Text with ped
    export PED_EDITOR=subl


Kudos
*****

This was inspired by `IPython's <https://ipython.org/>`_ ``%edit`` magic.


Changelog
*********

1.0.2
-----

- Fix for editing subpackages, e.g. ``ped pkg.subpkg``.
