# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['blog-gui.py'],
    pathex=['md2html'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'md2html',
        'markdown',
        'yaml',
        'pygments',
        'pygments.lexers',
        'pygments.styles',
        'pygments.formatters',
        'pymdownx',
        'pymdownx.highlight',
        'pymdownx.superfences',
    ],
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
    a.binaries,
    a.datas,
    [],
    name='blog-gui',
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
)
