from app.config import Settings


def test_parse_bot_admins_from_csv() -> None:
    settings = Settings(
        BOT_TOKEN="token",
        DATABASE_USER="user",
        DATABASE_PASSWORD="pass",
        DATABASE_NAME="db",
        BOT_ADMINS="1, 2,3",
    )

    assert settings.bot_admins == [1, 2, 3]


def test_database_dsn_building() -> None:
    settings = Settings(
        BOT_TOKEN="token",
        DATABASE_HOST="db-host",
        DATABASE_PORT=5433,
        DATABASE_USER="user",
        DATABASE_PASSWORD="pass",
        DATABASE_NAME="dbname",
    )

    assert settings.database_dsn == "postgresql+asyncpg://user:pass@db-host:5433/dbname"
