from backupwordpress.backup_directory import BackupDirectory


class TestBackupDirectory:
    @staticmethod
    def test(tmp_path):
        (tmp_path / 'mysql_dump_20190831174529.sql').write_text('a')
        (tmp_path / 'mysql_dump_20190831030000.sql').write_text('b')
        backup_directory = BackupDirectory(tmp_path)
        assert backup_directory.mysql_dump.read_text() == 'a'
