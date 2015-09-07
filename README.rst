===
ped
===

.. image:: https://img.shields.io/pypi/v/ped.svg
    :target: https://pypi.python.org/pypi/ped
    :alt: Latest version

Open python modules in your text editor.

::

    $ ped django
    $ ped django.core.urlresolvers

    # Classes and functions work, too
    $ ped django.views.generic.TemplateView

    # Partial name matching
    $ ped django.http.resp
    Editing django.http.response...
    ...Done.

    # Specify which editor to use
    $ PED_EDITOR=vim ped django.shortcuts


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

1.2.0
-----

- Add partial name matching.

1.1.0
-----

- Add support for editing functions and classes.

1.0.2
-----

- Fix for editing subpackages, e.g. ``ped pkg.subpkg``.
