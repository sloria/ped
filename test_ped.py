# -*- coding: utf-8 -*-
import mock
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
