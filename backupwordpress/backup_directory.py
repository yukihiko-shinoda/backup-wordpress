from pathlib import Path


class BackupDirectory:
    def __init__(self, path_root: Path):
        self.root = path_root
        self.static = self.root / 'static'
        self.uploads = self.root / 'uploads'

    @property
    def mysql_dump(self):
        return sorted(self.root.glob('*.sql'), reverse=True)[0]
