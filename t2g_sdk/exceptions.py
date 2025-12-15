# SPDX-FileCopyrightText: 2023-present Your Name <you@example.com>
#
# SPDX-License-Identifier: MIT
"""
Custom exceptions for the T2G SDK.
"""


class T2GException(Exception):
    """Base exception for all T2G SDK errors."""

    pass


class APIException(T2GException):
    """Raised for errors returned by the T2G API."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error: {status_code}: {message}")


class ConfigurationException(T2GException):
    """Raised for configuration errors, such as a missing API token."""

    pass
