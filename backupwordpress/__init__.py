"""Backup WordPress package for managing WordPress backups and restores."""

from backupwordpress.config import Config
from backupwordpress.pathlib import Path

CONFIG: Config = Config()


PATH_FILE_CONFIG = Path(__file__).parent.parent / "config.yml"

__all__ = ["CONFIG", "PATH_FILE_CONFIG", "Config", "Path"]
