"""Path handling module for backupwordpress.

This module centralizes all path-related functionality, including:
- Standard pathlib.Path from Python standard library
- Platform-aware path utilities (Windows short path handling)

Usage:
    from backupwordpress.pathlib import Path, get_short_path_name

    # get_short_path_name works cross-platform:
    # - On Windows: converts to short path format (8.3 names)
    # - On other platforms: returns path unchanged
    short_path = get_short_path_name(some_path)
"""

import platform
from pathlib import Path

if platform.system() == "Windows":  # pragma: no cover
    # Only import Windows-specific module on Windows
    from backupwordpress.pathlib import windows


def get_short_path_name(path: Path) -> Path:
    """Get short path name for the given path (platform-aware).

    On Windows, this converts long paths to short path format (8.3 filenames)
    to work around the 260-character path length limitation.

    On Unix-like systems (Linux, macOS), this returns the path unchanged
    since they don't have the same path length restrictions.

    Args:
        path: The path to convert

    Returns:
        Path object with short path name on Windows, unchanged on other platforms

    Raises:
        ImportError: If running on Windows but pywin32 is not installed
    """
    if platform.system() == "Windows":  # pragma: no cover
        return windows.get_short_path_name(path)
    # On Unix-like systems, return path unchanged
    return path


__all__ = ["Path", "get_short_path_name"]
