from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import sqlalchemy

from .parameters import (
    DATA_DIR,
    DEFAULT_SQL_URL,
    SQL_DATABASE,
    SQL_DRIVER,
    SQL_HOST,
    SQL_PORT,
    SQL_QUERY_STRING_PARAMETERS,
    SQL_USERNAME,
    TIME_ZONE,
    get_sqlalchemy_password,
)


def get_current_time():
    return datetime.now(ZoneInfo(TIME_ZONE))


def create_sql_engine() -> sqlalchemy.engine.base.Engine:
    if not SQL_DRIVER:
        if not Path(DATA_DIR).is_dir():
            raise FileNotFoundError(
                f'Cannot access database file - directory "{DATA_DIR}" does not exist in app directory'
            )
        return sqlalchemy.create_engine(DEFAULT_SQL_URL)

    sql_url = sqlalchemy.URL.create(
        SQL_DRIVER,
        SQL_USERNAME,
        get_sqlalchemy_password(),
        SQL_HOST,
        SQL_PORT,
        SQL_DATABASE,
        SQL_QUERY_STRING_PARAMETERS,
    )
    return sqlalchemy.create_engine(sql_url)
