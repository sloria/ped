# -*- coding: utf-8 -*-
import re
from setuptools import setup

EXTRAS_REQUIRE = {
    "tests": ["pytest", "mock", "pytest-mock", "scripttest==1.3"],
    "lint": [
        "flake8==3.6.0",
        'flake8-bugbear==18.8.0; python_version >= "3.5"',
        "pre-commit==1.14.2",
    ],
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["lint"] + ["tox"]
PYTHON_REQUIRES = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*"


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ""
    with open(fname, "r") as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError("Cannot find version information")
    return version


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name="ped",
    packages=["ped"],
    version=find_version("ped/__init__.py"),
    description="Quickly open Python modules in your text editor.",
    long_description=read("README.rst"),
    author="Steven Loria",
    author_email="sloria1@gmail.com",
    url="https://github.com/sloria/ped",
    install_requires=[],
    extras_require=EXTRAS_REQUIRE,
    python_requires=PYTHON_REQUIRES,
    license="MIT",
    zip_safe=False,
    keywords=("commandline", "cli", "open", "editor", "editing"),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: System :: Shells",
    ],
    entry_points={"console_scripts": ["ped = ped:main"]},
    package_data={"ped": ["ped_bash_completion.sh", "ped_zsh_completion.zsh"]},
)
