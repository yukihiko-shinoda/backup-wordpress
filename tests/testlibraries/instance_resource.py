"""Instance resource module for test fixtures."""

from pathlib import Path


class InstanceResource:
    """This class implements fixture of instance."""

    PATH_TESTS = Path(__file__).parent.parent
    PATH_PROJECT_HOME_DIRECTORY = PATH_TESTS.parent
    PATH_TEST_RESOURCES = PATH_TESTS / "testresources"
    PATH_MYSQL_DUMP = PATH_TEST_RESOURCES / "mysqldump"
    PATH_STATIC = PATH_TEST_RESOURCES / "static"
    PATH_UPLOADS = PATH_TEST_RESOURCES / "uploads"
    PATH_RED = PATH_UPLOADS / "red.png"
    PATH_BLUE = PATH_UPLOADS / "subdirectory/blue.png"

    @classmethod
    def read_bytes_red(cls) -> bytes:
        """Read red.png as bytes."""
        return cls.PATH_RED.read_bytes()

    @classmethod
    def read_bytes_blue(cls) -> bytes:
        """Read blue.png as bytes."""
        return cls.PATH_BLUE.read_bytes()
