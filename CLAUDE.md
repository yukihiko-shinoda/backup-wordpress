# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a WordPress backup and restore utility for Docker Compose-based WordPress projects, designed primarily for Windows environments. The tool backs up MySQL dumps and WordPress static/upload files to timestamped directories, and can restore from the latest backup.

## Commands

### Development Environment

Use `uv` for package management (preferred over pipenv):

```bash
# Install dependencies
uv sync --python 3.13

# Run commands via uv
uv run <command>
```

### Testing

```bash
# Run fast tests (excludes @pytest.mark.slow)
uv run invoke test

# Run all tests
uv run invoke test.all

# Run tests with coverage
uv run invoke test.coverage

# Run tests with coverage XML/HTML reports
uv run invoke test.coverage --xml
uv run invoke test.coverage --html
```

### Linting and Code Quality

```bash
# Fast linting (xenon, ruff, bandit, dodgy, flake8, pydocstyle)
uv run invoke lint

# Deep linting (mypy, pylint, semgrep) - slower but more thorough
uv run invoke lint.deep

# Individual linters
uv run invoke lint.mypy
uv run invoke lint.pylint
uv run invoke lint.flake8
uv run invoke lint.bandit
uv run invoke lint.ruff
uv run invoke lint.semgrep

# Check code complexity
uv run invoke lint.xenon
uv run invoke lint.radon
```

### Code Formatting

```bash
# Format code with docformatter and Ruff
uv run invoke style

# Check formatting only (without modifying files)
uv run invoke style --check-only
```

### Building and Distribution

```bash
# Build source and wheel packages
uv run invoke dist

# Clean build artifacts
uv run invoke clean.dist
uv run invoke clean.python
uv run invoke clean.tests
uv run invoke clean  # Clean all
```

### Running the Application

```bash
# Backup WordPress (via entry point)
uv run back_up.py

# Restore from latest backup
uv run restore.py

# Using Docker
docker compose up
```

## Architecture

### Core Components

**WordpressBackupExecutor** ([backupwordpress/wordpress_backup_executor.py](backupwordpress/wordpress_backup_executor.py))
- Main orchestrator with two static methods: `back_up()` and `restore()`
- Loads config from `config.yml` in project root
- Creates timestamped backup directories (format: `YYYYMMDDHHMMSS`)
- Coordinates between `BackupDirectory` and `DockerComposeWordpressProjectDirectory`

**BackupDirectory** ([backupwordpress/backup_directory.py](backupwordpress/backup_directory.py))
- Represents a timestamped backup directory structure
- Properties: `root`, `static`, `uploads`, `mysql_dump`
- `mysql_dump` property finds the latest `.sql` file in the backup

**DockerComposeWordpressProjectDirectory** ([backupwordpress/docker_compose_wordpress_project_directory.py](backupwordpress/docker_compose_wordpress_project_directory.py))
- Represents the Docker Compose WordPress project structure
- Platform-aware path handling: uses Windows short paths only on Windows systems
- Properties for paths: `init_db`, `static`, `uploads`, `mysql_dump`
- Temporary paths (`temporary_static`, `temporary_uploads`) use drive anchor to avoid path length issues

**Config** ([backupwordpress/config.py](backupwordpress/config.py))
- Uses `YamlDataClassConfig` for YAML-based configuration
- Two required fields: `backup_root_directory` and `docker_compose_wordpress_project_directory`
- Custom `load()` method converts YAML string paths to `Path` objects after loading
- Global instance `CONFIG` initialized in `__init__.py`
- Config file expected at `config.yml` in project root

**Path Module** ([backupwordpress/pathlib/](backupwordpress/pathlib/))
- Centralized module for all path-related functionality
- `__init__.py`: Main interface exposing:
  - `Path`: Re-exported from Python's standard library
  - `get_short_path_name(path)`: Platform-aware function for path conversion
    - On Windows: Converts to short path format (8.3 names) to handle long paths
    - On Unix-like systems: Returns path unchanged
    - Internally delegates to `windows.py` on Windows platforms only
- `windows.py`: Windows-specific implementation
  - Contains the actual `win32api.GetShortPathName()` wrapper
  - Only imported when running on Windows

**Import Convention**: All backupwordpress modules import from `backupwordpress.pathlib`:
```python
from backupwordpress.pathlib import Path, get_short_path_name
```
This provides a single point of control for path handling and keeps platform-specific logic transparent to callers.

### Backup Flow

1. Load config from `config.yml`
2. Create timestamped directory under `backup_root_directory`
3. Copy MySQL dump from `initdb.d/*.sql` (latest file) to backup root
4. Copy entire `wordpress-s3/web/static` directory to backup
5. Copy entire `wordpress-s3/web/app/uploads` directory to backup

### Restore Flow

1. Load config from `config.yml`
2. Find latest backup directory (sorted reverse alphabetically)
3. Copy backup's MySQL dump to Docker project's `initdb.d/`
4. For static/uploads: remove existing, copy to temporary location at drive root, then move to final location (workaround for Windows path length limits)

### Testing Infrastructure

**Fixtures** ([tests/conftest.py](tests/conftest.py))
- `yaml_config_file`: Creates temporary config YAML with test paths
- `patch_datetime_now`: Mocks datetime for predictable backup directory names (default: 9999-12-31 23:59:59)
- Uses `fixturefilehandler` for deploying/tearing down config files

Test resources are in [tests/testresources/](tests/testresources/) and helper libraries in [tests/testlibraries/](tests/testlibraries/).

## Platform-Specific Notes

### Cross-Platform Compatibility

The codebase now supports both Windows and Unix-like systems (Linux, macOS):

- **Windows-specific code** is isolated in [backupwordpress/pathlib/windows.py](backupwordpress/pathlib/windows.py)
- **Path imports** are centralized through [backupwordpress/pathlib/](backupwordpress/pathlib/) module
- Windows path handling (`win32api.GetShortPathName()`) is only invoked on Windows systems
- Platform detection uses `platform.system() == 'Windows'` before importing Windows-specific modules
- The `pywin32` dependency is platform-conditional: `pywin32; platform_system == 'Windows'`

### Windows-Specific Behavior

- Uses short path names to handle Windows long path limitations (paths > 260 characters)
- Temporary paths use drive anchor (`C:\static`, `C:\uploads`) to minimize path length
- Short path conversion only applies to existing paths

### Unix-Like Systems Behavior

- Paths are used as-is without conversion
- Temporary paths use root anchor (`/static`, `/uploads`)
- No `pywin32` dependency required

### Testing

Tests are platform-aware and verify correct behavior on both Windows and Unix systems. The [tests/test_docker_compose_wordpress_project_directory.py](tests/test_docker_compose_wordpress_project_directory.py) test suite includes platform-specific assertions.

## Configuration

The project expects a `config.yml` file at the repository root with this structure:

```yaml
backup_root_directory: /path/to/backups
docker_compose_wordpress_project_directory: /path/to/wordpress-docker-project
```

Test fixtures create this automatically with temporary paths.
