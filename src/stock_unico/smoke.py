"""Minimal smoke check for Sprint 0."""

from stock_unico import __version__


def health() -> dict[str, str]:
    return {"status": "ok", "service": "stock-unico", "version": __version__}


if __name__ == "__main__":
    print(health())
