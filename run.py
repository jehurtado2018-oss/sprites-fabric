"""Atajo: python run.py  ->  levanta la aplicación en http://localhost:8000"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from spritefactory.web.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
