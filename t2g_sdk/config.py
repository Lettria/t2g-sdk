# SPDX-FileCopyrightText: 2023-present Your Name <you@example.com>
#
# SPDX-License-Identifier: MIT
"""
Configuration for the T2G SDK.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings for the T2G SDK.
    """

    t2g_api_host: str = "https://oath.t2g-staging.lettria.net"
    lettria_api_key: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

