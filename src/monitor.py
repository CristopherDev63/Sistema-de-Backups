"""Monitor de logs para auto-commit.

Lee el archivo de log generado por el sistema de backups y cuenta
las entradas de nivel INFO. Útil para determinar si el proceso
fue exitoso y disparar un commit automático.

Ejemplo de uso:
    total = lectura_log(Path("backup.log"))
    print(f"{total} operaciones INFO encontradas")
"""

from pathlib import Path
import logging

logger: logging.Logger = logging.getLogger(__name__)


def lectura_log(ruta: Path) -> int:
    """Lee el archivo de log y cuenta las entradas de nivel INFO.

    Args:
        ruta: Ruta al archivo de log.

    Returns:
        Número de líneas INFO encontradas en el log.

    Raises:
        FileNotFoundError: Si el archivo de log no existe.
    """
    ruta_log: Path = Path(ruta)

    if not ruta_log.exists():
        logger.error(f"El archivo de log '{ruta}' no existe")
        raise FileNotFoundError(f"No se encontró el log en: {ruta}")

    contenido: str = ruta_log.read_text(encoding="UTF-8")
    contador_exitos: int = 0

    for linea in contenido.splitlines():
        if linea.startswith("INFO"):
            contador_exitos += 1

    logger.info(f"Se encontraron {contador_exitos} entradas INFO en el log")
    return contador_exitos
