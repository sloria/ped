# -*- coding: utf-8 -*-
import argparse
import pytest

import ped
from ped.guess_module import guess_module

def test_ped_edits_file(mocker):
    mocker.patch('ped.edit_file')
    ped.ped('pytest')
    path = ped.find_file(pytest)
    ped.edit_file.assert_called_once_with(path, lineno=0, editor=None)

def test_ped_edits_file_with_editor(mocker):
    mocker.patch('ped.edit_file')
    ped.ped('pytest', editor='nano')
    path = ped.find_file(pytest)
    ped.edit_file.assert_called_once_with(path, lineno=0, editor='nano')

def test_import_obj():
    import argparse
    import math
    obj = ped.import_object('argparse')
    assert obj is argparse
    cls = ped.import_object('argparse.ArgumentParser')
    assert cls is argparse.ArgumentParser
    func = ped.import_object('math.acos')
    assert func is math.acos

def test_guess_module():
    assert 'argparse' in guess_module('argpar')
    assert 'argparse.ArgumentParser' in guess_module('argparse.Argu')
    assert guess_module('argparse')[0] == 'argparse'

def test_get_editor_command():
    assert ped.get_editor_command('foo.py', editor='vi') == 'vi "foo.py"'
    assert ped.get_editor_command('foo.py', lineno=2, editor='vi') == 'vi +2 "foo.py"'
    assert ped.get_editor_command('foo.py', lineno=2, editor='gvim') == 'gvim +2 "foo.py"'
    assert ped.get_editor_command('foo.py', lineno=2, editor='kate') == 'kate "foo.py"'
    assert ped.get_editor_command(
        'foo.py', lineno=2, editor='emacs') == 'emacs +2 "foo.py"'

def test_get_info():
    name, fpath, lineno = ped.get_info('argparse.ArgumentPars')
    assert name == 'argparse.ArgumentParser'
    assert fpath == ped.find_file(argparse.ArgumentParser)
    assert lineno == ped.find_source_lines(argparse.ArgumentParser)
