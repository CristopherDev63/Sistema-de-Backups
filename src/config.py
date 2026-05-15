"""Modelos Pydantic y carga de configuración.

Define el esquema de configuración usando Pydantic para validación
de tipos y valores del archivo `config.json`.

Typical usage example:
    config = cargando_configuracion(Path("config.json"))
    print(config.rutas.origen)
"""

from pathlib import Path
from typing import Dict, List, Optional, Union
import json
import logging

from pydantic import BaseModel, Field, field_validator

from src.exceptions import RutaInvalidaError

logger: logging.Logger = logging.getLogger(__name__)


class RespaldoConfig(BaseModel):
    """Metadatos del respaldo.

    Attributes:
        nombre: Nombre identificador del backup.
        descripcion: Descripción opcional del backup.
    """

    nombre: str = Field(..., min_length=1, description="Nombre del backup")
    descripcion: str = Field(default="", description="Descripción del backup")


class RutasConfig(BaseModel):
    """Rutas de origen y destino.

    Attributes:
        origen: Directorio a respaldar.
        destino: Directorio donde se guardará el backup.
    """

    origen: str = Field(..., description="Directorio a respaldar")
    destino: str = Field(..., description="Directorio de destino del backup")

    @field_validator("origen", "destino")
    @classmethod
    def verificar_ruta_existe(cls, v: str) -> str:
        """Valida que la ruta exista en el sistema.

        Args:
            v: Ruta a validar.

        Returns:
            La misma ruta si es válida.

        Raises:
            RutaInvalidaError: Si la ruta no existe.
        """
        ruta: Path = Path(v)
        if not ruta.exists():
            raise RutaInvalidaError(ruta)
        return v


class FiltrosConfig(BaseModel):
    """Filtros para incluir/excluir archivos y carpetas.

    Attributes:
        ignorar_extensiones: Extensiones de archivo a excluir (ej. .tmp).
        ignorar_carpetas: Nombres de carpeta a excluir (ej. node_modules).
        ignorar_archivos: Nombres de archivo exactos a excluir (ej. .DS_Store).
    """

    ignorar_extensiones: List[str] = Field(
        default_factory=list,
        description="Extensiones de archivo a ignorar (ej. .tmp, .log)",
    )
    ignorar_carpetas: List[str] = Field(
        default_factory=list,
        description="Nombres de carpeta a ignorar (ej. node_modules, .git)",
    )
    ignorar_archivos: List[str] = Field(
        default_factory=list,
        description="Archivos exactos a ignorar (ej. .DS_Store)",
    )


class CompresionConfig(BaseModel):
    """Configuración de compresión del backup.

    Attributes:
        tipo: Formato de compresión (zip, tar, gztar, bztar, xztar).
        incluir_fecha: Si se agrega la fecha al nombre del archivo.
        formato_fecha: Formato datetime para la fecha en el nombre.
    """

    tipo: str = Field(
        default="zip",
        pattern=r"^(zip|tar|gztar|bztar|xztar)$",
        description="Formato de compresión",
    )
    incluir_fecha: bool = Field(
        default=True, description="Agregar fecha al nombre del archivo"
    )
    formato_fecha: str = Field(
        default="%Y-%m-%d_%H:%M",
        description="Formato de fecha para el nombre",
    )


class RetencionConfig(BaseModel):
    """Política de retención de backups antiguos.

    Attributes:
        max_backups: Número máximo de backups a conservar.
        dias_maximos: Días máximos antes de eliminar un backup.
    """

    max_backups: int = Field(
        default=5, ge=1, description="Máximo de backups a conservar"
    )
    dias_maximos: int = Field(
        default=30, ge=1, description="Días máximos de retención"
    )


class LoggingConfig(BaseModel):
    """Configuración del sistema de logging.

    Attributes:
        nivel: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        archivo: Ruta del archivo de log.
    """

    nivel: str = Field(
        default="DEBUG",
        pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="Nivel de logging",
    )
    archivo: str = Field(
        default="backup.log", min_length=1, description="Archivo de log"
    )


class ModoPruebaConfig(BaseModel):
    """Configuración del modo de prueba.

    Attributes:
        activado: Indica si el modo prueba está activo.
        ruta_origen: Ruta de origen para las pruebas.
        ruta_destino: Ruta de destino para las pruebas.
    """

    activado: bool = Field(
        default=False, description="Activar modo de prueba"
    )
    ruta_origen: Optional[str] = Field(
        default=None, description="Ruta de origen en modo prueba"
    )
    ruta_destino: Optional[str] = Field(
        default=None, description="Ruta de destino en modo prueba"
    )

    @field_validator("ruta_origen", "ruta_destino")
    @classmethod
    def verificar_ruta_si_existe(cls, v: Optional[str]) -> Optional[str]:
        """Valida la ruta si fue proporcionada.

        Args:
            v: Ruta a validar o None.

        Returns:
            La misma ruta o None.

        Raises:
            RutaInvalidaError: Si la ruta fue dada pero no existe.
        """
        if v is not None:
            ruta: Path = Path(v)
            if not ruta.exists():
                raise RutaInvalidaError(ruta)
        return v


class ConfigSchema(BaseModel):
    """Esquema raíz de configuración del sistema de backups.

    Attributes:
        respaldo: Metadatos del respaldo.
        rutas: Rutas de origen y destino.
        filtros: Filtros de exclusión.
        compresion: Configuración de compresión.
        retencion: Política de retención.
        logging: Configuración de logging.
        modo_prueba: Modo de prueba.
    """

    respaldo: RespaldoConfig
    rutas: RutasConfig
    filtros: FiltrosConfig
    compresion: CompresionConfig
    retencion: RetencionConfig
    logging: LoggingConfig
    modo_prueba: ModoPruebaConfig


def cargando_configuracion(archivo: Path) -> ConfigSchema:
    """Carga y valida la configuración desde un archivo JSON.

    Utiliza Pydantic para validar la estructura y los tipos de datos
    del archivo de configuración.

    Args:
        archivo: Ruta al archivo JSON de configuración.

    Returns:
        Instancia de ConfigSchema con los datos validados.

    Raises:
        FileNotFoundError: Si el archivo de configuración no existe.
        json.JSONDecodeError: Si el archivo JSON tiene un formato inválido.
    """
    logger.debug("Ejecución de la función `cargando_configuracion`")

    try:
        contenido: str = archivo.read_text(encoding="UTF-8")
        data_dict: Dict = json.loads(contenido)
        config: ConfigSchema = ConfigSchema(**data_dict)
        logger.info("Configuración JSON cargada y validada correctamente")
        return config

    except FileNotFoundError:
        logger.error("No se encontró el archivo de configuración")
        raise

    except json.JSONDecodeError as e:
        logger.critical(f"Error de sintaxis en el JSON: {e}")
        raise
