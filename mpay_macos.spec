# -*- mode: python ; coding: utf-8 -*-
import os

static_dir = "static"
images_dir = "images"
env = os.path.join("env/lib/python3.11/site-packages/")


file_path = os.path.join(os.getcwd(), static_dir, images_dir)
a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        (file_path, os.path.join(static_dir, images_dir)),
        (f"{env}/Common/cimages", "Common/cimages"),
    ],
    hiddenimports=["PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="main",
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
    icon=[os.path.join(static_dir, images_dir, "logo.ico")],
)
# app = BUNDLE(
#     exe,
#     name="main.app",
#     # icon="static/images/logo.ico",
#     bundle_identifier=None,
# )
