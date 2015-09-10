===
ped
===

.. image:: https://img.shields.io/pypi/v/ped.svg
    :target: https://pypi.python.org/pypi/ped
    :alt: Latest version

.. image:: https://img.shields.io/travis/sloria/ped.svg
    :target: https://travis-ci.org/sloria/ped
    :alt: Travis-CI

Quickly open Python modules in your text editor.

.. code-block:: bash

    $ ped django
    $ ped django.core.urlresolvers
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

``ped`` will try to use your favorite text editor. If you want to override the editor ``ped`` uses, set the ``PED_EDITOR`` environment variable.

.. code-block:: bash

    # .zshrc or .bashrc
    # Use Sublime Text with ped
    export PED_EDITOR=subl

Tab-completion
**************

The ped package contains tab-completion scripts for bash and zsh. Place these files in your system's completion directories. The ``ped.install_completion`` module can be run as a script to copy the files.

- `bash completion <https://github.com/sloria/ped/blob/master/ped/ped_bash_completion.sh>`_
- `zsh completion <https://github.com/sloria/ped/blob/master/ped/ped_zsh_completion.zsh>`_

Bash completion
---------------

To install bash completion, run::

    # The path given here will depend on your OS
    $ python -m ped.install_completion --bash /usr/local/etc/bash_completion.d

Zsh completion
---------------

To install zsh completion, run::

    # The path given here will depend on your OS
    $ python -m ped.install_completion --zsh /usr/local/share/zsh/site-functions

Editor integrations
*******************

- `vim-ped <https://github.com/sloria/vim-ped>`_

Kudos
*****

This was inspired by `IPython's <https://ipython.org/>`_ ``%edit`` magic.


Changelog
*********

1.5.0
-----

- Support tab-completion in bash and zsh. Thanks `Thomas Kluyver <https://github.com/takluyver>`_.

1.4.0
-----

- Add ``--info`` argument for outputting name, file path, and line number of modules/functions/classes.
- Fix: Support line numbers in gvim.

1.3.0
-----

- If a class or function is passed, the editor will open up the file at the correct line number (for supported editors).

1.2.1
-----

- Fix for Py2 compatibility.

1.2.0
-----

- Add partial name matching.

1.1.0
-----

- Add support for editing functions and classes.

1.0.2
-----

- Fix for editing subpackages, e.g. ``ped pkg.subpkg``.
