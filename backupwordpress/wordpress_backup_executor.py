"""WordPress backup execution orchestrator."""

import shutil
from datetime import UTC
from datetime import datetime

from backupwordpress import CONFIG
from backupwordpress import PATH_FILE_CONFIG
from backupwordpress.backup_directory import BackupDirectory
from backupwordpress.docker_compose_wordpress_project_directory import DockerComposeWordpressProjectDirectory


class WordpressBackupExecutor:
    """Main orchestrator for WordPress backup and restore operations."""

    @staticmethod
    def back_up() -> None:
        """Execute WordPress backup operation."""
        CONFIG.load(PATH_FILE_CONFIG)
        now = datetime.now(tz=UTC)

        path_root = CONFIG.path_backup_root_directory / now.strftime("%Y%m%d%H%M%S")
        path_root.mkdir()
        backup_directory = BackupDirectory(path_root)

        docker_compose_wordpress_project_directory = DockerComposeWordpressProjectDirectory(
            CONFIG.path_docker_compose_wordpress_project_directory,
        )

        shutil.copy2(str(docker_compose_wordpress_project_directory.mysql_dump), str(backup_directory.root))

        shutil.copytree(str(docker_compose_wordpress_project_directory.static), str(backup_directory.static))

        shutil.copytree(str(docker_compose_wordpress_project_directory.uploads), str(backup_directory.uploads))

    @staticmethod
    def restore() -> None:
        """Execute WordPress restore operation from latest backup."""
        CONFIG.load(PATH_FILE_CONFIG)

        docker_compose_wordpress_project_directory = DockerComposeWordpressProjectDirectory(
            CONFIG.path_docker_compose_wordpress_project_directory,
        )
        backup_directory = BackupDirectory(sorted(CONFIG.path_backup_root_directory.glob("./*"), reverse=True)[0])
        shutil.copy2(str(backup_directory.mysql_dump), str(docker_compose_wordpress_project_directory.init_db))

        if docker_compose_wordpress_project_directory.static_exists:
            shutil.rmtree(str(docker_compose_wordpress_project_directory.static))
        shutil.copytree(str(backup_directory.static), str(docker_compose_wordpress_project_directory.temporary_static))
        shutil.move(
            str(docker_compose_wordpress_project_directory.temporary_static),
            str(docker_compose_wordpress_project_directory.static),
        )

        if docker_compose_wordpress_project_directory.uploads_exists:
            shutil.rmtree(str(docker_compose_wordpress_project_directory.uploads))
        shutil.copytree(
            str(backup_directory.uploads),
            str(docker_compose_wordpress_project_directory.temporary_uploads),
        )
        shutil.move(
            str(docker_compose_wordpress_project_directory.temporary_uploads),
            str(docker_compose_wordpress_project_directory.uploads),
        )
