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
import subprocess
import sys

from .guess_module import guess_module

__version__ = '1.2.0'

def main():
    args = parse_args()
    try:
        ped(module=args.module, editor=args.editor)
    except ImportError:
        print('ERROR: Could not find module in '
              'current environment: "{0}"'.format(args.module))
        sys.exit(1)
    print('...Done.')

def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('module', help='Python module to edit')
    parser.add_argument('-e', '--editor', type=str, dest='editor', help='editor program')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    return parser.parse_args()

def ped(module, editor=None):
    module_name = module
    try:
        obj = import_object(module_name)
    except ImportError:
        guessed = guess_module(module)
        if guessed:
            module_name = guessed[0]
            obj = import_object(module_name)
        else:
            raise ImportError('Cannot find any module that matches "{0}"'.format(module))
    print('Editing {0}...'.format(module_name))
    fpath = find_file(obj)
    edit_file(fpath, editor=editor)


def import_object(ipath):
    try:
        return importlib.import_module(ipath)
    except ImportError as err:
        if '.' not in ipath:
            raise err
        module_name, symbol_name = ipath.rsplit('.', 1)
        mod = importlib.import_module(module_name)
        try:
            return getattr(mod, symbol_name)
        except AttributeError:
            raise ImportError(
                'Cannot import "{0}" from "{1}"'.format(symbol_name, module_name)
            )
        raise err

# Adapted from IPython.core.oinspect.find_file
def find_file(obj):
    """Find the absolute path to the file where an object was defined.

    This is essentially a robust wrapper around `inspect.getabsfile`.
    """
    # get source if obj was decorated with @decorator
    if safe_hasattr(obj, '__wrapped__'):
        obj = obj.__wrapped__

    fname = None
    try:
        fname = inspect.getabsfile(obj)
    except TypeError:
        # For an instance, the file that matters is where its class was
        # declared.
        if hasattr(obj, '__class__'):
            try:
                fname = inspect.getabsfile(obj.__class__)
            except TypeError:
                # Can happen for builtins
                pass
    except:
        pass
    return fname

def safe_hasattr(obj, attr):
    """In recent versions of Python, hasattr() only catches AttributeError.
    This catches all errors.
    """
    try:
        getattr(obj, attr)
        return True
    except:
        return False

# Adapted from click
def get_editor():
    for key in ('PED_EDITOR', 'VISUAL', 'EDITOR'):
        ret = os.environ.get(key)
        if ret:
            return ret
    if sys.platform.startswith('win'):
        return 'notepad'
    for editor in 'vim', 'nano':
        if os.system('which %s &> /dev/null' % editor) == 0:
            return editor
    return 'vi'

def edit_file(filename, editor=None):
    editor = editor or get_editor()
    try:
        result = subprocess.Popen('{0} "{1}"'.format(editor, filename), shell=True)
        exit_code = result.wait()
        if exit_code != 0:
            print('{0}: Editing failed!'.format(editor), file=sys.stderr)
            sys.exit(1)
    except OSError as err:
        print('{0}: Editing failed: {1}'.format(editor, err), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
