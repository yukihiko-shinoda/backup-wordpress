"""Windows-specific path handling utilities.

This module contains Windows-specific functionality that depends on pywin32.
It should only be imported when running on Windows platforms.
"""
from pathlib import Path


def get_short_path_name(path: Path) -> Path:
    """Get Windows short path name to handle long path issues.

    Args:
        path: The path to convert to short path format

    Returns:
        Path object with short path name on Windows

    Raises:
        ImportError: If win32api is not available (non-Windows platform)
    """
    import win32api
    return Path(win32api.GetShortPathName(str(path)))
