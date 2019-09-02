from dataclasses import dataclass, field
from pathlib import Path

from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class Config(YamlDataClassConfig):
    """This class implements configuration wrapping."""
    backup_root_directory: Path = field(  # type: ignore
        default=None,
        metadata={'dataclasses_json': {
            'decoder': Path,
            'mm_field': Path
        }}
    )
    docker_compose_wordpress_project_directory: Path = field(  # type: ignore
        default=None,
        metadata={'dataclasses_json': {
            'decoder': Path,
            'mm_field': Path
        }}
    )
