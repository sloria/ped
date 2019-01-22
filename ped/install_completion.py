"""Script to install bash and zsh completion for ped."""
from __future__ import print_function

import argparse
import os
import shutil
import sys

from .style import print_error

HERE = os.path.dirname(os.path.abspath(__file__))
BASH = os.path.join(HERE, "ped_bash_completion.sh")
ZSH = os.path.join(HERE, "ped_zsh_completion.zsh")


def main(zsh=None, bash=None):
    if not (zsh or bash):
        print_error("Must provide --bash and/or --zsh")
        sys.exit(1)
    if bash:
        install_bash_completion(bash)
    if zsh:
        install_zsh_completion(zsh)
    print("...Done.")


def install_bash_completion(destination):
    print("Copying {BASH} to {destination}")
    shutil.copy(BASH, destination)


def install_zsh_completion(destination):
    if not os.path.isdir(destination):
        print_error(f"{destination} is not a directory")
        sys.exit(1)
    print(f"Copying {ZSH} to {destination}")
    shutil.copy(ZSH, os.path.join(destination, "_ped"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-b", "--bash", type=str, dest="bash", help="path to install bash completion"
    )
    parser.add_argument(
        "-z", "--zsh", type=str, dest="zsh", help="path to install zsh completion"
    )
    args = parser.parse_args()
    main(zsh=args.zsh, bash=args.bash)
