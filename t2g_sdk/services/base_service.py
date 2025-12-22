from typing import Any, Optional
import aiohttp
from ..exceptions import APIException, ConfigurationException
import logging
from t2g_sdk.config import settings

logging.basicConfig(level=settings.loglevel.upper())
logger = logging.getLogger(__name__)


class BaseService:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        api_host: str,
    ):
        self._session = session
        self.api_host = api_host

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> Any:
        """
        Internal method to make asynchronous requests to the API.
        """
        if not self._session:
            raise ConfigurationException(
                "Client session not found. Please use the client as an async context manager, e.g., `async with T2GClient() as client:`"
            )
        url = f"{self.api_host}{endpoint}"
        logger.debug("Making async API request: %s %s", method.upper(), url)
        try:
            async with self._session.request(method, url, **kwargs) as response:
                if response.status >= 400:
                    try:
                        error_body = await response.json()
                    except Exception:
                        error_body = await response.text()

                    if response.status >= 500:
                        logger.error(
                            "Async API request failed: %s %s -> %s",
                            method.upper(),
                            url,
                            error_body,
                        )
                    elif response.status != 409:
                        logger.debug(
                            "Async API request returned error: %s %s -> %s",
                            method.upper(),
                            url,
                            error_body,
                        )

                    raise APIException(
                        status_code=response.status,
                        message=(
                            str(error_body["message"])
                            if isinstance(error_body, dict) and "message" in error_body
                            else str(error_body)
                        ),
                    )
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error("Async request failed: %s", e)
            raise APIException(status_code=500, message=str(e)) from e
