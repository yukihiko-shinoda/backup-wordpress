"""Tests for Config."""

from backupwordpress import PATH_FILE_CONFIG
from backupwordpress import Config
from tests.conftest import PathForTest


class TestConfig:
    """Test class for Config."""

    @staticmethod
    def test_load(yaml_config_file: PathForTest) -> None:
        """Arguments should load yaml file."""
        config = Config()
        config.load(PATH_FILE_CONFIG)
        assert config.backup_root_directory == yaml_config_file.backup
        assert config.docker_compose_wordpress_project_directory == yaml_config_file.docker_compose_wordpress_project
