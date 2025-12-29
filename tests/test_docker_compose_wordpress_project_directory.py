import platform
from pathlib import Path

from backupwordpress.docker_compose_wordpress_project_directory import DockerComposeWordpressProjectDirectory


class TestDockerComposeWordPressProjectDirectory:
    @staticmethod
    def test(tmp_path):
        path_init_db = tmp_path / 'initdb.d'
        path_init_db.mkdir()
        (path_init_db / 'mysql_dump_20190831174529.sql').write_text('a')
        (path_init_db / 'mysql_dump_20190831030000.sql').write_text('b')
        docker_compose_wordpress_project_directory = DockerComposeWordpressProjectDirectory(tmp_path)
        assert docker_compose_wordpress_project_directory.mysql_dump.read_text() == 'a'

        # Check temporary paths - format depends on platform
        temp_static = str(docker_compose_wordpress_project_directory.temporary_static)
        temp_uploads = str(docker_compose_wordpress_project_directory.temporary_uploads)
        if platform.system() == 'Windows':
            assert temp_static.endswith(r':\static')
            assert temp_uploads.endswith(r':\uploads')
        else:
            # On Unix-like systems, anchor is '/' so paths are /static and /uploads
            assert temp_static.endswith('/static')
            assert temp_uploads.endswith('/uploads')

        assert isinstance(docker_compose_wordpress_project_directory.static, Path)
        assert isinstance(docker_compose_wordpress_project_directory.uploads, Path)
        assert not docker_compose_wordpress_project_directory.static_exists
        assert not docker_compose_wordpress_project_directory.uploads_exists
        (tmp_path / 'wordpress-s3/web/static').mkdir(parents=True)
        (tmp_path / 'wordpress-s3/web/app/uploads').mkdir(parents=True)
        assert docker_compose_wordpress_project_directory.static_exists
        assert docker_compose_wordpress_project_directory.uploads_exists

        # Check actual paths - on non-Windows, should just be normal paths
        if platform.system() == 'Windows':
            # On Windows, paths may be converted to short path format
            assert str(docker_compose_wordpress_project_directory.static).endswith(r'\static')
            assert str(docker_compose_wordpress_project_directory.uploads).endswith(r'\uploads')
        else:
            # On Unix-like systems, paths should contain 'static' and 'uploads'
            assert 'static' in str(docker_compose_wordpress_project_directory.static)
            assert 'uploads' in str(docker_compose_wordpress_project_directory.uploads)
