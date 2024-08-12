# -*- mode: python ; coding: utf-8 -*-
import os

# Définir les chemins des répertoires statiques et des images
static_dir = "static"
images_dir = "images"
icon_path = os.path.join(
    static_dir, images_dir, "logo.ico"
)  # Icône pour Windows (.ico)

# Chemin vers le fichier principal
main_script = "main.py"

# Analyse de l'application
a = Analysis(
    [main_script],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[
        (
            os.path.join(static_dir, images_dir),
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
    console=False,  # Changer à True pour les applications en ligne de commande
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,  # Icône pour Windows
)

# Création du bundle Windows (non nécessaire pour Windows, mais inclus pour la cohérence)
app = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Payments",  # Nom du bundle
)
