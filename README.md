# Sistema de Backups

Este programa te permite hacer una copia de seguridad (backup) de tus
archivos de forma automatica. Eliges una carpeta de origen, el programa
copia todo lo importante, lo comprime en un ZIP y lo guarda donde tu
quieras.

## Primeros pasos (guia paso a paso)

Sigue estas instrucciones en orden y el programa funcionara.

### 1. Requisitos

Necesitas tener **Python 3.10 o superior** instalado en tu computadora.

Abre una terminal (simbolo del sistema en Windows, Terminal en macOS/Linux)
y verifica escribiendo:

```bash
python --version
```

Si ves algo como `Python 3.11.x` o superior, estas listo.

### 2. Crear un entorno virtual (recomendado)

El entorno virtual es como una cajita aparte donde se instalan las
librerias necesarias, sin ensuciar tu computadora.

**En macOS y Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

Al activarlo, veras algo como `(venv)` al inicio de la linea en la terminal.

### 3. Instalar las dependencias

Con el entorno virtual activado, ejecuta:

```bash
pip install -r requirements.txt
```

Esto instala `pydantic` (para validar la configuracion) y
`pyinstaller` (para crear un ejecutable, solo si lo necesitas).

### 4. Configurar el backup

Abre el archivo `config.json` con cualquier editor de texto (Block de
Notas, TextEdit, VS Code, etc.) y ajusta los valores:

```json
{
    "respaldo": {
        "nombre": "backup",
        "descripcion": "Mi primer backup"
    },
    "rutas": {
        "origen": "./tests/",
        "destino": "./tests/carpeta_destino"
    },
    "filtros": {
        "ignorar_extensiones": [".tmp", ".log"],
        "ignorar_carpetas": ["node_modules", ".git", "__pycache__"],
        "ignorar_archivos": [".DS_Store"]
    },
    "compresion": {
        "tipo": "zip",
        "incluir_fecha": true,
        "formato_fecha": "%Y-%m-%d_%H:%M"
    },
    "retencion": {
        "max_backups": 5,
        "dias_maximos": 30
    },
    "logging": {
        "nivel": "DEBUG",
        "archivo": "backup.log"
    },
    "modo_prueba": {
        "activado": false,
        "ruta_origen": "./tests/carpeta_origen",
        "ruta_destino": "./tests/carpeta_destino"
    }
}
```

| Seccion | Que hace |
|---|---|
| `respaldo` | El nombre y descripcion de tu copia de seguridad |
| `rutas` | La carpeta que quieres respaldar (`origen`) y donde se guardara (`destino`) |
| `filtros` | Archivos o carpetas que **NO** quieres incluir en el backup (ej. `.tmp`, `node_modules`) |
| `compresion` | El formato del comprimido (`zip` es el mas comun) y si le agrega la fecha al nombre |
| `retencion` | Cuantos backups mantener y por cuantos dias |
| `logging` | Como y donde se guarda el registro de lo que hizo el programa |
| `modo_prueba` | Modo para probar sin tocar tus archivos reales |

### 5. Ejecutar el backup

Con el entorno virtual activado y la terminal en la carpeta del proyecto,
escribe:

```bash
python -m src.main
```

El programa hara lo siguiente:

1. Leer y validar `config.json`
2. Revisar la carpeta de origen
3. Copiar los archivos (excluyendo los que estan en los filtros)
4. Comprimir todo en un ZIP
5. Guardar el ZIP en la carpeta de destino
6. Generar un archivo de log (`backup.log`) con el resultado

Veras algo como esto en pantalla:

```
DEBUG | 2026-05-15 10:42 | Ejecucion de la funcion cargando_configuracion
INFO  | 2026-05-15 10:42 | Configuracion JSON cargada y validada correctamente
INFO  | 2026-05-15 10:42 | Archivos copiados correctamente (3 elementos)
INFO  | 2026-05-15 10:42 | ZIP creado exitosamente
INFO  | 2026-05-15 10:42 | Programa finalizado con exito
```

## Probar sin riesgos (modo prueba)

Si activas `"activado": true` dentro de `modo_prueba` en el `config.json`,
el programa creara archivos de ejemplo en la carpeta de prueba y hara el
backup ahi. Tus carpetas reales no se tocaran.

Esto es util para ver como funciona antes de usarlo con datos importantes.

## Como se ve si algo sale mal

El programa es muy claro cuando encuentra un error. Por ejemplo, si falta
un campo en `config.json`:

```
CRITICAL | Error de validacion Pydantic: 1 errores
ERROR    |   - ('rutas', 'origen'): Field required
```

Traduccion: falta el campo `origen` en la seccion `rutas` del JSON.

## El archivo de registro (log)

Cada vez que ejecutas el programa se genera un archivo `backup.log` con
todo lo que hizo. Sirve para revisar si hubo problemas. Su formato es:

```
NIVEL | FECHA HORA | Mensaje
```

Los niveles pueden ser: `DEBUG` (detalle), `INFO` (aviso),
`WARNING` (atencion), `ERROR`, `CRITICAL` (error grave).

## Estructura de las carpetas del proyecto

Si tienes curiosidad de como esta organizado el proyecto internamente:

```
.
├── config.json              # Tu configuracion
├── backup.log               # Registro de cada ejecucion
├── requirements.txt         # Librerias necesarias
├── build.spec               # Para crear un ejecutable (avanzado)
├── build.py                 # Script para crear el ejecutable
├── src/                     # Codigo del programa
│   ├── main.py              # Punto de entrada
│   ├── config.py            # Validacion de la configuracion
│   ├── backup.py            # Logica del backup
│   ├── exceptions.py        # Mensajes de error personalizados
│   ├── log_setup.py         # Configuracion del registro
│   └── monitor.py           # Lectura del log
├── tests/
│   └── generador_test.py    # Genera archivos de prueba
└── README.md                # Este archivo
```

## Crear un ejecutable (para no depender de Python)

Si quieres convertir el programa en un archivo `.exe` (Windows) o
`.app` (macOS) que funcione sin tener Python instalado, puedes usar
el script incluido.

### Paso a paso

1. Activa el entorno virtual (paso 2 de la guia inicial)
2. Asegurate de tener instalado PyInstaller:

```bash
pip install pyinstaller
```

3. Ejecuta el script de empaquetado:

```bash
python build.py
```

4. El ejecutable se crea en la carpeta `dist/`:
   - En **Windows**: `dist/backup.exe`
   - En **macOS/Linux**: `dist/backup`

5. Copia el archivo `config.json` que quieras usar a la misma carpeta
   donde esta el ejecutable.

### Opciones adicionales

| Comando | Que hace |
|---|---|
| `python build.py` | Crea un solo archivo ejecutable (recomendado) |
| `python build.py --app` | Crea una aplicacion `.app` para macOS |
| `python build.py --onedir` | Crea una carpeta con el ejecutable (se abre mas rapido) |
| `python build.py --clean --onefile` | Limpia y vuelve a crear desde cero |

### En macOS: .app

```bash
python build.py --app
```

Esto genera `dist/Backup.app`. Puedes hacer doble clic para ejecutarlo.

**Importante:** el ejecutable busca el archivo `config.json` en la carpeta
donde lo ejecutas, no dentro del `.app`. Pon tu `config.json` junto al
ejecutable.
