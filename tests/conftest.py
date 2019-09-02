from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pytest
import yaml
from fixturefilehandler.factories import DeployerFactory
from fixturefilehandler.file_paths import YamlConfigFilePathBuilder

from backupwordpress import wordpress_backup_executor
from tests.testlibraries.instance_resource import InstanceResource

YAML_CONFIG_FILE_PATH = YamlConfigFilePathBuilder(
    path_target_directory=InstanceResource.PATH_PROJECT_HOME_DIRECTORY,
    path_test_directory=InstanceResource.PATH_TEST_RESOURCES
)
YamlConfigFileDeployer = DeployerFactory.create(YAML_CONFIG_FILE_PATH)


@dataclass
class PathForTest:
    backup: Path
    docker_compose_wordpress_project: Path


@pytest.fixture
def yaml_config_file(tmp_path):
    """This fixture prepares YAML config file and loads it."""
    path_for_test = PathForTest(
        tmp_path / 'backup',
        tmp_path / 'docker_compose_word_press_project',
    )
    YAML_CONFIG_FILE_PATH.resource.write_text(
        yaml.dump({
            'backup_root_directory': str(path_for_test.backup),
            'docker_compose_wordpress_project_directory': str(path_for_test.docker_compose_wordpress_project)
        })
    )

    YamlConfigFileDeployer.setup()
    yield path_for_test
    YamlConfigFileDeployer.teardown()


@pytest.fixture
def patch_datetime_now(monkeypatch, request):
    date_time = getattr(request, 'param', datetime(9999, 12, 31, 23, 59, 59))

    class MockDateTime:
        @classmethod
        def now(cls):
            return date_time

    monkeypatch.setattr(wordpress_backup_executor, 'datetime', MockDateTime)
    yield date_time
