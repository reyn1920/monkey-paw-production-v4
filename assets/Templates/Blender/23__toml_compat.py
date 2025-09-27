try:
    import tomllib
except ImportError:
    try:
        # type: ignore[no-redef, unused-ignore]
        from pip._vendor import tomli as tomllib
    except ModuleNotFoundError:  # pragma: no cover
        tomllib = None  # type: ignore[assignment, unused-ignore]

__all__ = ("tomllib",)
