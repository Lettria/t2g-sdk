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
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"
    loglevel: str = "WARNING"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


try:
    settings = Settings(**{})
except ValidationError as e:
    logger.error(e.json())

    sys.exit(1)
