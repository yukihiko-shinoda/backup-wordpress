"""Backup directory structure management."""

from backupwordpress.pathlib import Path


class BackupDirectory:
    """Represents a timestamped backup directory structure."""

    def __init__(self, path_root: Path) -> None:
        """Initialize backup directory.

        Args:
            path_root: Root path of the backup directory
        """
        self.root = path_root
        self.static = self.root / "static"
        self.uploads = self.root / "uploads"

    @property
    def mysql_dump(self) -> Path:
        """Get the latest MySQL dump file in the backup.

        Returns:
            Path to the most recent .sql file
        """
        return sorted(self.root.glob("*.sql"), reverse=True)[0]
