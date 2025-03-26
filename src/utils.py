from datetime import datetime
from os import environ
from zoneinfo import ZoneInfo

from .constants import SECRET_DIR


def get_current_time():
    return datetime.now(ZoneInfo("Europe/Riga"))


def get_required_environment_variable(environment_variable_name: str) -> str:
    try:
        return environ[environment_variable_name]
    except KeyError as e:
        raise KeyError(
            f"Environment variable {environment_variable_name} is not set"
        ) from e


def get_secret_value(secret_name: str) -> str:
    try:
        with open(f"{SECRET_DIR}/{secret_name}") as secret_file:
            return secret_file.read().strip()
    except (FileNotFoundError, PermissionError) as e:
        raise KeyError(f"Secret {secret_name} is not set") from e
