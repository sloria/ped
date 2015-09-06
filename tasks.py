# -*- coding: utf-8 -*-
import os
import webbrowser

from invoke import task, run

@task
def test():
    run('py.test test_ped.py')

@task
def clean():
    run("rm -rf build")
    run("rm -rf dist")
    run("rm -rf ped.egg-info")
    clean_docs()
    print("Cleaned up.")

@task
def readme(browse=False):
    run("rst2html.py README.rst > README.html")
    if browse:
        webbrowser.open_new_tab('README.html')

@task
def publish(test=False):
    """Publish to the cheeseshop."""
    if test:
        run('python setup.py register -r test sdist upload -r test')
    else:
        run("python setup.py register sdist upload")
