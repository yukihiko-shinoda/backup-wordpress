from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class Config(YamlDataClassConfig):
    """This class implements configuration wrapping.

    Note on Path handling:
    Fields are declared as Union[str, Path] rather than just Path because
    yamldataclassconfig v2.x validates types BEFORE applying any decoder metadata.
    If we declare fields as Path, the validation fails when loading from YAML
    (which contains strings) before any conversion can happen.

    The custom load() method below handles the string-to-Path conversion after
    the parent class has loaded and validated the YAML data.
    """
    backup_root_directory: Optional[Union[str, Path]] = None
    docker_compose_wordpress_project_directory: Optional[Union[str, Path]] = None

    def load(
        self,
        path: Optional[Union[Path, str]] = None,
        *,
        path_is_absolute: bool = False
    ) -> None:
        """Load config from YAML and convert string paths to Path objects.

        This override is necessary because yamldataclassconfig validates types
        before applying decoders. The validation sequence is:
        1. Load YAML (contains strings)
        2. Validate types (would fail if fields were typed as Path)
        3. Apply decoder metadata (never reached if validation fails)

        Our approach:
        1. Accept strings during validation (Union[str, Path] type)
        2. Load with parent class (stores as strings)
        3. Convert strings to Path objects after loading (this method)

        We use object.__setattr__() to bypass yamldataclassconfig's property
        setters and set the converted Path values directly.
        """
        super().load(path, path_is_absolute=path_is_absolute)

        # Convert string paths to Path objects after loading
        if isinstance(self.backup_root_directory, str):
            object.__setattr__(
                self, 'backup_root_directory', Path(self.backup_root_directory)
            )
        if isinstance(self.docker_compose_wordpress_project_directory, str):
            object.__setattr__(
                self,
                'docker_compose_wordpress_project_directory',
                Path(self.docker_compose_wordpress_project_directory)
            )
