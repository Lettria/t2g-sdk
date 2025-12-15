# SPDX-FileCopyrightText: 2023-present Your Name <you@example.com>
#
# SPDX-License-Identifier: MIT
"""
Configuration for the T2G SDK.
"""
import sys
from typing import Optional
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from .exceptions import ConfigurationException

import logging


logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Settings for the T2G SDK.
    """

    t2g_api_host: str = "https://oath.t2g-staging.lettria.net"
    lettria_api_key: str
    neo4j_uri: Optional[str] = None
    neo4j_user: Optional[str] = None
    neo4j_password: Optional[str] = None
    loglevel: str = "WARNING"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


try:
    settings = Settings(**{})
except ValidationError as e:
    missing_fields = [
        error["loc"][0] for error in e.errors() if error["type"] == "missing"
    ]
    logger.error(
        f"Missing configuration fields: {', '.join(str(field) for field in missing_fields)}"
    )
    sys.exit(1)
