from pathlib import Path

import win32api


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
        return win32api.GetShortPathName(str(self._static)) if self.static_exists else self._static

    @property
    def uploads(self):
        return win32api.GetShortPathName(str(self._uploads)) if self.uploads_exists else self._uploads

    @property
    def static_exists(self):
        return self._static.exists()

    @property
    def uploads_exists(self):
        return self._uploads.exists()
