import asyncio
import os
from time import time
from typing import Any, Dict, List, Optional, cast
import aiohttp
import logging
import asyncio
import itertools
import sys
from time import time

from .base_service import BaseService
from ..models import Job, JobStatus
from ..exceptions import T2GException

logging.basicConfig(level=os.getenv("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class JobService(BaseService):
    async def submit_job(self, file_id: str, ontology_id: str | None = None) -> Job:
        """
        Asynchronously submits a job for processing.
        """
        response = await self._request(
            "POST",
            "/api/v0/job/submit",
            json={"fileId": file_id, "ontologyId": ontology_id},
        )
        job_data = response["job"]
        return Job(id=job_data["id"], status=job_data["status"])

    async def find_jobs(self, ids: List[str]) -> List[Job]:
        """
        Asynchronously finds one or more jobs by their IDs.
        """
        response = await self._request("POST", "/api/v0/job/find", json={"ids": ids})
        return [Job(id=job["id"], status=job["status"]) for job in response["jobs"]]

    async def download_job_output(
        self, job_id: str, output_path: Optional[str] = None
    ) -> str:
        """
        Asynchronously fetches a presigned URL and downloads the job output.
        """
        if output_path is None:
            output_path = f"{job_id}.output"
        download_urls = await self._get_download_urls(job_id)
        async with aiohttp.ClientSession() as download_session:
            await self._download_file(
                download_session,
                download_urls["ttlFileDownloadUrl"],
                f"{output_path}.ttl",
            )
            await self._download_file(
                download_session,
                download_urls["cqlFileDownloadUrl"],
                f"{output_path}.cql",
            )
        return output_path

    async def _get_download_urls(self, job_id: str) -> Dict[str, str]:
        """
        Asynchronously fetches a presigned URL to download the output of a job.
        """
        response = await self._request("GET", f"/api/v0/job/{job_id}/download-output")
        return {
            "ttlFileDownloadUrl": cast(Dict[str, Any], response)["ttlFileDownloadUrl"],
            "cqlFileDownloadUrl": cast(Dict[str, Any], response)["cqlFileDownloadUrl"],
        }

    async def _download_file(
        self, session: aiohttp.ClientSession, url: str, output_path: str
    ):
        """
        Asynchronously downloads a file from a URL and saves it.
        """
        logger.debug(f"Downloading file from {url}")
        logger.info(f"Downloading file to {output_path}")
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                with open(output_path, "wb") as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
        except aiohttp.ClientResponseError as e:
            raise T2GException(
                f"Failed to download file. Status: {e.status}, " f"Message: {e.message}"
            ) from e
        except Exception as e:
            raise T2GException(
                f"An unexpected error occurred during file download: {e}"
            ) from e
        logger.info(f"File downloaded successfully to {output_path}")

    async def run_job(
        self,
        file_id: str,
        ontology_id: str | None = None,
        polling_interval: int = 5,
        timeout: int = 3600,
    ) -> Job:
        """
        Asynchronously submits a job and polls for its completion with a terminal spinner.
        """

        async def spinner():
            for c in itertools.cycle("|/-\\"):
                sys.stdout.write(f"\rWaiting for job {job.id}... {c}")
                sys.stdout.flush()
                await asyncio.sleep(0.1)

        start_time = time()
        job = await self.submit_job(file_id, ontology_id)
        logger.debug(f"Job {job.id} submitted, status: {job.status}")

        spin_task = asyncio.create_task(spinner())

        try:
            while (
                job.status not in [JobStatus.FAILED, JobStatus.SUCCEEDED]
                and not job.stopped
            ):
                if time() - start_time > timeout:
                    raise T2GException(f"Timeout reached for job {job.id}")
                await asyncio.sleep(polling_interval)
                jobs = await self.find_jobs([job.id])
                if not jobs:
                    raise T2GException(f"Could not find job {job.id}")
                job = jobs[0]
                logger.debug(f"Job {job.id} status: {job.status}")
        finally:
            spin_task.cancel()
            sys.stdout.write("\r" + " " * 50 + "\r")  # Clear spinner line

        if job.status == JobStatus.FAILED:
            raise T2GException(f"Job {job.id} failed.")
        return job
