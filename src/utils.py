from datetime import datetime
from pathlib import Path

import sqlalchemy

from .parameters import (
    DATA_DIRECTORY,
    DATABASE_DRIVER,
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_PORT,
    DATABASE_QUERY_STRING_PARAMETERS,
    DATABASE_USERNAME,
    DEFAULT_DATABASE_URL,
    get_database_password,
)


def get_current_time():
    return datetime.now()  # (ZoneInfo(TIME_ZONE))


def create_sql_engine() -> sqlalchemy.engine.base.Engine:
    if not DATABASE_DRIVER:
        if not Path(DATA_DIRECTORY).is_dir():
            raise FileNotFoundError(
                f'Cannot access database file - directory "{DATA_DIRECTORY}" does not exist in app directory'
            )
        return sqlalchemy.create_engine(DEFAULT_DATABASE_URL)

    sql_url = sqlalchemy.URL.create(
        DATABASE_DRIVER,
        DATABASE_USERNAME,
        get_database_password(),
        DATABASE_HOST,
        DATABASE_PORT,
        DATABASE_NAME,
        DATABASE_QUERY_STRING_PARAMETERS,
    )
    return sqlalchemy.create_engine(sql_url)
