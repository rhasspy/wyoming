"""Version number."""
from pathlib import Path

_DIR = Path(__file__).parent
_VERSION_PATH = _DIR / "VERSION"

__version__ = _VERSION_PATH.read_text(encoding="utf-8").strip()

__all__ = ["__version__"]
