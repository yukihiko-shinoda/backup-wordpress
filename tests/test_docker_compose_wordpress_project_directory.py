"""Tests for DockerComposeWordpressProjectDirectory."""

import platform
from pathlib import Path

from backupwordpress.docker_compose_wordpress_project_directory import DockerComposeWordpressProjectDirectory


class Paths:
    """Base class for platform-specific path assertions."""

    def __init__(self, path_static: Path, path_uploads: Path) -> None:
        self.path_static = str(path_static)
        self.path_uploads = str(path_uploads)

    def assert_paths(self) -> None:
        """Assert paths match platform-specific format."""
        raise NotImplementedError

    @staticmethod
    def create_temporary(path_static: Path, path_uploads: Path) -> "Paths":
        """Create platform-specific Paths instance."""
        if platform.system() == "Windows":
            return PathsForWindows(path_static, path_uploads)
        return TemporaryPathsForLinux(path_static, path_uploads)

    @staticmethod
    def create(path_static: Path, path_uploads: Path) -> "Paths":
        """Create platform-specific Paths instance."""
        if platform.system() == "Windows":
            return PathsForWindows(path_static, path_uploads)
        return ActualPathsForLinux(path_static, path_uploads)


class PathsForWindows(Paths):
    """Windows-specific path assertions."""

    def assert_paths(self) -> None:
        """Assert paths use Windows path separators."""
        assert self.path_static.endswith(r"\static")
        assert self.path_uploads.endswith(r"\uploads")


class TemporaryPathsForLinux(Paths):
    """Unix/Linux-specific path assertions."""

    def assert_paths(self) -> None:
        """Assert paths use Unix path separators."""
        assert self.path_static.endswith("/static.tmp")
        assert self.path_uploads.endswith("/uploads.tmp")


class ActualPathsForLinux(Paths):
    """Unix/Linux-specific path assertions."""

    def assert_paths(self) -> None:
        """Assert paths use Unix path separators."""
        assert self.path_static.endswith("/static")
        assert self.path_uploads.endswith("/uploads")


class DockerComposeWordpressProjectDirectoryForTest(DockerComposeWordpressProjectDirectory):
    """Test wrapper for DockerComposeWordpressProjectDirectory with assertions."""

    def __init__(self, path: Path) -> None:
        super().__init__(path)
        assert isinstance(self.static, Path)
        assert isinstance(self.uploads, Path)
        assert not self.static_exists
        assert not self.uploads_exists

    def assert_temp_paths(self) -> None:
        """Assert temporary paths format based on platform."""
        paths = Paths.create_temporary(self.temporary_static, self.temporary_uploads)
        paths.assert_paths()

    def make_directories(self) -> None:
        """Create static and uploads directories for testing existence checks."""
        self._static.mkdir(parents=True)
        self._uploads.mkdir(parents=True)
        assert self.static_exists
        assert self.uploads_exists

    def assert_actual_paths(self) -> None:
        """Assert actual paths format based on platform."""
        paths = Paths.create(self.static, self.uploads)
        paths.assert_paths()


class TestDockerComposeWordPressProjectDirectory:
    """Test class for DockerComposeWordpressProjectDirectory."""

    @staticmethod
    def test(tmp_path: Path) -> None:
        """Test platform-specific path handling."""
        path_init_db = tmp_path / "initdb.d"
        path_init_db.mkdir()
        (path_init_db / "mysql_dump_20190831174529.sql").write_text("a")
        (path_init_db / "mysql_dump_20190831030000.sql").write_text("b")
        docker_compose_wordpress_project_directory = DockerComposeWordpressProjectDirectoryForTest(tmp_path)
        assert docker_compose_wordpress_project_directory.mysql_dump.read_text() == "a"

        # Check temporary paths - format depends on platform
        docker_compose_wordpress_project_directory.assert_temp_paths()
        docker_compose_wordpress_project_directory.make_directories()
        # Check actual paths - on non-Windows, should just be normal paths
        docker_compose_wordpress_project_directory.assert_actual_paths()
