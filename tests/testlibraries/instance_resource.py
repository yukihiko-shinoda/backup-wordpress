from pathlib import Path


class InstanceResource:
    """This class implements fixture of instance."""
    PATH_TESTS = Path(__file__).parent.parent
    PATH_PROJECT_HOME_DIRECTORY = PATH_TESTS.parent
    PATH_TEST_RESOURCES = PATH_TESTS / 'testresources'
    PATH_MYSQL_DUMP = PATH_TEST_RESOURCES / 'mysqldump'
    PATH_STATIC = PATH_TEST_RESOURCES / 'static'
    PATH_UPLOADS = PATH_TEST_RESOURCES / 'uploads'
    PATH_RED = PATH_UPLOADS / 'red.png'
    PATH_BLUE = PATH_UPLOADS / 'subdirectory/blue.png'
