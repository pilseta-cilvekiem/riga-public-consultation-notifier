from os import environ, getenv
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs

from .enums.public_consultation_type import PublicConsultationType


def _get_enabled_public_consultation_types(
    public_consultation_types_string: str,
) -> list[PublicConsultationType]:
    public_consultation_type_strings = [
        public_consultation_type_string.strip()
        for public_consultation_type_string in public_consultation_types_string.split(
            ","
        )
    ]
    public_consultation_types = [
        PublicConsultationType(public_consultation_type_string)
        for public_consultation_type_string in public_consultation_type_strings
        if public_consultation_type_string
    ] or list(PublicConsultationType)
    return public_consultation_types


def _get_required_environment_variable(environment_variable_name: str) -> str:
    try:
        return environ[environment_variable_name]
    except KeyError as e:
        raise KeyError(
            f"Environment variable {environment_variable_name} is not set"
        ) from e


DATA_DIRECTORY = "data"
DATABASE_DRIVER = getenv("DATABASE_DRIVER")
DATABASE_HOST = getenv("DATABASE_HOST")
sqlalchemy_port_string = getenv("DATABASE_PORT")
DATABASE_NAME = getenv("DATABASE_NAME")
DATABASE_PASSWORD_FILE = getenv("DATABASE_PASSWORD_FILE")
DATABASE_PORT = int(sqlalchemy_port_string) if sqlalchemy_port_string else None
DATABASE_QUERY_STRING_PARAMETERS = parse_qs(getenv("DATABASE_QUERY_STRING_PARAMETERS"))
DATABASE_USERNAME = getenv("DATABASE_USERNAME")
days_to_store_inactive_public_consultations = getenv(
    "DAYS_TO_STORE_INACTIVE_PUBLIC_CONSULTATIONS", 365
)
DAYS_TO_STORE_INACTIVE_PUBLIC_CONSULTATIONS = (
    int(days_to_store_inactive_public_consultations)
    if days_to_store_inactive_public_consultations
    else None
)
DEFAULT_DATABASE_URL = f"sqlite:///{DATA_DIRECTORY}/sqlite.db"
ENABLED_PUBLIC_CONSULTATION_TYPES = _get_enabled_public_consultation_types(
    getenv("ENABLED_PUBLIC_CONSULTATION_TYPES", "")
)
ROOT_URL = "https://www.riga.lv"
SLACK_BOT_USER_OAUTH_TOKEN_FILE = _get_required_environment_variable(
    "SLACK_BOT_USER_OAUTH_TOKEN_FILE"
)
SLACK_CHANNEL_ID = _get_required_environment_variable("SLACK_CHANNEL_ID")
TIME_ZONE = getenv("TIME_ZONE", "Europe/Riga")


def get_slack_bot_user_oauth_token() -> str:
    slack_bot_user_oauth_token = _get_file_contents(SLACK_BOT_USER_OAUTH_TOKEN_FILE)
    return slack_bot_user_oauth_token


def get_database_password() -> Optional[str]:
    database_password = (
        _get_file_contents(DATABASE_PASSWORD_FILE) if DATABASE_PASSWORD_FILE else None
    )
    return database_password


def _get_file_contents(file_path: str) -> str:
    file_contents = Path(file_path).read_text().strip()
    return file_contents
