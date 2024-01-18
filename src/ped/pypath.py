import shutil
import subprocess
import sys
from typing import List


def patch_sys_path() -> None:
    """Modify sys.path to include all paths from the
    current environment.
    """
    syspath = _get_external_sys_path()
    for each in reversed(syspath):
        if each not in sys.path:
            sys.path.insert(0, each)


def _get_external_sys_path() -> List[str]:
    executable = shutil.which("python") or "python"
    if executable == sys.executable:  # not in virtualenv
        return []
    ret = (
        subprocess.run(
            [executable, "-c", "import sys; print(','.join(sys.path))"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        .stdout.decode()
        .strip()
    )
    return ret.split(",")
