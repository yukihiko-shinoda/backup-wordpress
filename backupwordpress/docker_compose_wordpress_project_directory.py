import platform
from pathlib import Path


class DockerComposeWordpressProjectDirectory:
    def __init__(self, path):
        self.path = path
        self.init_db = path / 'initdb.d'
        self._static = path / 'wordpress-s3/web/static'
        self._uploads = path / 'wordpress-s3/web/app/uploads'

    @property
    def mysql_dump(self):
        return sorted(self.init_db.glob('*.sql'), reverse=True)[0]

    @property
    def temporary_static(self):
        return Path(f'{self.path.anchor}static')

    @property
    def temporary_uploads(self):
        return Path(f'{self.path.anchor}uploads')

    @property
    def static(self):
        if not self.static_exists:
            return self._static

        # Only use Windows short path handling on Windows platform
        if platform.system() == 'Windows':
            from backupwordpress.windows import get_short_path_name
            return get_short_path_name(self._static)
        return self._static

    @property
    def uploads(self):
        if not self.uploads_exists:
            return self._uploads

        # Only use Windows short path handling on Windows platform
        if platform.system() == 'Windows':
            from backupwordpress.windows import get_short_path_name
            return get_short_path_name(self._uploads)
        return self._uploads

    @property
    def static_exists(self):
        return self._static.exists()

    @property
    def uploads_exists(self):
        return self._uploads.exists()
