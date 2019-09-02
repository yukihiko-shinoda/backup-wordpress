import shutil

import pytest

from backupwordpress.wordpress_backup_executor import WordpressBackupExecutor
from tests.testlibraries.instance_resource import InstanceResource


@pytest.fixture
def path_for_back_up_test(yaml_config_file):
    yaml_config_file.backup.mkdir()
    yaml_config_file.docker_compose_wordpress_project.mkdir()
    shutil.copytree(
        str(InstanceResource.PATH_MYSQL_DUMP),
        str(yaml_config_file.docker_compose_wordpress_project / 'initdb.d')
    )

    docker_compose_wordpress_project_static = (
        yaml_config_file.docker_compose_wordpress_project / 'wordpress-s3/web/static'
    )
    docker_compose_wordpress_project_static.mkdir(parents=True)
    docker_compose_wordpress_project_static.rmdir()
    shutil.copytree(
        str(InstanceResource.PATH_STATIC),
        str(docker_compose_wordpress_project_static)
    )
    docker_compose_wordpress_project_uploads = (
        yaml_config_file.docker_compose_wordpress_project / 'wordpress-s3/web/app/uploads'
    )
    docker_compose_wordpress_project_uploads.mkdir(parents=True)
    docker_compose_wordpress_project_uploads.rmdir()
    shutil.copytree(
        str(InstanceResource.PATH_UPLOADS),
        str(docker_compose_wordpress_project_uploads)
    )
    yield yaml_config_file


@pytest.fixture
def path_for_restore_test(yaml_config_file):
    yaml_config_file.backup.mkdir()
    (yaml_config_file.backup / '99991231235959').mkdir()
    (yaml_config_file.backup / '99991231235958').mkdir()
    (yaml_config_file.docker_compose_wordpress_project / 'initdb.d').mkdir(parents=True)
    (yaml_config_file.docker_compose_wordpress_project / 'wordpress-s3/web/static').mkdir(parents=True)
    (yaml_config_file.docker_compose_wordpress_project / 'wordpress-s3/web/app/uploads').mkdir(parents=True)
    for file in InstanceResource.PATH_MYSQL_DUMP.glob('*'):
        shutil.copy2(str(file), str(yaml_config_file.backup / '99991231235959'))
    backup_static = (yaml_config_file.backup / '99991231235959/static')
    shutil.copytree(str(InstanceResource.PATH_STATIC), str(backup_static))
    backup_uploads = (yaml_config_file.backup / '99991231235959/uploads')
    shutil.copytree(str(InstanceResource.PATH_UPLOADS), str(backup_uploads))
    yield yaml_config_file


class TestWordpressBackupExecutor:
    # pylint: disable=unused-argument
    @staticmethod
    def test_back_up(patch_datetime_now, path_for_back_up_test):
        WordpressBackupExecutor.back_up()
        assert (path_for_back_up_test.backup / '99991231235959/mysql_dump_20190831174529.sql').read_text() == 'a'
        assert sum(1 for _ in (path_for_back_up_test.backup / '99991231235959/static').rglob('*')) == 3
        assert (path_for_back_up_test.backup / '99991231235959/static/static1.txt').read_text() == 'c'
        assert (path_for_back_up_test.backup / '99991231235959/static/subdirectory/static2.txt').read_text() == 'd'
        assert sum(1 for _ in (path_for_back_up_test.backup / '99991231235959/uploads').rglob('*')) == 3
        assert (path_for_back_up_test.backup / '99991231235959/uploads/red.png').read_bytes(
        ) == InstanceResource.PATH_RED.read_bytes()
        assert (path_for_back_up_test.backup / '99991231235959/uploads/subdirectory/blue.png').read_bytes(
        ) == InstanceResource.PATH_BLUE.read_bytes()

    # pylint: disable=unused-argument
    @staticmethod
    def test_restore(patch_datetime_now, path_for_restore_test):
        WordpressBackupExecutor.restore()
        for file in path_for_restore_test.docker_compose_wordpress_project.rglob('*'):
            print(file)
        path_sql = path_for_restore_test.docker_compose_wordpress_project / 'initdb.d/mysql_dump_20190831174529.sql'
        assert path_sql.read_text() == 'a'
        path_static = path_for_restore_test.docker_compose_wordpress_project / 'wordpress-s3/web/static'
        assert sum(1 for _ in path_static.rglob('*')) == 3
        path_static1 = path_for_restore_test.docker_compose_wordpress_project / 'wordpress-s3/web/static/static1.txt'
        assert path_static1.read_text() == 'c'
        static2 = path_for_restore_test.docker_compose_wordpress_project / (
            'wordpress-s3/web/static/subdirectory/static2.txt'
        )
        assert static2.read_text() == 'd'
        path_uploads = path_for_restore_test.docker_compose_wordpress_project / 'wordpress-s3/web/app/uploads'
        assert sum(1 for _ in path_uploads.rglob('*')) == 3
        path_red = path_for_restore_test.docker_compose_wordpress_project / 'wordpress-s3/web/app/uploads/red.png'
        assert path_red.read_bytes() == InstanceResource.PATH_RED.read_bytes()
        path_blue = path_for_restore_test.docker_compose_wordpress_project / (
            'wordpress-s3/web/app/uploads/subdirectory/blue.png'
        )
        assert path_blue.read_bytes() == InstanceResource.PATH_BLUE.read_bytes()
