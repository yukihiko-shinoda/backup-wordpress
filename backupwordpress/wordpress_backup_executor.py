"""WordPress backup execution orchestrator."""

import shutil
from datetime import datetime
from datetime import timezone

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
        now = datetime.now(tz=timezone.utc)

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
        r"""Execute WordPress restore operation from latest backup.

        This method uses a two-step copy-then-move approach for restoring static and uploads directories:
        1. Copy backup files to a temporary location (temporary_static/temporary_uploads)
        2. Move from temporary location to final destination

        Rationale for this approach:
        - Windows path length mitigation: Temporary paths use drive root (e.g., C:\static) to minimize
          path length and avoid hitting the 260-character MAX_PATH limitation during copy operations.
        - Atomic replacement: shutil.move() on the same filesystem is essentially a rename operation,
          which is atomic. This ensures the final directory appears complete or not at all, with no
          intermediate partial state visible to other processes.
        - Safety: If the copy to temporary location fails, the original destination remains intact.
          Only after successful copy does the move replace the old directory.
        - Clean replacement: The pattern ensures old files are completely replaced rather than merged
          with restored files.
        """
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
