# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

project_root = Path(SPECPATH)
tcl_root = Path(r"D:\Miniconda3\tcl")

a = Analysis(
    [str(project_root / "scripts" / "blog_gui.py")],
    pathex=[str(project_root / "scripts")],
    binaries=[],
    # Conda's Tcl/Tk layout is not always discovered correctly by the
    # PyInstaller hook. Keep the canonical runtime folder names expected by
    # pyi_rth__tkinter so the one-file executable works on machines without
    # Python installed.
    datas=[
        (str(tcl_root / "tcl8.6"), "_tcl_data"),
        (str(tcl_root / "tk8.6"), "_tk_data"),
    ],
    hiddenimports=["yaml"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name="DuckLingBlogManager",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / "img" / "blog-manager.ico"),
    exclude_binaries=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="DuckLingBlogManager",
)
