"""Docker Compose WordPress project directory structure management."""

from backupwordpress.pathlib import Path
from backupwordpress.pathlib import get_short_path_name


class DockerComposeWordpressProjectDirectory:
    """Represents the Docker Compose WordPress project directory structure."""

    def __init__(self, path: Path) -> None:
        """Initialize Docker Compose WordPress project directory.

        Args:
            path: Root path of the Docker Compose WordPress project
        """
        self.path = path
        self.init_db = path / "initdb.d"
        self._static = path / "wordpress-s3/web/static"
        self._uploads = path / "wordpress-s3/web/app/uploads"

    @property
    def mysql_dump(self) -> Path:
        """Get the latest MySQL dump file.

        Returns:
            Path to the most recent .sql file
        """
        return sorted(self.init_db.glob("*.sql"), reverse=True)[0]

    @property
    def temporary_static(self) -> Path:
        """Get temporary static directory path at drive root.

        Returns:
            Path using drive anchor to minimize path length
        """
        return Path(f"{self.path.anchor}static")

    @property
    def temporary_uploads(self) -> Path:
        """Get temporary uploads directory path at drive root.

        Returns:
            Path using drive anchor to minimize path length
        """
        return Path(f"{self.path.anchor}uploads")

    @property
    def static(self) -> Path:
        """Get static directory path with platform-aware conversion.

        Returns:
            Short path on Windows if exists, normal path otherwise
        """
        if not self.static_exists:
            return self._static
        # Convert to short path if needed (handles platform differences internally)
        return get_short_path_name(self._static)

    @property
    def uploads(self) -> Path:
        """Get uploads directory path with platform-aware conversion.

        Returns:
            Short path on Windows if exists, normal path otherwise
        """
        if not self.uploads_exists:
            return self._uploads
        # Convert to short path if needed (handles platform differences internally)
        return get_short_path_name(self._uploads)

    @property
    def static_exists(self) -> bool:
        """Check if static directory exists.

        Returns:
            True if static directory exists
        """
        return self._static.exists()

    @property
    def uploads_exists(self) -> bool:
        """Check if uploads directory exists.

        Returns:
            True if uploads directory exists
        """
        return self._uploads.exists()
