import asyncio
import logging
import sys
from t2g_sdk.client import T2GClient
from t2g_sdk.exceptions import T2GException
from t2g_sdk.models import Job
from simple_graph_retriever.client import GraphRetrievalClient


async def main(file_path: str):
    async with T2GClient() as client:
        try:
            job: Job = await client.index_file(
                file_path=file_path,
                save_to_neo4j=True,
            )
            GraphRetrievalClient().index()

        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    script_input = sys.argv[1] if len(sys.argv) > 1 else None
    if not script_input:
        print("Please provide a file path as an argument.")
        sys.exit(1)
    asyncio.run(main(script_input))
