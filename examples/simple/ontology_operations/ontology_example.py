from dotenv import load_dotenv

load_dotenv()


import asyncio
import os
from t2g_sdk.client import T2GClient


async def main():
    ontology_path = "assets/example_ontology.ttl"

    async with T2GClient() as client:
        print(f"Uploading ontology: {ontology_path}")
        uploaded_ontology = await client.ontology.upload_ontology(ontology_path)
        print(
            f"Uploaded Ontology ID: {uploaded_ontology.id}, Name: {uploaded_ontology.name}, Status: {uploaded_ontology.status}"
        )

        await client.ontology.wait_for_ontology_upload(uploaded_ontology.id)

        print(f"Finding ontology with ID: {uploaded_ontology.id}")
        found_ontologies = await client.ontology.find_ontologies(
            ids=[uploaded_ontology.id]
        )
        if found_ontologies:
            print(
                f"Found Ontology ID: {found_ontologies[0].id}, Name: {found_ontologies[0].name}, Status: {found_ontologies[0].status}"
            )
        else:
            print("Ontology not found.")


if __name__ == "__main__":
    asyncio.run(main())
