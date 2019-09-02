#!/usr/bin/env python
"""This module implements only calling Zaim CSV converter package."""
from backupwordpress.wordpress_backup_executor import WordpressBackupExecutor


def main() -> None:
    """This function calls Zaim CSV converter package."""
    WordpressBackupExecutor.restore()


if __name__ == '__main__':
    main()
