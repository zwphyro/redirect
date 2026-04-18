import subprocess
import sys

from src.settings import settings


def main():
    """Run clickhouse-migrations with settings from environment."""
    cmd = [
        "clickhouse-migrations",
        "--db-host",
        settings.ch_host,
        "--db-port",
        settings.ch_native_port,
        "--db-user",
        settings.ch_user,
        "--db-password",
        settings.ch_password,
        "--db-name",
        settings.ch_db_name,
        "--migrations-dir",
        "migrations",
    ]

    result = subprocess.run(cmd, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
