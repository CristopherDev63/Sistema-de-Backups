"""Lógica principal del backup.

Contiene las funciones responsables de copiar archivos aplicando
filtros, crear el archivo ZIP y orquestar el flujo completo.

Typical usage example:
    config = cargando_configuracion(Path("config.json"))
    ejecucion_backup(config)
"""

from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime
import shutil
import logging

from src.config import ConfigSchema
from src.exceptions import ConfiguracionVaciaError, BackupError

logger: logging.Logger = logging.getLogger(__name__)

try:
    from tests import generador_test
except ImportError:
    generador_test = None  # type: ignore[assignment]
    logger.warning("No se pudo importar el módulo de tests")


def _debe_ignorar(
    elemento: Path,
    extensiones: List[str],
    carpetas: List[str],
    archivos: List[str],
) -> bool:
    """Determina si un archivo o carpeta debe ser ignorado.

    Args:
        elemento: Ruta del archivo o carpeta a evaluar.
        extensiones: Lista de extensiones a ignorar.
        carpetas: Lista de nombres de carpeta a ignorar.
        archivos: Lista de nombres de archivo a ignorar.

    Returns:
        True si el elemento debe ignorarse, False en caso contrario.
    """
    if elemento.is_dir() and elemento.name in carpetas:
        return True
    if elemento.is_file():
        if elemento.name in archivos:
            return True
        if elemento.suffix in extensiones:
            return True
    return False


def copiar_archivos_backup(
    ruta_origen: Path,
    ruta_destino: Path,
    nombre_backup: Path,
    extensiones: List[str],
    carpetas: List[str],
    archivos: List[str],
) -> List[Tuple[Path, Path]]:
    """Copia los archivos desde origen a destino aplicando los filtros.

    Itera sobre los elementos del directorio de origen y construye una
    lista de tuplas (origen, destino) excluyendo aquellos que coincidan
    con los filtros de exclusión.

    Args:
        ruta_origen: Directorio desde donde se copiarán los archivos.
        ruta_destino: Directorio raíz de destino.
        nombre_backup: Nombre de la subcarpeta de backup.
        extensiones: Extensiones de archivo a ignorar.
        carpetas: Nombres de carpeta a ignorar.
        archivos: Nombres de archivo exactos a ignorar.

    Returns:
        Lista de tuplas (ruta_origen, ruta_destino) copiadas.

    Raises:
        BackupError: Si ocurre un error durante el proceso de copia.
    """
    lista: List[Tuple[Path, Path]] = []
    carpeta_destino: Path = ruta_destino / nombre_backup.name

    logger.debug("Iniciando verificación de archivos a copiar")

    try:
        for elemento in ruta_origen.iterdir():
            if not _debe_ignorar(elemento, extensiones, carpetas, archivos):
                destino: Path = carpeta_destino / elemento.name
                lista.append((elemento, destino))

        if not carpeta_destino.exists():
            carpeta_destino.mkdir(parents=True, exist_ok=True)

        for origen, destino in lista:
            if origen.is_dir():
                shutil.copytree(origen, destino, dirs_exist_ok=True)
            else:
                shutil.copy2(origen, destino)

        logger.info(f"Archivos copiados correctamente ({len(lista)} elementos)")
        return lista

    except OSError as e:
        raise BackupError("Error al copiar archivos durante el backup", causa=e)


def crear_zip_backup(
    ruta_destino: Path,
    nombre_backup: Path,
    tipo: str = "zip",
    incluir_fecha: bool = True,
    formato_fecha: str = "%Y-%m-%d_%H:%M",
) -> Path:
    """Crea un archivo comprimido a partir de la carpeta de backup y la elimina.

    Args:
        ruta_destino: Directorio donde se creará el comprimido.
        nombre_backup: Ruta de la carpeta temporal de backup.
        tipo: Formato de compresión (zip, tar, gztar, etc.).
        incluir_fecha: Si se agrega timestamp al nombre.
        formato_fecha: Formato datetime para el timestamp.

    Returns:
        Ruta del archivo comprimido generado.

    Raises:
        BackupError: Si falla la creación o la limpieza.
    """
    fecha_actual: datetime = datetime.now()

    if incluir_fecha:
        nombre_final: str = (
            f"{nombre_backup.name}_{fecha_actual.strftime(formato_fecha)}"
        )
    else:
        nombre_final = nombre_backup.name

    ruta_comprimido: Path = ruta_destino / nombre_final

    logger.debug("Creando archivo comprimido y eliminando directorio temporal")

    try:
        shutil.make_archive(str(ruta_comprimido), tipo, nombre_backup)
        shutil.rmtree(nombre_backup)
        logger.info(f"Comprimido creado exitosamente: {ruta_comprimido}.{tipo}")
        return ruta_comprimido

    except (shutil.Error, OSError) as e:
        raise BackupError("Error al crear el archivo comprimido", causa=e)


def ejecucion_backup(config: ConfigSchema) -> None:
    """Ejecuta el proceso completo de backup.

    Valida la configuración, prepara las rutas (incluyendo modo prueba),
    copia los archivos filtrados y genera un archivo comprimido.

    Args:
        config: Objeto ConfigSchema con la configuración validada.

    Raises:
        ConfiguracionVaciaError: Si la configuración está vacía.
        BackupError: Si ocurre un error durante la ejecución.
    """
    logger.debug("Iniciando función `ejecucion_backup`")

    if not config:
        raise ConfiguracionVaciaError()

    ruta_origen: Path = Path(config.rutas.origen)
    ruta_destino: Path = Path(config.rutas.destino)
    nombre_backup: Path = ruta_destino / config.respaldo.nombre

    # --- Modo prueba ---
    if config.modo_prueba.activado:
        ruta_origen_str: Optional[str] = config.modo_prueba.ruta_origen
        ruta_destino_str: Optional[str] = config.modo_prueba.ruta_destino

        if ruta_origen_str and ruta_destino_str:
            ruta_origen = Path(ruta_origen_str)
            ruta_origen.mkdir(parents=True, exist_ok=True)
            ruta_destino = Path(ruta_destino_str)
            ruta_destino.mkdir(parents=True, exist_ok=True)
            nombre_backup = ruta_destino / config.respaldo.nombre

            if generador_test is not None:
                generador_test.generar_archivos_test(ruta_origen)
                logger.info("Archivos de prueba generados correctamente")
        else:
            logger.warning(
                "Modo prueba activado pero faltan rutas de prueba "
                "en la configuración"
            )

    # --- Copia de archivos ---
    copiar_archivos_backup(
        ruta_origen=ruta_origen,
        ruta_destino=ruta_destino,
        nombre_backup=nombre_backup,
        extensiones=config.filtros.ignorar_extensiones,
        carpetas=config.filtros.ignorar_carpetas,
        archivos=config.filtros.ignorar_archivos,
    )

    # --- Creación del comprimido ---
    crear_zip_backup(
        ruta_destino=ruta_destino,
        nombre_backup=nombre_backup,
        tipo=config.compresion.tipo,
        incluir_fecha=config.compresion.incluir_fecha,
        formato_fecha=config.compresion.formato_fecha,
    )

    logger.info("Proceso de backup finalizado exitosamente")
