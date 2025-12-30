from backupwordpress.config import Config
from backupwordpress.pathlib import Path

CONFIG: Config = Config()


PATH_FILE_CONFIG = Path(__file__).parent.parent / 'config.yml'
