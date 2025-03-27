from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import sqlalchemy

from .parameters import (
    DATA_DIR,
    DEFAULT_SQL_URL,
    SQLALCHEMY_DATABASE,
    SQLALCHEMY_DRIVER,
    SQLALCHEMY_HOST,
    SQLALCHEMY_PORT,
    SQLALCHEMY_QUERY,
    SQLALCHEMY_USERNAME,
    TIME_ZONE,
    get_sqlalchemy_password,
)


def get_current_time():
    return datetime.now(ZoneInfo(TIME_ZONE))


def create_sql_engine() -> sqlalchemy.engine.base.Engine:
    if not SQLALCHEMY_DRIVER:
        if not Path(DATA_DIR).is_dir():
            raise FileNotFoundError(
                f'Cannot access database file - directory "{DATA_DIR}" does not exist in app directory'
            )
        return sqlalchemy.create_engine(DEFAULT_SQL_URL)

    sql_url = sqlalchemy.URL.create(
        SQLALCHEMY_DRIVER,
        SQLALCHEMY_USERNAME,
        get_sqlalchemy_password(),
        SQLALCHEMY_HOST,
        SQLALCHEMY_PORT,
        SQLALCHEMY_DATABASE,
        SQLALCHEMY_QUERY,
    )
    return sqlalchemy.create_engine(sql_url)
