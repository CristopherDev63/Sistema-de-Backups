"""Excepciones personalizadas del sistema de backups.

Define todas las excepciones que puede lanzar la aplicación,
organizadas por dominio: rutas inválidas, configuración vacía
y errores durante la ejecución del backup.

Ejemplo de uso:
    raise RutaInvalidaError(Path("/ruta/que/no/existe"))
"""

from pathlib import Path
from typing import Optional
import logging

logger: logging.Logger = logging.getLogger(__name__)


class RutaInvalidaError(Exception):
    """Excepción lanzada cuando una ruta no existe o es inválida.

    Attributes:
        ruta: La ruta que causó el error.
        mensaje: Descripción del error.
    """

    def __init__(self, ruta: Path) -> None:
        """Inicializa la excepción con la ruta problemática.

        Args:
            ruta: Objeto Path que no es válido.
        """
        self.ruta: Path = ruta
        self.mensaje: str = f"La ruta '{ruta}' no existe o no es válida."
        logger.critical(self.mensaje)
        super().__init__(self.mensaje)


class ConfiguracionVaciaError(Exception):
    """Excepción lanzada cuando la configuración cargada está vacía.

    Attributes:
        mensaje: Descripción del error.
    """

    def __init__(self) -> None:
        """Inicializa la excepción con un mensaje por defecto."""
        self.mensaje: str = (
            "No se encontró ninguna configuración válida en `config.json`."
        )
        logger.error(self.mensaje)
        super().__init__(self.mensaje)


class BackupError(Exception):
    """Excepción lanzada durante el proceso de creación del backup.

    Attributes:
        mensaje: Descripción del error.
        causa: Excepción original que originó el error (opcional).
    """

    def __init__(self, mensaje: str, causa: Optional[Exception] = None) -> None:
        """Inicializa la excepción con un mensaje y una causa opcional.

        Args:
            mensaje: Descripción del error ocurrido.
            causa: Excepción original que se encadenó (por defecto None).
        """
        self.mensaje: str = mensaje
        self.causa: Optional[Exception] = causa
        logger.error(f"BackupError: {mensaje}")
        super().__init__(mensaje)
