# Lettria's Text-to-Graph SDK 🚀

[![PyPI version](https://badge.fury.io/py/t2g-sdk.svg)](https://badge.fury.io/py/t2g-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to the official Python SDK for Lettria's Text-to-Graph (T2G) API! This SDK provides a convenient way to interact with the T2G API, allowing you to unlock the power of knowledge graphs from your text data directly within your Python applications.

## 🌟 Overview

Lettria's Text-to-Graph (T2G) technology transforms unstructured text into structured knowledge graphs. This SDK is designed to simplify the process of sending your data to the T2G API and retrieving the results, whether you are indexing a single document, a collection of files, or building complex ontologies.

This SDK is built with developers in mind, providing a clean, asynchronous client to handle API requests efficiently.

## ✨ Features

- **Asynchronous Client**: Built with `asyncio` and `aiohttp` for high-performance, non-blocking API calls.
- **Simple Interface**: Easy-to-use methods for indexing files and managing jobs.
- **Data Validation**: Leverages `pydantic` for robust and reliable data modeling.
- **Neo4j Integration**: Directly save your graph data to a Neo4j instance.
- **Flexible Configuration**: Configure the SDK via environment variables or directly in your code.
- **Built-in Error Handling**: Gracefully handles API errors with custom exceptions.

## 📦 Installation

You can install the SDK using pip:

```bash
pip install t2g-sdk==1.0.0-rc.9
```

## 🚀 Getting Started

To start using the SDK, you will need an API key from Lettria.

To create an API key, please visit our preview instance [here](https://app.t2g-staging.lettria.net/).

Access to the API is managed by whitelisting. If you require access, please contact us at [hello@lettria.com](mailto:hello@lettria.com) to request whitelisting.

### Configuration

The SDK can be configured by setting the following environment variable:

- `LETTRIA_API_KEY`: Your Lettria API key.

Alternatively, you can pass this value directly to the `T2GClient` constructor.

### Quick Example: Indexing a File

This example demonstrates how to index a local text file and save the resulting graph to Neo4j.

```python
import asyncio
from t2g_sdk.client import T2GClient
from t2g_sdk.exceptions import T2GException
from t2g_sdk.models import Job


async def main():
    # It is recommended to use the client as a context manager
    async with T2GClient() as client:
        try:
            # Index a file and save the result to Neo4j
            job: Job = await client.index_file(
                file_path="path/to/your/document.txt",
                # You can also specify an ontology file
                # ontology_path="path/to/your/ontology.ttl",
                save_to_neo4j=True,
            )
            print("🎉 Job completed successfully!")
            print("Job details:", job)
        except T2GException as e:
            print(f"An API error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

```

## 📚 API Reference

The main entry point of the SDK is the `T2GClient` class.

### `t2g_sdk.client.T2GClient`

The asynchronous client for interacting with the T2G API.

**Methods:**

- `async def index_file(file_path: str, ontology_path: str = None, output_path: str = None, save_to_neo4j: bool = False) -> Job`:
  Processes a file by uploading it, running a job, and downloading the output.
  - `file_path`: Path to the file to process.
  - `ontology_path` (optional): Path to an ontology file (e.g., `.ttl`).
  - `output_path` (optional): The path to save the output to. If not provided, a default path will be used.
  - `save_to_neo4j` (optional): If `True`, saves the result to your configured Neo4j instance.

**Properties:**

- `file` -> `FileService`: Provides access to file-related operations.
- `job` -> `JobService`: Provides access to job-related operations.
- `ontology` -> `OntologyService`: Provides access to ontology-related operations.
- `neo4j` -> `Neo4jService`: Provides access to Neo4j-related operations.

---

### Services

### `T2GClient.file` -> `FileService`

The `FileService` handles file-related operations and is accessed via the `file` property of an active `T2GClient` instance.

**Methods:**

- `async def upload_file(file_path: str) -> File`:
  Uploads a file to the T2G API.
  - `file_path`: The path to the file to upload.
- `async def create_file(name: str, source_hash: str) -> Dict`:
  Creates a file record and returns a presigned URL for uploading.
  - `name`: The name of the file.
  - `source_hash`: The SHA256 hash of the file's content.
- `async def find_files(ids: List[str] = None, source_hashes: List[str] = None) -> List[File]`:
  Finds files by their IDs or source hashes.
  - `ids` (optional): A list of file IDs to find.
  - `source_hashes` (optional): A list of source hashes to find.

### `T2GClient.job` -> `JobService`

The `JobService` handles job-related operations and is accessed via the `job` property of an active `T2GClient` instance.

**Methods:**

- `async def run_job(file_id: str, ontology_id: str = None, polling_interval: int = 5, timeout: int = 300) -> Job`:
  Submits a job and waits for its completion.
  - `file_id`: The ID of the file to process.
  - `ontology_id` (optional): The ID of the ontology to use.
  - `polling_interval` (optional): The interval in seconds to poll for job status.
  - `timeout` (optional): The timeout in seconds for the job to complete.
- `async def submit_job(file_id: str, ontology_id: str = None) -> Job`:
  Submits a job for processing.
  - `file_id`: The ID of the file to process.
  - `ontology_id` (optional): The ID of the ontology to use.
- `async def find_jobs(ids: List[str]) -> List[Job]`:
  Finds jobs by their IDs.
  - `ids`: A list of job IDs to find.
- `async def download_job_output(job_id: str, output_path: str = None) -> str`:
  Downloads the output of a completed job.
  - `job_id`: The ID of the job to download the output from.
  - `output_path` (optional): The path to save the output to.

### `T2GClient.ontology` -> `OntologyService`

The `OntologyService` handles ontology-related operations and is accessed via the `ontology` property of an active `T2GClient` instance.

**Methods:**

- `async def upload_ontology(ontology_path: str) -> Ontology`:
  Uploads an ontology file to the T2G API.
  - `ontology_path`: The path to the ontology file to upload.
- `async def create_ontology(name: str, source_hash: str) -> Dict`:
  Creates an ontology record and returns a presigned URL for uploading.
  - `name`: The name of the ontology.
  - `source_hash`: The SHA256 hash of the ontology file's content.
- `async def find_ontologies(ids: List[str] = None, source_hashes: List[str] = None) -> List[Ontology]`:
  Finds ontologies by their IDs or source hashes.
  - `ids` (optional): A list of ontology IDs to find.
  - `source_hashes` (optional): A list of source hashes to find.

### `T2GClient.neo4j` -> `Neo4jService`

The `Neo4jService` handles operations related to Neo4j and is accessed via the `neo4j` property of an active `T2GClient` instance.

**Methods:**

- `async def save_output_to_neo4j(file_path: str)`:
  Saves the output of a job (in CQL format) to a Neo4j database.
  - `file_path`: The path to the CQL file to save.

---

### Models

The SDK uses `pydantic` models to represent the data returned by the API.

- **`Job`**: Represents a job with its `id` and `status`.
- **`File`**: Represents a file with its `id`, `name`, `status`, and `created_at`.
- **`Ontology`**: Represents an ontology with its `id`, `name`, `status`, and `created_at`.
- **`JobStatus`**: An `Enum` for the status of a job (`PENDING`, `PROCESSING`, `SUCCEEDED`, `FAILED`).
- **`FileStatus`**: An `Enum` for the status of a file (`UPLOADED`, `PENDING`).
- **`OntologyStatus`**: An `Enum` for the status of an ontology (`UPLOADED`, `PENDING`).

## ⚙️ Configuration Details

The SDK uses `pydantic-settings` for configuration management. You can configure the client by passing arguments to its constructor, or by setting environment variables.

| Argument         | Environment Variable | Description                                      |
| ---------------- | -------------------- | ------------------------------------------------ |
| `api_key`        | `LETTRIA_API_KEY`    | **Required.** Your Lettria API key.              |
| `neo4j_uri`      | `NEO4J_URI`          | (Optional) The URI for your Neo4j instance.      |
| `neo4j_user`     | `NEO4J_USER`         | (Optional) The username for your Neo4j instance. |
| `neo4j_password` | `NEO4J_PASSWORD`     | (Optional) The password for your Neo4j instance. |

**Note:** The Neo4j configuration options (`neo4j_uri`, `neo4j_user`, `neo4j_password`) are only required if you set `save_to_neo4j=True` when calling `index_file`.

## 🚨 Error Handling

The SDK defines custom exceptions to handle API errors.

- `t2g_sdk.exceptions.T2GException`: The base exception for all API-related errors.
- `t2g_sdk.exceptions.APIError`: Raised for general API errors.
- `t2g_sdk.exceptions.AuthenticationError`: Raised for authentication-related errors (e.g., invalid API key).
- `t2g_sdk.exceptions.JobError`: Raised when a job fails.

It is recommended to wrap your API calls in a `try...except` block to handle these exceptions.

## 📂 Examples

You can find more examples in the [`examples/`](./examples/) directory. Each example includes a `README.md` with instructions on how to run it.

- [`index_file/`](./examples/index_file/README.md): A simple demonstration of how to index a file.
- [`simple-reporting/`](./examples/simple-reporting/README.md): An advanced example of how to generate a report from the indexed data.
- [`upload_file/`](./examples/upload_file/README.md): A basic example of how to upload a file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any feedback or suggestions.

## 📧 Contact

For any feedback, questions, or support, please reach out to us at [hello@lettria.com](mailto:hello@lettria.com).

## 📄 License

This SDK is licensed under the MIT License.
