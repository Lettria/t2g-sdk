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
pip install t2g-sdk==1.0.0rc6
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

- `async def index_file(file_path: str, ontology_path: str = None, save_to_neo_4j: bool = False) -> Job`:
  Indexes a file and returns a `Job` object with the results.
  - `file_path`: Path to the file to index.
  - `ontology_path` (optional): Path to an ontology file (e.g., `.ttl`).
  - `save_to_neo4j` (optional): If `True`, saves the result to your configured Neo4j instance.

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

You can find more examples in the [`examples/`](./examples/) directory, including:

- `index_file/`: A simple demonstration of how to index a file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any feedback or suggestions.

## 📧 Contact

For any feedback, questions, or support, please reach out to us at [hello@lettria.com](mailto:hello@lettria.com).

## 📄 License

This SDK is licensed under the MIT License.
