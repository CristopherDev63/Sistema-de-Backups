"""Sistema de Backups.

Paquete modular para la generación de backups con validación
Pydantic, logging estructurado y soporte para modo test.

Módulos disponibles:
    - config: Modelos Pydantic y carga de configuración.
    - backup: Lógica de copia, filtrado y compresión ZIP.
    - exceptions: Excepciones personalizadas.
    - log_setup: Configuración del logging.
    - monitor: Lectura de logs para auto-commit.
"""
