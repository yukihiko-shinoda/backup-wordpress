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
        r"""Get temporary static directory path with platform-specific optimization.

        This property returns different paths based on the platform to optimize for platform-specific
        constraints and requirements:

        On Windows:
            Uses drive root (e.g., C:\static) to minimize path length and avoid hitting the 260-character
            MAX_PATH limitation. During restore operations, both source (backup) and destination paths
            contribute to total path length. By using the shortest possible temporary path at the drive
            root, we minimize the risk of path length errors during file copy operations.

        On Unix/Linux:
            Uses parent directory with .tmp suffix (e.g., /path/to/static.tmp) for two reasons:
            1. Avoids permission issues - cannot create directories at filesystem root (/)
            2. Enables atomic move operations - staying on the same filesystem allows shutil.move()
               to use rename(), which is atomic at the filesystem level

        The two-step copy-to-temp-then-move pattern provides:
        - Atomic directory replacement (no partial state visible)
        - Safety (original remains intact if copy fails)
        - Clean replacement (no file merging)

        Returns:
            Temporary path for static directory based on platform
        """
        # On Windows, anchor is like 'C:\\', on Unix it's '/'
        if self.path.anchor == "/":
            # Unix: use parent directory with temp suffix for atomic move
            return self._static.parent / f"{self._static.name}.tmp"
        # Windows: use drive root to minimize path length
        return Path(f"{self.path.anchor}static")  # pragma: no cover

    @property
    def temporary_uploads(self) -> Path:
        r"""Get temporary uploads directory path with platform-specific optimization.

        This property returns different paths based on the platform to optimize for platform-specific
        constraints and requirements:

        On Windows:
            Uses drive root (e.g., C:\uploads) to minimize path length and avoid hitting the 260-character
            MAX_PATH limitation. During restore operations, both source (backup) and destination paths
            contribute to total path length. By using the shortest possible temporary path at the drive
            root, we minimize the risk of path length errors during file copy operations.

        On Unix/Linux:
            Uses parent directory with .tmp suffix (e.g., /path/to/uploads.tmp) for two reasons:
            1. Avoids permission issues - cannot create directories at filesystem root (/)
            2. Enables atomic move operations - staying on the same filesystem allows shutil.move()
               to use rename(), which is atomic at the filesystem level

        The two-step copy-to-temp-then-move pattern provides:
        - Atomic directory replacement (no partial state visible)
        - Safety (original remains intact if copy fails)
        - Clean replacement (no file merging)

        Returns:
            Temporary path for uploads directory based on platform
        """
        # On Windows, anchor is like 'C:\\', on Unix it's '/'
        if self.path.anchor == "/":
            # Unix: use parent directory with temp suffix for atomic move
            return self._uploads.parent / f"{self._uploads.name}.tmp"
        # Windows: use drive root to minimize path length
        return Path(f"{self.path.anchor}uploads")  # pragma: no cover

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
