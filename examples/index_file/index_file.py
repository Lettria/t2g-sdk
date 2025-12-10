import asyncio
from t2g_sdk.client import T2GClient
from t2g_sdk.exceptions import T2GException
from t2g_sdk.models import Job


async def main():
    async with T2GClient() as client:
        try:
            job: Job = await client.index_file(
                file_path="pizza.txt",
                ontology_path="pizza.ttl",
                save_to_neo4j=True,
            )
            print("Job completed successfully:", job)
        except T2GException as e:
            print(f"An API error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
