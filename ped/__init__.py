#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Open Python modules in your text editor.

Example: ped django.core.urlresolvers
"""
from __future__ import print_function
import argparse
import importlib
import inspect
import os
import shlex
import subprocess
import sys

from .guess_module import guess_module, get_names_by_prefix

__version__ = "1.6.0"


def main():
    args = parse_args()
    if args.complete:
        complete(args.module)
    else:
        try:
            ped(module=args.module, editor=args.editor, info=args.info)
        except ImportError:
            print(
                "ERROR: Could not find module in "
                'current environment: "{}"'.format(args.module),
                file=sys.stderr,
            )
            sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("module", help="import path to module, function, or class")
    parser.add_argument(
        "-e", "--editor", type=str, dest="editor", help="editor program"
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="output name, file path, and line number (if applicable) of module",
    )
    parser.add_argument("--complete", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args()


def ped(module, editor=None, info=False):
    module_name, fpath, lineno = get_info(module)
    if info:
        out = "{} {}".format(module_name, fpath)
        if lineno is not None:
            out += " {:d}".format(lineno)
        print(out)
    else:
        print("Editing {}...".format(module_name))
        edit_file(fpath, lineno=lineno, editor=editor)
        print("...Done.")


def complete(ipath):
    """Print possible module completions to stdout.

    :param str ipath: Partial import path to a module, function, or class.
    """
    for name in get_names_by_prefix(ipath):
        print(name)


def get_info(ipath):
    """Return module name, file path, and line number.

    :param str ipath: Import path to module, function, or class. May be a partial name,
        in which case we guess the import path.
    """
    module_name = ipath
    try:
        obj = import_object(module_name)
    except ImportError:
        guessed = guess_module(ipath)
        if guessed:
            module_name = guessed[0]
            obj = import_object(module_name)
        else:
            raise ImportError('Cannot find any module that matches "{}"'.format(ipath))
    fpath = find_file(obj)
    lineno = find_source_lines(obj)
    return module_name, fpath, lineno


def import_object(ipath):
    try:
        return importlib.import_module(ipath)
    except ImportError as err:
        if "." not in ipath:
            raise err
        module_name, symbol_name = ipath.rsplit(".", 1)
        mod = importlib.import_module(module_name)
        try:
            return getattr(mod, symbol_name)
        except AttributeError:
            raise ImportError(
                'Cannot import "{}" from "{}"'.format(symbol_name, module_name)
            )
        raise err


# Adapted from IPython.core.oinspect.find_file
def _get_wrapped(obj):
    """Get the original object if wrapped in one or more @decorators"""
    while safe_hasattr(obj, "__wrapped__"):
        obj = obj.__wrapped__
    return obj


def find_file(obj):
    """Find the absolute path to the file where an object was defined.

    This is essentially a robust wrapper around `inspect.getabsfile`.
    """
    # get source if obj was decorated with @decorator
    obj = _get_wrapped(obj)

    fname = None
    try:
        fname = inspect.getabsfile(obj)
    except TypeError:
        # For an instance, the file that matters is where its class was
        # declared.
        if hasattr(obj, "__class__"):
            try:
                fname = inspect.getabsfile(obj.__class__)
            except TypeError:
                # Can happen for builtins
                pass
    except Exception:
        pass
    return fname


# Adapted from IPython.core.oinspect.find_source_lines
def find_source_lines(obj):
    """Find the line number in a file where an object was defined.

    This is essentially a robust wrapper around `inspect.getsourcelines`.

    Returns None if no file can be found.
    """
    obj = _get_wrapped(obj)

    try:
        try:
            lineno = inspect.getsourcelines(obj)[1]
        except TypeError:
            # For instances, try the class object like getsource() does
            if hasattr(obj, "__class__"):
                lineno = inspect.getsourcelines(obj.__class__)[1]
            else:
                lineno = None
    except Exception:
        return None

    return lineno


def safe_hasattr(obj, attr):
    """In recent versions of Python, hasattr() only catches AttributeError.
    This catches all errors.
    """
    try:
        getattr(obj, attr)
        return True
    except Exception:
        return False


# Adapted from click._termui_impl
def get_editor():
    for key in ("PED_EDITOR", "VISUAL", "EDITOR"):
        ret = os.environ.get(key)
        if ret:
            return ret
    if sys.platform.startswith("win"):
        return "notepad"
    for editor in "vim", "nano":
        if os.system("which %s &> /dev/null" % editor) == 0:
            return editor
    return "vi"


# Editors that support the +lineno option
SUPPORTS_LINENO = {"vim", "gvim", "vi", "nvim", "mvim", "emacs", "jed", "nano"}


def get_editor_command(filename, lineno=None, editor=None):
    editor = editor or get_editor()
    # Enclose in quotes if necessary and legal
    if " " in editor and os.path.isfile(editor) and editor[0] != '"':
        editor = '"%s"' % editor
    if lineno and shlex.split(editor)[0] in SUPPORTS_LINENO:
        command = '{editor} +{lineno:d} "{filename}"'.format(**locals())
    else:
        command = '{editor} "{filename}"'.format(**locals())
    return command


def edit_file(filename, lineno=None, editor=None):
    command = get_editor_command(filename, lineno=lineno, editor=editor)
    try:
        result = subprocess.Popen(command, shell=True)
        exit_code = result.wait()
        if exit_code != 0:
            print("ERROR: Editing failed!", file=sys.stderr)
            sys.exit(1)
    except OSError as err:
        print("ERROR: Editing failed: {}".format(err), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
