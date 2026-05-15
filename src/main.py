"""Punto de entrada del sistema de backups.

Orquesta la configuración, la ejecución del backup y el monitoreo
posterior. Es un módulo deliberadamente delgado; toda la lógica
está delegada en los submódulos (`config`, `backup`, `monitor`).

Ejemplo de uso:
    python -m src.main
"""

from pathlib import Path
import json
import sys
import logging

from pydantic import ValidationError

from src.log_setup import configurar_logging, _resolver_nivel
from src.config import cargando_configuracion, ConfigSchema
from src.backup import ejecucion_backup
from src.monitor import lectura_log
from src.exceptions import ConfiguracionVaciaError, BackupError

ROOT_DIR: Path = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

RUTA_CONFIG: Path = Path("./config.json")

# Logging inicial con valores por defecto
configurar_logging()
logger: logging.Logger = logging.getLogger(__name__)


def main() -> None:
    """Punto de entrada principal del sistema de backups.

    Carga la configuración desde el JSON, ajusta el logging según
    lo definido en el archivo, ejecuta el backup completo y lee el
    log generado para mostrar un resumen.

    Raises:
        ValidationError: Si la configuración no pasa la validación Pydantic.
        Exception: Captura genérica para errores inesperados.
    """
    try:
        config: ConfigSchema = cargando_configuracion(archivo=RUTA_CONFIG)

        # Reconfigurar logging con los valores del JSON
        logging.root.handlers.clear()
        configurar_logging(
            nivel=config.logging.nivel,
            ruta_log=config.logging.archivo,
        )

        ejecucion_backup(config=config)

        ruta_log: Path = Path(config.logging.archivo)
        if ruta_log.exists():
            total_info: int = lectura_log(ruta=ruta_log)
            logger.info(f"Resumen: {total_info} operaciones INFO registradas")

        logger.info("Programa finalizado con éxito")

    except ValidationError as e:
        logging.critical(f"Error de validación Pydantic: {e.error_count()} errores")
        for error in e.errors():
            logging.error(f"  - {error['loc']}: {error['msg']}")
        sys.exit(1)

    except FileNotFoundError:
        logging.critical("No se pudo encontrar el archivo de configuración")
        sys.exit(1)

    except json.JSONDecodeError:
        logging.critical("El archivo de configuración tiene un formato JSON inválido")
        sys.exit(1)

    except ConfiguracionVaciaError:
        logging.critical("La configuración cargada está vacía")
        sys.exit(1)

    except BackupError as e:
        logging.critical(f"Error durante el backup: {e.mensaje}")
        sys.exit(1)

    except Exception as e:
        logging.critical(f"Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
