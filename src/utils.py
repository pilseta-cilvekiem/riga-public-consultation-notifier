from datetime import datetime
from os import environ
from pathlib import Path
from typing import Optional
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


def get_required_secret_value(secret_name: str) -> str:
    try:
        return _get_secret_value(secret_name)
    except (FileNotFoundError, IsADirectoryError, PermissionError) as e:
        raise KeyError(f"Secret {secret_name} is not set") from e


def get_optional_secret_value(secret_name: str) -> Optional[str]:
    try:
        return _get_secret_value(secret_name)
    except (FileNotFoundError, IsADirectoryError, PermissionError):
        return None


def _get_secret_value(secret_name: str) -> str:
    secret_value = Path(f"{SECRET_DIR}/{secret_name}").read_text().strip()
    return secret_value
