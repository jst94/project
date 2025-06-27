"""
PyInstaller hook for psutil module
This file is only used during the packaging process with PyInstaller
"""

try:
    from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_dynamic_libs  # type: ignore # pyright: ignore[reportMissingModuleSource]
    
    # Collect all psutil components
    hiddenimports = collect_submodules('psutil')
    datas = collect_data_files('psutil')
    binaries = collect_dynamic_libs('psutil')
    
except ImportError:
    # PyInstaller not available - this is fine during development
    hiddenimports = []
    datas = []
    binaries = []