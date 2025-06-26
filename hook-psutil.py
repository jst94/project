"""
PyInstaller hook for psutil module
This file is only used during the packaging process with PyInstaller
"""

try:
    from PyInstaller.utils.hooks import collect_submodules  # type: ignore # pyright: ignore[reportMissingModuleSource]
    hiddenimports = collect_submodules('psutil')
except ImportError:
    # PyInstaller not available - this is fine during development
    hiddenimports = []