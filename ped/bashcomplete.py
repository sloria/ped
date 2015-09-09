from __future__ import print_function

import os
import shutil

def install():
    # Is this right for all systems?
    destination = '/etc/bash_completion.d/'
    source = os.path.join(os.path.dirname(__file__), 'ped_bash_completion.sh')
    print('Copying', source, 'to', destination)
    shutil.copy(source, destination)

if __name__ == '__main__':
    install()
