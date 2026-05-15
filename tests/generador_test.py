"""Generación de archivos de prueba para el sistema de backups.

Crea una estructura de directorios y archivos simulando un entorno
real con archivos importantes, basura y carpetas ignorables.

Typical usage example:
    generar_archivos_test(Path("./tests/carpeta_origen"))
"""

from pathlib import Path
from typing import List, Tuple


ARCHIVOS_IMPORTANTES: List[Tuple[str, str]] = [
    ("proyecto_final.pdf", "Contenido importante del proyecto."),
    ("notas_reunion.txt", "Lista de tareas pendientes."),
    ("codigo_fuente.py", "print('Hola Mundo')"),
]

ARCHIVOS_BASURA: List[Tuple[str, str]] = [
    ("temp_cache_001.tmp", "Basura temporal."),
    ("error_log_abril.log", "2026-04-23 ERROR: Fallo crítico simulado."),
    ("debug.log", "Datos innecesarios."),
]

CARPETAS_IGNORADAS: List[str] = ["node_modules", ".git"]


def generar_archivos_test(ruta_destino: Path) -> None:
    """Genera una estructura de prueba en la ruta indicada.

    Crea archivos importantes, archivos basura y carpetas que
    deberían ser ignoradas durante el backup.

    Args:
        ruta_destino: Directorio donde se creará la estructura.
    """
    base_path: Path = Path(ruta_destino)

    # 1. Crear la carpeta principal
    base_path.mkdir(parents=True, exist_ok=True)

    # 2. Archivos importantes
    for nombre, contenido in ARCHIVOS_IMPORTANTES:
        ruta: Path = base_path / nombre
        ruta.write_text(contenido)

    # 3. Archivos basura
    for nombre, contenido in ARCHIVOS_BASURA:
        ruta = base_path / nombre
        ruta.write_text(contenido)

    # 4. Carpetas ignoradas con archivos dentro
    for carpeta in CARPETAS_IGNORADAS:
        ruta_carpeta: Path = base_path / carpeta
        ruta_carpeta.mkdir(parents=True, exist_ok=True)
        ruta_archivo: Path = ruta_carpeta / "dummy.file"
        ruta_archivo.write_text("Este archivo no debería estar en el backup")
