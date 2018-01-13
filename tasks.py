# -*- coding: utf-8 -*-
import webbrowser
import sys

from invoke import task


@task
def test(ctx):
    import pytest
    retcode = pytest.main(['test_ped.py'])
    sys.exit(retcode)


@task
def clean(ctx):
    ctx.run("rm -rf build")
    ctx.run("rm -rf dist")
    ctx.run("rm -rf ped.egg-info")
    print("Cleaned up.")


@task
def readme(ctx, browse=False):
    ctx.run("rst2html.py README.rst > README.html")
    if browse:
        webbrowser.open_new_tab('README.html')


@task
def publish(ctx, test=False):
    """Publish to the cheeseshop."""
    if test:
        ctx.run('python setup.py register -r test sdist upload -r test')
    else:
        ctx.run("python setup.py register sdist upload")
