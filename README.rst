===
ped
===

.. image:: https://badgen.net/pypi/v/ped
  :alt: pypi badge
  :target: https://pypi.org/project/ped/

.. image:: https://github.com/sloria/ped/actions/workflows/build-release.yml/badge.svg
    :alt: build status
    :target: https://github.com/sloria/ped/actions/workflows/build-release.yml

.. image:: https://badgen.net/badge/code%20style/black/000
   :target: https://github.com/ambv/black
   :alt: Code style: Black

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

From PyPI:

::

    $ pip install ped


Or, run it with `pipx <https://github.com/pipxproject/pipx>`_:

::

    $ pipx run ped --help


Changing the default editor
***************************

``ped`` will try to use your favorite text editor. If you want to override the editor ``ped`` uses, set the ``PED_EDITOR`` environment variable.

.. code-block:: bash

    # .zshrc or .bashrc
    # Use vim with ped
    export PED_EDITOR=vim


Opening directories
*******************

By default, ``ped`` will open ``__init__.py`` files when a package name is passed.
If you would rather open the package's directory, set the ``PED_OPEN_DIRECTORIES`` environment variable.

.. code-block:: bash

    # .zshrc or .bashrc
    # Open package directories instead of __init__.py
    export PED_OPEN_DIRECTORIES=1


Tab-completion
**************

The ped package contains tab-completion scripts for bash and zsh. Place these files in your system's completion directories. The ``ped.install_completion`` module can be run as a script to output the files to a given location. It determines the correct completion file from
the ``$SHELL`` environment variable.

Bash completion
---------------

To install bash completion, run::

    # The path given here will depend on your OS
    $ python -m ped.install_completion > /usr/local/etc/bash_completion.d

Zsh completion
---------------

To install zsh completion, run::

    # The path given here will depend on your OS
    $ python -m ped.install_completion > /usr/local/share/zsh/site-functions

Editor integrations
*******************

- `vim-ped <https://github.com/sloria/vim-ped>`_

Kudos
*****

This was inspired by `IPython's <https://ipython.org/>`_ ``%edit`` magic.


Changelog
*********

3.0.0 (2024-01-18)
------------------

- Publish type information.
- Test against Python 3.8-3.12. Older versions of Python are no longer supported.
- *Backwards-incompatible*: Remove ``ped.__version__`` attribute.
  Use ``importlib.metadata.version("ped")`` instead.

2.1.0 (2020-03-18)
------------------

- Set ``PED_OPEN_DIRECTORIES=1`` to open package directories instead of
  opening ``__init__.py`` files. Thanks `Alex Nordin <https://github.com/anordin95>`_.

2.0.1 (2018-01-27)
------------------

Bug fixes:

- Properly handle imports that don't correspond to a file.

2.0.0 (2019-01-22)
------------------

- Drop support for Python 2.7 and 3.5. Only Python>=3.6 is supported.
- ``ped`` can be run its own virtual environment separate from the
  user's virtual environment. Therefore, ped can be installed with
  pipsi or pipx.
- ``install_completion`` script writes to ``stdout`` and detemrmines
  script from ``$SHELL``.

1.6.0 (2019-01-14)
------------------

- Test against Python 3.7.

Note: This is the last version to support Python 2.

1.5.1
-----

- Minor code cleanups.
- Test against Python 2.7, 3.5, and 3.6. Support for older versions is dropped.

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
