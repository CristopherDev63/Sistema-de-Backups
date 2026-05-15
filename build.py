"""Script de empaquetado para generar un ejecutable del sistema de backups.

Uso:
    python build.py              # genera .exe o ejecutable standalone
    python build.py --onefile    # genera un solo archivo
    python build.py --app        # genera .app para macOS (solo macOS)

Requisitos:
    pip install pyinstaller
"""

import subprocess
import sys
import shutil
from pathlib import Path


def limpiar_cache() -> None:
    """Elimina directorios temporales de PyInstaller."""
    for dirname in ("build", "dist", "__pycache__"):
        ruta = Path(dirname)
        if ruta.exists() and ruta.is_dir():
            shutil.rmtree(ruta)
            print(f"  Eliminado: {dirname}/")
    for pyc in Path(".").rglob("__pycache__"):
        if pyc.is_dir():
            shutil.rmtree(pyc)
            print(f"  Eliminado: {pyc}")


def construir(args: list[str]) -> None:
    """Ejecuta PyInstaller con los argumentos dados."""
    comando = ["pyinstaller", "build.spec"] + args
    print(f"Ejecutando: {' '.join(comando)}")
    print("-" * 50)
    resultado = subprocess.run(comando)
    if resultado.returncode == 0:
        print("-" * 50)
        print("Empaquetado exitoso.")
        dist_dir = Path("dist")
        if dist_dir.exists():
            for item in dist_dir.iterdir():
                print(f"  Generado: {item}")
    else:
        print(f"Error durante el empaquetado (codigo: {resultado.returncode})")
        sys.exit(resultado.returncode)


def main() -> None:
    """Punto de entrada del script de build."""
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    if "--clean" in args:
        print("Limpiando cache...")
        limpiar_cache()
        args.remove("--clean")

    if not args:
        construir(["--onefile"])
    elif "--onefile" in args:
        construir(["--onefile"])
    elif "--app" in args:
        construir(["--windowed", "--onedir"])
    else:
        print(f"Argumento no reconocido: {args}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
