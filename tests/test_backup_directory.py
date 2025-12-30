"""Tests for BackupDirectory."""

from pathlib import Path

from backupwordpress.backup_directory import BackupDirectory


class TestBackupDirectory:
    """Test class for BackupDirectory."""

    @staticmethod
    def test(tmp_path: Path) -> None:
        """Test that mysql_dump property returns the latest SQL file."""
        (tmp_path / "mysql_dump_20190831174529.sql").write_text("a")
        (tmp_path / "mysql_dump_20190831030000.sql").write_text("b")
        backup_directory = BackupDirectory(tmp_path)
        assert backup_directory.mysql_dump.read_text() == "a"
