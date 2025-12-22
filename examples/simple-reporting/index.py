import asyncio
import logging
from t2g_sdk.client import T2GClient
from t2g_sdk.exceptions import T2GException
from t2g_sdk.models import Job
from simple_graph_retriever.client import GraphRetrievalClient


async def main():
    async with T2GClient() as client:
        try:
            job: Job = await client.index_file(
                file_path="napoleon_wikipedia.txt",
                save_to_neo4j=True,
            )
            retrieval_client = GraphRetrievalClient()
            retrieval_client.index()

        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    asyncio.run(main())
