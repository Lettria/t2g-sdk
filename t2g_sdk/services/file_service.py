import logging
import hashlib
from typing import Dict, List
from datetime import datetime
import aiohttp
import os

from .base_service import BaseService
from ..models import File, FileStatus
from ..exceptions import T2GException, APIException

logger = logging.getLogger(__name__)


class FileService(BaseService):
    async def create_file(self, name: str, source_hash: str) -> Dict:
        """
        Asynchronously creates a file and returns a presigned URL for uploading.
        """
        response = await self._request(
            "POST",
            "/api/v0/file",
            json={
                "name": name,
                "sourceHash": source_hash,
            },
        )
        file_data = response["file"]
        created_at_str = file_data["createdAt"].replace("Z", "+00:00")
        file = File(
            id=file_data["id"],
            name=file_data["name"],
            status=FileStatus(file_data["status"]),
            created_at=datetime.fromisoformat(created_at_str),
        )
        upload_url = response.get("uploadUrl", "")
        return {"file": file, "upload_url": upload_url}

    async def find_files(
        self, ids: list[str] | None = None, source_hashes: list[str] | None = None
    ) -> list[File]:
        """
        Asynchronously finds one or more files by their IDs.
        """
        logger.debug(
            "Finding files with ids: %s or source_hashes: %s", ids, source_hashes
        )
        payload = {}
        if ids:
            payload["ids"] = ids
        if source_hashes:
            payload["sourceHashes"] = source_hashes
        response = await self._request("POST", "/api/v0/file/find", json=payload)
        files: list[File] = []
        for file_data in response["files"]:
            created_at_str = file_data["createdAt"].replace("Z", "+00:00")
            file = File(
                id=file_data["id"],
                name=file_data["name"],
                status=FileStatus(file_data["status"]),
                created_at=datetime.fromisoformat(created_at_str),
            )
            files.append(file)
        return files

    async def upload_file(self, file_path: str) -> File:
        """
        Asynchronously creates a file record and uploads the file content.
        If a file with the same content already exists, it will be returned.
        """
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            file_content = f.read()
            source_hash = hashlib.sha256(file_content).hexdigest()

        try:
            response = await self.create_file(file_name, source_hash)
            file_obj = response["file"]
            upload_url = response["upload_url"]
            if not upload_url:
                # If the file is newly created, an upload URL is expected.
                raise T2GException("Failed to get upload URL for the new file.")
        except APIException as e:
            if e.status_code == 409:
                files = await self.find_files(source_hashes=[source_hash])
                if not files:
                    raise T2GException(e) from e
                return files[0]
            else:
                raise

        try:
            async with aiohttp.ClientSession() as s3_session:
                async with s3_session.put(upload_url, data=file_content) as resp:
                    resp.raise_for_status()
        except FileNotFoundError:
            raise T2GException(f"Local file not found at: {file_path}")
        except aiohttp.ClientResponseError as e:
            raise T2GException(
                f"Failed to upload file to S3. Status: {e.status}, "
                f"Response: {e.message}"
            ) from e
        except Exception as e:
            raise T2GException(
                f"An unexpected error occurred during file upload: {e}"
            ) from e
        return file_obj
