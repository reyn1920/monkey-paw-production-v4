"""Allow safety to be executable through `python -m safety`."""

from .cli import cli


if __name__ == "__main__":  # pragma: no cover
    cli(prog_name="safety")