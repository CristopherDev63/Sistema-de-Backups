# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec para generar un ejecutable del sistema de backups.
# USO:
#   pyinstaller build.spec
#
# Para generar un solo archivo:
#   pyinstaller --onefile build.spec
#
# Para macOS .app:
#   pyinstaller --windowed build.spec

import sys
from pathlib import Path

block_cipher = None

ROOT_DIR = Path(__file__).parent.resolve()

a = Analysis(
    [str(ROOT_DIR / "src" / "main.py")],
    pathex=[str(ROOT_DIR)],
    binaries=[],
    datas=[
        (str(ROOT_DIR / "config.json"), "."),
    ],
    hiddenimports=[
        "pydantic",
        "pydantic._internal",
        "pydantic._internal._config",
        "pydantic._internal._fields",
        "pydantic._internal._validators",
        "src.config",
        "src.backup",
        "src.exceptions",
        "src.log_setup",
        "src.monitor",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "matplotlib",
        "numpy",
        "PIL",
        "cv2",
        "pandas",
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="backup",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Para macOS .app bundle (sin terminal)
app = BUNDLE(
    exe,
    name="Backup.app",
    icon=None,
    bundle_identifier="com.backup.sistema",
    info_plist={
        "CFBundleName": "Sistema de Backups",
        "CFBundleDisplayName": "Sistema de Backups",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "NSHighResolutionCapable": True,
    },
)
