"""Configuración del sistema de logging.

Centraliza la configuración del logging para que todos los módulos
compartan el mismo formato, nivel y manejadores (archivo + consola).

El nivel de logging se puede pasar como entero (`logging.DEBUG`) o
como cadena (`"DEBUG"`, `"INFO"`, `"WARNING"`, etc.).

Ejemplo de uso:
    from src.log_setup import configurar_logging
    configurar_logging(nivel="DEBUG", ruta_log="backup.log")
"""

import logging
from typing import Union


NIVELES: dict[str, int] = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def _resolver_nivel(nivel: Union[int, str]) -> int:
    """Convierte un nivel de logging desde cadena o entero.

    Args:
        nivel: Puede ser un entero (`logging.DEBUG`) o un
               string (`"DEBUG"`, `"INFO"`, etc.).

    Returns:
        Entero correspondiente al nivel de logging.

    Raises:
        ValueError: Si el string no corresponde a un nivel válido.
    """
    if isinstance(nivel, int):
        return nivel
    nivel_str: str = nivel.upper()
    if nivel_str not in NIVELES:
        valores: str = ", ".join(NIVELES)
        raise ValueError(f"Nivel de logging inválido: '{nivel}'. Usa: {valores}")
    return NIVELES[nivel_str]


def configurar_logging(
    nivel: Union[int, str] = logging.DEBUG,
    ruta_log: str = "backup.log",
) -> None:
    """Configura el logging global de la aplicación.

    Args:
        nivel: Nivel de logging como entero o string.
               Por defecto `logging.DEBUG`.
        ruta_log: Ruta del archivo de log. Por defecto `"backup.log"`.
    """
    nivel_resuelto: int = _resolver_nivel(nivel)

    logging.basicConfig(
        level=nivel_resuelto,
        format="%(levelname)s | %(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M",
        handlers=[
            logging.FileHandler(ruta_log),
            logging.StreamHandler(),
        ],
    )
