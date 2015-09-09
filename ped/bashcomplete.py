from __future__ import print_function

import argparse
import os
import shutil

def install(destination):
    # Is this right for all systems?
    destination = '/etc/bash_completion.d/'
    source = os.path.join(os.path.dirname(__file__), 'ped_bash_completion.sh')
    print('Copying', source, 'to', destination)
    shutil.copy(source, destination)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('destination',
            help='Directory to which to install completion script')
    args = ap.parse_args()
    install(args.destination)
