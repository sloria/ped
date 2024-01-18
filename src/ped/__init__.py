#!/usr/bin/env python
"""Open Python modules in your text editor.

Example: ped django.core.urlresolvers
"""
import argparse
import importlib
import importlib.metadata
import inspect
import os
import shlex
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Optional, Tuple

from .guess_module import get_names_by_prefix, guess_module
from .pypath import patch_sys_path
from .style import GREEN, print_error, sprint, style


def main() -> None:
    args = parse_args()
    if args.complete:
        complete(args.module)
    else:
        # Allow ped to be run in its own virtual environment
        # by pre-pending sys.path with the current virtual
        # environment's sys.path
        patch_sys_path()
        try:
            ped(module=args.module, editor=args.editor, info=args.info)
        except ImportError:
            print_error(
                f'Could not find module in current environment: "{args.module}"'
            )
            sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("module", help="import path to module, function, or class")
    parser.add_argument(
        "-e", "--editor", type=str, dest="editor", help="editor program"
    )
    parser.add_argument(
        "-v", "--version", action="version", version=importlib.metadata.version("ped")
    )
    parser.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="output name, file path, and line number (if applicable) of module",
    )
    parser.add_argument("--complete", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args()


def ped(module: str, editor: Optional[str] = None, info: bool = False) -> None:
    module_name, fpath, lineno = get_info(module)
    if info:
        out = f"{module_name} {fpath}"
        if lineno is not None:
            out += f" {lineno:d}"
        print(out)
    else:
        print(f"Editing {style(module_name, bold=True)}...")
        edit_file(fpath, lineno=lineno, editor=editor)
        sprint("Done!", fg=GREEN)


def complete(ipath: str) -> None:
    """Print possible module completions to stdout.

    :param str ipath: Partial import path to a module, function, or class.
    """
    for name in get_names_by_prefix(ipath):
        print(name)


def get_info(ipath: str) -> Tuple[str, str, Optional[int]]:
    """Return module name, file path, and line number.

    :param str ipath: Import path to module, function, or class. May be a partial name,
        in which case we guess the import path.
    """
    module_name = ipath
    try:
        obj = import_object(module_name)
    except ImportError as error:
        guessed = guess_module(ipath)
        if guessed:
            module_name = guessed[0]
            obj = import_object(module_name)
        else:
            raise ImportError(
                f'Cannot find any module that matches "{ipath}"'
            ) from error
    fpath = find_file(obj)
    if not fpath:
        raise ImportError(f'Cannot find any module that matches "{ipath}"')
    lineno = find_source_lines(obj)
    return module_name, fpath, lineno


def import_object(ipath: str) -> ModuleType:
    try:
        return importlib.import_module(ipath)
    except ImportError as err:
        if "." not in ipath:
            raise err
        module_name, symbol_name = ipath.rsplit(".", 1)
        mod = importlib.import_module(module_name)
        try:
            return getattr(mod, symbol_name)
        except AttributeError as error:
            raise ImportError(
                f'Cannot import "{symbol_name}" from "{module_name}"'
            ) from error
        raise err


# Adapted from IPython.core.oinspect.find_file
def _get_wrapped(obj: Any) -> Any:
    """Get the original object if wrapped in one or more @decorators"""
    while safe_hasattr(obj, "__wrapped__"):
        obj = obj.__wrapped__
    return obj


def find_file(obj: Any) -> Optional[str]:
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

    if fname and os.environ.get("PED_OPEN_DIRECTORIES"):
        fname_path = Path(fname)
        if fname_path.name == "__init__.py":
            # open the directory instead of the __init__.py file.
            fname = str(fname_path.parent)

    return fname


# Adapted from IPython.core.oinspect.find_source_lines
def find_source_lines(obj: Any) -> Optional[int]:
    """Find the line number in a file where an object was defined.

    This is essentially a robust wrapper around `inspect.getsourcelines`.

    Returns None if no file can be found.
    """
    obj = _get_wrapped(obj)

    lineno: Optional[int]
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


def safe_hasattr(obj: Any, attr: str) -> bool:
    """In recent versions of Python, hasattr() only catches AttributeError.
    This catches all errors.
    """
    try:
        getattr(obj, attr)
        return True
    except Exception:
        return False


# Adapted from click._termui_impl
def get_editor() -> str:
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


def get_editor_command(
    filename: str, lineno: Optional[int] = None, editor: Optional[str] = None
) -> str:
    editor = editor or get_editor()
    # Enclose in quotes if necessary and legal
    if " " in editor and os.path.isfile(editor) and editor[0] != '"':
        editor = f'"{editor}"'
    if lineno and shlex.split(editor)[0] in SUPPORTS_LINENO:
        command = f'{editor} +{lineno:d} "{filename}"'
    else:
        command = f'{editor} "{filename}"'
    return command


def edit_file(
    filename: str, lineno: Optional[int] = None, editor: Optional[str] = None
) -> None:
    command = get_editor_command(filename, lineno=lineno, editor=editor)
    try:
        result = subprocess.Popen(command, shell=True)
        exit_code = result.wait()
        if exit_code != 0:
            print_error("Editing failed!")
            sys.exit(1)
    except OSError as err:
        print_error(f"Editing failed: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
