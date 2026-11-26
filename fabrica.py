"""Atajo de la línea de comandos: python fabrica.py build assets/photos_demo salida/"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from spritefactory.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
