from backupwordpress import Config, PATH_FILE_CONFIG


class TestConfig:
    @staticmethod
    def test_load(yaml_config_file):
        """Arguments should load yaml file."""
        config = Config()
        config.load(PATH_FILE_CONFIG)
        assert config.backup_root_directory == yaml_config_file.backup
        assert config.docker_compose_wordpress_project_directory == yaml_config_file.docker_compose_wordpress_project
