# -*- mode: python ; coding: utf-8 -*-
import os

from PyInstaller.utils.hooks import collect_data_files

# Définir les chemins des répertoires statiques et des images
static_dir = "static"
images_dir = "images"
icon_path = os.path.join(
    static_dir, images_dir, "logo.icns"
)  # Icône pour macOS (.icns)

env = os.path.join("env/lib/python3.11/site-packages/")
# Chemin vers le fichier principal
main_script = "main.py"

# Analyse de l'application
a = Analysis(
    [main_script],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[
        (f"{env}/Common/cimages", "Common/cimages"),
        (
            os.path.join("static", "images"),
            "static/images",
        ),  # Inclure le répertoire static/images
    ],
    hiddenimports=["PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# Création de l'archive PYZ
pyz = PYZ(a.pure)

# Création de l'exécutable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Payments",  # Nom de l'exécutable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Changer à False pour les applications GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,  # Utiliser .icns pour macOS
)

# Création du bundle macOS
app = BUNDLE(
    exe,
    name="Payments.app",  # Nom du bundle
    icon=icon_path,  # Icône pour macOS
    bundle_identifier="com.fgs.payments",  # Identifiant unique pour l'application
)

# pkgbuild --root payload --identifier com.example.mpayment --version 1.0 --install-location /Applications Mpayment.pkg
