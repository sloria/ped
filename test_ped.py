# -*- coding: utf-8 -*-
import pytest

import ped

def test_ped_edits_file(mocker):
    mocker.patch('ped.edit_file')
    ped.ped('pytest')
    path = ped.find_file(pytest)
    ped.edit_file.assert_called_once_with(path, editor=None)

def test_ped_edits_file_with_editor(mocker):
    mocker.patch('ped.edit_file')
    ped.ped('pytest', editor='nano')
    path = ped.find_file(pytest)
    ped.edit_file.assert_called_once_with(path, editor='nano')

def test_import_obj():
    import argparse
    import math
    obj = ped.import_object('argparse')
    assert obj is argparse
    cls = ped.import_object('argparse.ArgumentParser')
    assert cls is argparse.ArgumentParser
    func = ped.import_object('math.acos')
    assert func is math.acos
