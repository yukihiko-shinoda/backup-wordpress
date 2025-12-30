"""Tests for WordpressBackupExecutor."""

import shutil
from pathlib import Path

import pytest

from backupwordpress.wordpress_backup_executor import WordpressBackupExecutor
from tests.conftest import PathForTest
from tests.testlibraries.instance_resource import InstanceResource

# Expected number of files in static and uploads directories
EXPECTED_FILE_COUNT = 3


@pytest.fixture
def path_for_back_up_test(yaml_config_file: PathForTest) -> PathForTest:
    """Prepare test environment for backup test."""
    yaml_config_file.backup.mkdir()
    yaml_config_file.docker_compose_wordpress_project.mkdir()
    shutil.copytree(
        str(InstanceResource.PATH_MYSQL_DUMP),
        str(yaml_config_file.docker_compose_wordpress_project / "initdb.d"),
    )

    docker_compose_wordpress_project_static = (
        yaml_config_file.docker_compose_wordpress_project / "wordpress-s3/web/static"
    )
    docker_compose_wordpress_project_static.mkdir(parents=True)
    docker_compose_wordpress_project_static.rmdir()
    shutil.copytree(str(InstanceResource.PATH_STATIC), str(docker_compose_wordpress_project_static))
    docker_compose_wordpress_project_uploads = (
        yaml_config_file.docker_compose_wordpress_project / "wordpress-s3/web/app/uploads"
    )
    docker_compose_wordpress_project_uploads.mkdir(parents=True)
    docker_compose_wordpress_project_uploads.rmdir()
    shutil.copytree(str(InstanceResource.PATH_UPLOADS), str(docker_compose_wordpress_project_uploads))
    return yaml_config_file


@pytest.fixture
def path_for_restore_test(yaml_config_file: PathForTest) -> PathForTest:
    """Prepare test environment for restore test."""
    yaml_config_file.backup.mkdir()
    (yaml_config_file.backup / "99991231235959").mkdir()
    (yaml_config_file.backup / "99991231235958").mkdir()
    (yaml_config_file.docker_compose_wordpress_project / "initdb.d").mkdir(parents=True)
    (yaml_config_file.docker_compose_wordpress_project / "wordpress-s3/web/static").mkdir(parents=True)
    (yaml_config_file.docker_compose_wordpress_project / "wordpress-s3/web/app/uploads").mkdir(parents=True)
    for file in InstanceResource.PATH_MYSQL_DUMP.glob("*"):
        shutil.copy2(str(file), str(yaml_config_file.backup / "99991231235959"))
    backup_static = yaml_config_file.backup / "99991231235959/static"
    shutil.copytree(str(InstanceResource.PATH_STATIC), str(backup_static))
    backup_uploads = yaml_config_file.backup / "99991231235959/uploads"
    shutil.copytree(str(InstanceResource.PATH_UPLOADS), str(backup_uploads))
    return yaml_config_file


class TestWordpressBackupExecutor:
    """Test class for WordpressBackupExecutor."""

    @pytest.mark.usefixtures("patch_datetime_now")
    def test_back_up(self, path_for_back_up_test: PathForTest) -> None:  # pylint: disable=redefined-outer-name
        """Test backup functionality."""
        WordpressBackupExecutor.back_up()
        assert (path_for_back_up_test.backup / "99991231235959/mysql_dump_20190831174529.sql").read_text() == "a"
        self.assert_backup_static(path_for_back_up_test.backup / "99991231235959/static")
        self.assert_backup_uploads(path_for_back_up_test.backup / "99991231235959/uploads")

    @staticmethod
    def assert_backup_static(backup: Path) -> None:
        """Assert static files in backup."""
        assert sum(1 for _ in backup.rglob("*")) == EXPECTED_FILE_COUNT
        static1 = backup / "static1.txt"
        assert static1.read_text() == "c"
        static2 = backup / "subdirectory/static2.txt"
        assert static2.read_text() == "d"

    @staticmethod
    def assert_backup_uploads(backup: Path) -> None:
        """Assert uploads files in backup."""
        assert sum(1 for _ in backup.rglob("*")) == EXPECTED_FILE_COUNT
        red = backup / "red.png"
        assert red.read_bytes() == InstanceResource.read_bytes_red()
        blue = backup / "subdirectory/blue.png"
        assert blue.read_bytes() == InstanceResource.read_bytes_blue()

    @pytest.mark.usefixtures("patch_datetime_now")
    def test_restore(self, path_for_restore_test: PathForTest) -> None:  # pylint: disable=redefined-outer-name
        """Test restore functionality."""
        WordpressBackupExecutor.restore()
        path_sql = path_for_restore_test.docker_compose_wordpress_project / "initdb.d/mysql_dump_20190831174529.sql"
        assert path_sql.read_text() == "a"
        self.assert_restore_static(
            path_for_restore_test.docker_compose_wordpress_project / "wordpress-s3/web/static",
        )
        self.assert_restore_uploads(
            path_for_restore_test.docker_compose_wordpress_project / "wordpress-s3/web/app/uploads",
        )

    def assert_restore_static(self, restored: Path) -> None:
        """Assert static files after restore."""
        assert sum(1 for _ in restored.rglob("*")) == EXPECTED_FILE_COUNT
        static1 = restored / "static1.txt"
        assert static1.read_text() == "c"
        static2 = restored / "subdirectory/static2.txt"
        assert static2.read_text() == "d"

    def assert_restore_uploads(self, restored: Path) -> None:
        """Assert uploads files after restore."""
        assert sum(1 for _ in restored.rglob("*")) == EXPECTED_FILE_COUNT
        red = restored / "red.png"
        assert red.read_bytes() == InstanceResource.read_bytes_red()
        blue = restored / "subdirectory/blue.png"
        assert blue.read_bytes() == InstanceResource.read_bytes_blue()
