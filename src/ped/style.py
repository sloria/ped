import os
import sys
from typing import IO, Any, Optional

RED = 31
GREEN = 32
BOLD = 1
RESET_ALL = 0


def style(
    text: str, fg: Optional[int] = None, *, bold: bool = False, file: IO = sys.stdout
) -> str:
    use_color = not os.environ.get("NO_COLOR") and file.isatty()
    if use_color:
        parts = [
            fg and f"\033[{fg}m",
            bold and f"\033[{BOLD}m",
            text,
            f"\033[{RESET_ALL}m",
        ]
        return "".join([e for e in parts if e])
    else:
        return text


def sprint(text: str, *args: Any, **kwargs: Any) -> None:
    file = kwargs.pop("file", sys.stdout)
    return print(style(text, *args, **kwargs, file=file), file=file)


def print_error(text: str) -> None:
    prefix = style("ERROR", RED, file=sys.stderr)
    return sprint(f"{prefix}: {text}", file=sys.stderr)
