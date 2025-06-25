# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['psutil']
hiddenimports += collect_submodules('psutil')

a = Analysis(
    ['poe_craft_helper.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports + [
        'cv2', 'numpy', 'PIL', 'PIL._tkinter_finder',
        'tkinter', 'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.messagebox',
        'pytesseract', 'requests', 'json', 'threading', 'time', 'datetime',
        'random', 'os', 're', 'market_api', 'session_tracker', 'performance_optimizer'
    ],
    hookspath=['.'],
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
    name='PoE_Craft_Helper',
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
