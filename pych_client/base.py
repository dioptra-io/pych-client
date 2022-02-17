import json
import os
from typing import Optional, Tuple

from pych_client.constants import (
    BASE_URL_ENV,
    CREDENTIALS_FILE,
    DATABASE_ENV,
    DEFAULT_BASE_URL,
    DEFAULT_DATABASE,
    DEFAULT_PASSWORD,
    DEFAULT_USERNAME,
    PASSWORD_ENV,
    USERNAME_ENV,
)
from pych_client.logger import logger
from pych_client.typing import Params, Settings

# TODO: Benchmark different functions


def get_credentials(
    base_url: Optional[str],
    database: Optional[str],
    username: Optional[str],
    password: Optional[str],
) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    if base_url or database or username or password:
        logger.debug("using credentials from arguments")
        return base_url, database, username, password
    if (
        BASE_URL_ENV in os.environ
        or DATABASE_ENV in os.environ
        or USERNAME_ENV in os.environ
        or PASSWORD_ENV in os.environ
    ):
        logger.debug("using credentials from environment")
        return (
            os.environ.get(BASE_URL_ENV),
            os.environ.get(DATABASE_ENV),
            os.environ.get(USERNAME_ENV),
            os.environ.get(PASSWORD_ENV),
        )
    if CREDENTIALS_FILE.exists():
        logger.debug("using credentials from %s", CREDENTIALS_FILE)
        credentials = json.loads(CREDENTIALS_FILE.read_text())
        return (
            credentials.get("base_url"),
            credentials.get("database"),
            credentials.get("username"),
            credentials.get("password"),
        )
    return DEFAULT_BASE_URL, DEFAULT_DATABASE, DEFAULT_USERNAME, DEFAULT_PASSWORD


def get_http_params(query: str, params: Params, settings: Settings):
    http_params = {"query": query}
    if params:
        http_params |= {f"param_{k}": v for k, v in params.items()}
    if settings:
        http_params |= settings
    return http_params
