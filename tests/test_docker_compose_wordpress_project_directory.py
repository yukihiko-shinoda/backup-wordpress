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
        assert str(docker_compose_wordpress_project_directory.temporary_static).endswith(r':\static')
        assert str(docker_compose_wordpress_project_directory.temporary_uploads).endswith(r':\uploads')
        assert isinstance(docker_compose_wordpress_project_directory.static, Path)
        assert isinstance(docker_compose_wordpress_project_directory.uploads, Path)
        assert not docker_compose_wordpress_project_directory.static_exists
        assert not docker_compose_wordpress_project_directory.uploads_exists
        (tmp_path / 'wordpress-s3/web/static').mkdir(parents=True)
        (tmp_path / 'wordpress-s3/web/app/uploads').mkdir(parents=True)
        assert docker_compose_wordpress_project_directory.static_exists
        assert docker_compose_wordpress_project_directory.uploads_exists
        assert docker_compose_wordpress_project_directory.static.endswith(r'\static')
        assert docker_compose_wordpress_project_directory.uploads.endswith(r'\uploads')
