import logging
import os
import hashlib
from typing import Dict, List
from datetime import datetime
import aiohttp

from .base_service import BaseService
from ..models import Ontology, OntologyStatus
from ..exceptions import T2GException, APIException

logging.basicConfig(level=os.getenv("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class OntologyService(BaseService):
    async def create_ontology(self, name: str, source_hash: str) -> Dict:
        """
        Asynchronously creates a ontology and returns a presigned URL for uploading.
        """
        response = await self._request(
            "POST",
            "/api/v0/ontology",
            json={
                "name": name,
                "sourceHash": source_hash,
            },
        )
        ontology_data = response["ontology"]
        created_at_str = ontology_data["createdAt"].replace("Z", "+00:00")
        ontology = Ontology(
            id=ontology_data["id"],
            name=ontology_data["name"],
            status=OntologyStatus(ontology_data["status"]),
            created_at=datetime.fromisoformat(created_at_str),
        )
        upload_url = response.get("uploadUrl", "")
        return {"ontology": ontology, "upload_url": upload_url}

    async def find_ontologies(
        self, ids: list[str] | None = None, source_hashes: list[str] | None = None
    ) -> list[Ontology]:
        """
        Asynchronously finds one or more ontologies by their IDs.
        """
        logger.debug(
            "Finding ontologies with ids: %s or source_hashes: %s", ids, source_hashes
        )
        payload = {}
        if ids:
            payload["ids"] = ids
        if source_hashes:
            payload["sourceHashes"] = source_hashes
        response = await self._request("POST", "/api/v0/ontology/find", json=payload)
        ontologies: list[Ontology] = []
        for ontology_data in response["ontologies"]:
            created_at_str = ontology_data["createdAt"].replace("Z", "+00:00")
            ontology = Ontology(
                id=ontology_data["id"],
                name=ontology_data["name"],
                status=OntologyStatus(ontology_data["status"]),
                created_at=datetime.fromisoformat(created_at_str),
            )
            ontologies.append(ontology)
        return ontologies

    async def upload_ontology(self, ontology_path: str) -> Ontology:
        """
        Asynchronously creates a ontology record and uploads the ontology content.
        If a ontology with the same content already exists, it will be returned.
        """
        ontology_name = os.path.basename(ontology_path)
        with open(ontology_path, "rb") as f:
            ontology_content = f.read()
            source_hash = hashlib.sha256(ontology_content).hexdigest()

        try:
            response = await self.create_ontology(ontology_name, source_hash)
            ontology_obj = response["ontology"]
            upload_url = response["upload_url"]
            if not upload_url:
                # If the ontology is newly created, an upload URL is expected.
                raise T2GException("Failed to get upload URL for the new ontology.")
        except APIException as e:
            if e.status_code == 409:
                ontologies = await self.find_ontologies(source_hashes=[source_hash])
                if not ontologies:
                    raise T2GException(e) from e
                return ontologies[0]
            else:
                raise

        try:
            async with self._session.put(
                upload_url, data=ontology_content
            ) as resp:
                resp.raise_for_status()
        except FileNotFoundError:
            raise T2GException(f"Local ontology not found at: {ontology_path}")
        except aiohttp.ClientResponseError as e:
            raise T2GException(
                f"Failed to upload ontology to S3. Status: {e.status}, "
                f"Response: {e.message}"
            ) from e
        except Exception as e:
            raise T2GException(
                f"An unexpected error occurred during ontology upload: {e}"
            ) from e
        return ontology_obj
