# -*- coding: utf-8 -*-
"""Helpers for finding possible module matches, given a substring.

Much of this code is adapted from IPython.core.completerlib
(see NOTICE for license information).
"""
import difflib
import inspect
import os
import re
import sys
import time
import zipimport

try:
    # Python >= 3.3
    from importlib.machinery import all_suffixes

    _suffixes = all_suffixes()
except ImportError:
    from imp import get_suffixes

    _suffixes = [s[0] for s in get_suffixes()]

# Regular expression for the python import statement
import_re = re.compile(
    r"(?P<name>[a-zA-Z_][a-zA-Z0-9_]*?)"
    r"(?P<package>[/\\]__init__)?"
    r"(?P<suffix>%s)$" % r"|".join(re.escape(s) for s in _suffixes)
)


# Time in seconds after which we give up
TIMEOUT_GIVEUP = 20


def guess_module(name, **kwargs):
    """Given a string, return a list of probably module paths.

    Example: ::

        guess_module('argparse.Argument')
        # ['argparse.ArgumentError',
        # 'argparse.ArgumentParser',
        # 'argparse.ArgumentTypeError']
    """
    possible = get_possible_modules(name)
    return difflib.get_close_matches(name, possible, **kwargs)


def get_possible_modules(name):
    mod = name.split(".")
    if len(mod) < 2:
        return get_root_modules()
    completion_list = try_import(".".join(mod[:-1]), True)
    return [".".join(mod[:-1] + [el]) for el in completion_list]


def get_names_by_prefix(prefix):
    for name in get_possible_modules(prefix):
        if name.startswith(prefix):
            yield name


def get_root_modules():
    """Return a list containing the names of all the modules available in the
    folders of the pythonpath.
    """
    rootmodules = list(sys.builtin_module_names)
    start_time = time.time()
    for path in sys.path:
        modules = module_list(path)
        try:
            modules.remove("__init__")
        except ValueError:
            pass
        if time.time() - start_time > TIMEOUT_GIVEUP:
            print("This is taking too long, we give up.\n")
            return []
        rootmodules.extend(modules)
    rootmodules = list(set(rootmodules))
    return rootmodules


def module_list(path):
    """
    Return the list containing the names of the modules available in the given
    folder.
    """
    # sys.path has the cwd as an empty string, but isdir/listdir need it as '.'
    if path == "":
        path = "."

    # A few local constants to be used in loops below
    pjoin = os.path.join

    if os.path.isdir(path):
        # Build a list of all files in the directory and all files
        # in its subdirectories. For performance reasons, do not
        # recurse more than one level into subdirectories.
        files = []
        for root, dirs, nondirs in os.walk(path, followlinks=True):
            subdir = root[len(path) + 1 :]
            if subdir:
                files.extend(pjoin(subdir, f) for f in nondirs)
                dirs[:] = []  # Do not recurse into additional subdirectories.
            else:
                files.extend(nondirs)

    else:
        try:
            files = list(zipimport.zipimporter(path)._files.keys())
        except Exception:
            files = []

    # Build a list of modules which match the import_re regex.
    modules = []
    for f in files:
        m = import_re.match(f)
        if m:
            modules.append(m.group("name"))
    return list(set(modules))


def try_import(mod, only_modules=False):
    try:
        m = __import__(mod)
    except Exception:
        return []
    mods = mod.split(".")
    for module in mods[1:]:
        m = getattr(m, module)

    m_is_init = hasattr(m, "__file__") and "__init__" in m.__file__

    completions = []
    if (not hasattr(m, "__file__")) or (not only_modules) or m_is_init:
        completions.extend(
            [attr for attr in dir(m) if is_importable(m, attr, only_modules)]
        )

    completions.extend(getattr(m, "__all__", []))
    if m_is_init:
        completions.extend(module_list(os.path.dirname(m.__file__)))
    completions = set(completions)
    if "__init__" in completions:
        completions.remove("__init__")
    return list(completions)


def is_importable(module, attr, only_modules):
    if only_modules:
        return inspect.ismodule(getattr(module, attr))
    else:
        return not (attr[:2] == "__" and attr[-2:] == "__")
