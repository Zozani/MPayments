# -*- mode: python ; coding: utf-8 -*-

import os

env = os.path.join("env/lib/python3.11/site-packages/")
# Example directory and file names
static_dir = "static"
images_dir = "images"
current_working_directory = os.getcwd()

file_path = os.path.join(current_working_directory, static_dir, images_dir)
print(f"{file_path=}")
a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[],
    datas=[
        (file_path, os.path.join(static_dir, images_dir)),
        (f"{env}/Common/cimages", "Common/cimages"),
    ],
    hiddenimports=[],
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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[os.path.join(current_working_directory, static_dir, images_dir, "logo.ico")],
)


coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name="mpay")
