# -*- coding: utf-8 -*-
import re
from setuptools import setup


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version('ped/__init__.py')


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='ped',
    packages=['ped'],
    version=__version__,
    description='Quickly open Python modules in your text editor.',
    long_description=read('README.rst'),
    author='Steven Loria',
    author_email='sloria1@gmail.com',
    url='https://github.com/sloria/ped',
    install_requires=[],
    license=read("LICENSE"),
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: System :: Shells',
    ],
    entry_points={
        'console_scripts': [
            "ped = ped:main"
        ]
    },
    package_data={
        'ped': [
            "ped_bash_completion.sh",
        ]
    },
)
