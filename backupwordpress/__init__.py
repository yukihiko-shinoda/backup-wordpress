from pathlib import Path

from backupwordpress.config import Config

CONFIG: Config = Config()


PATH_FILE_CONFIG = Path(__file__).parent.parent / 'config.yml'
