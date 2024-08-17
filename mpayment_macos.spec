# -*- mode: python ; coding: utf-8 -*-
import os

from PyInstaller.utils.hooks import collect_data_files

static_dir = "static"
images_dir = os.path.join(static_dir, "images")
icon_path = os.path.join(images_dir, "logo.icns")
# icon_path = os.path.join("static", "images", "logo.icns")
env_dir = os.path.join("env", "lib", "python3.11", "site-packages")
main_script = "main.py"

datas = collect_data_files(env_dir, includes=["**/*.py", "**/*.so"]) + [
    (images_dir, "static/images"),
]

a = Analysis(
    [main_script],
    pathex=[os.getcwd()],
    binaries=[],
    datas=datas,
    hiddenimports=["PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets"],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Payments",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

app = BUNDLE(
    exe,
    name="Payments.app",
    icon=icon_path,
    bundle_identifier="com.fgs.payments",
    version="1.0.0",
    info_plist={
        "NSPrincipalClass": "NSApplication",
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": "10.13",
    },
)
