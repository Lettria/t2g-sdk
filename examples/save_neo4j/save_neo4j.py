import asyncio
from t2g_sdk.client import T2GClient
from t2g_sdk.exceptions import T2GException
from t2g_sdk.models import Job


async def main():
    async with T2GClient() as client:
        try:
            await client.neo4j.save_output_to_neo4j(
                file_path="./output.cql",
            )
            print("Data successfully saved to Neo4j.")
        except T2GException as e:
            print(f"An API error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
