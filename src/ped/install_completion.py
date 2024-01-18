"""Script to install bash and zsh completion for ped."""
import os
import sys
from pathlib import Path

from .style import print_error, style

HERE = Path(__file__).parent
SHELL_MAP = {
    "bash": HERE / "ped_bash_completion.sh",
    "zsh": HERE / "ped_zsh_completion.zsh",
}


def main() -> None:
    if "SHELL" not in os.environ or not os.environ.get("SHELL"):
        print_error("Must have $SHELL set.")
        example = style(
            "SHELL=bash python -m scripts.install_completion",
            bold=True,
            file=sys.stderr,
        )
        print(f"Example: {example}", file=sys.stderr)
        sys.exit(1)
    shell_path = Path(os.environ["SHELL"])
    shell = Path(shell_path).stem
    if shell not in SHELL_MAP:
        print_error(
            f'"{shell_path}" not supported. Only bash and zsh are currently supported.'
        )
        sys.exit(1)
    completion_path = SHELL_MAP[shell]
    with completion_path.open("r") as fp:
        print(fp.read(), end="")
    sys.exit(0)


if __name__ == "__main__":
    main()
