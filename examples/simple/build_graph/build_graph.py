import os
from dotenv import load_dotenv

load_dotenv()

import asyncio
import logging
from t2g_sdk.client import T2GClient
from t2g_sdk.exceptions import T2GException
from t2g_sdk.models import Job


async def main():
    async with T2GClient() as client:
        try:
            job: Job = await client.build_graph(
                file_path="assets/pizza.txt",
                ontology_path="assets/pizza.ttl",
                output_path="./output/graph",
                save_to_neo4j=False,
                refresh_graph=False,
            )
            print("Job completed successfully:", job)
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    asyncio.run(main())
