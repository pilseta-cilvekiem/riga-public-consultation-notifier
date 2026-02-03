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


def create_sql_engine() -> sqlalchemy.engine.base.Engine:
    if not DATABASE_DRIVER:
        Path(DATA_DIRECTORY).mkdir(exist_ok=True)
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
