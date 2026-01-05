# Lettria's Text-to-Graph SDK 🚀

[![PyPI version](https://badge.fury.io/py/t2g-sdk.svg)](https://badge.fury.io/py/t2g-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to the official Python SDK for Lettria's Text-to-Graph (T2G) API! This SDK provides a convenient way to interact with the T2G API, allowing you to unlock the power of knowledge graphs from your text data directly within your Python applications.

## 🌟 Overview

Lettria's Text-to-Graph (T2G) technology transforms unstructured text into structured knowledge graphs. This SDK is designed to simplify the process of sending your data to the T2G API and retrieving the results, whether you are indexing a single document, a collection of files, or building complex graph system.

This SDK is built with developers in mind, providing a clean, asynchronous client to handle API requests efficiently.

## ✨ Features

- **Asynchronous Client**: Built with `asyncio` and `aiohttp` for high-performance, non-blocking API calls.
- **Simple Interface**: Easy-to-use methods for indexing files and managing jobs.
- **Data Validation**: Leverages `pydantic` for robust and reliable data modeling.
- **Neo4j Integration**: Directly save your graph data to a Neo4j instance.
- **Flexible Configuration**: Configure the SDK via environment variables or directly in your code.
- **Built-in Error Handling**: Gracefully handles API errors with custom exceptions.

## 📦 Installation

```bash
pip install t2g-sdk==1.0.0-rc.13
```

## 🚀 Getting Started

To start using the SDK, you will need an API key from Lettria.

To create an API key, please visit our preview instance [here](https://app.t2g-staging.lettria.net/).

Access to the API is managed by whitelisting. If you require access, please contact us at [hello@lettria.com](mailto:hello@lettria.com) to request whitelisting.

### Configuration

The SDK can be configured by setting the following environment variable:

- `LETTRIA_API_KEY`: Your Lettria API key.

Alternatively, you can pass this value directly to the `T2GClient` constructor.

### Quick Example: Building a graph

This example demonstrates how to build a graph from a local text file and save the resulting graph to Neo4j.

```python
import asyncio
from t2g_sdk.client import T2GClient
from t2g_sdk.exceptions import T2GException
from t2g_sdk.models import Job


async def main():
    async with T2GClient() as client:
        try:
            await client.build_graph(
                file_path="path/to/your/document.txt",
                ontology_path="path/to/your/ontology.ttl",
                output_path="path/to/your/output",
                save_to_neo4j=True,
            )
            print("🎉 Graph builded successfully")
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

- `async def build_graph(file_path: str, ontology_path: str = None, output_path: str = None, save_to_neo4j: bool = False) -> Job`:
  Build a knowledge graph from a file by uploading it, running a job, and downloading the output.
  - `file_path`: Path to the file to process.
  - `ontology_path` (optional): Path to an ontology file (e.g., `.ttl`).
  - `output_path` (optional): The path to save the output to. If not provided, a default path will be used.
  - `save_to_neo4j` (optional): If `True`, saves the result to your configured Neo4j instance.

## ⚙️ Configuration Details

The SDK uses `pydantic-settings` for configuration management. You can configure the client by passing arguments to its constructor, or by setting environment variables.

| Argument         | Environment Variable | Description                                      |
| ---------------- | -------------------- | ------------------------------------------------ |
| `api_key`        | `LETTRIA_API_KEY`    | **Required.** Your Lettria API key.              |
| `neo4j_uri`      | `NEO4J_URI`          | (Optional) The URI for your Neo4j instance.      |
| `neo4j_user`     | `NEO4J_USER`         | (Optional) The username for your Neo4j instance. |
| `neo4j_password` | `NEO4J_PASSWORD`     | (Optional) The password for your Neo4j instance. |

**Note:** The Neo4j configuration options (`neo4j_uri`, `neo4j_user`, `neo4j_password`) are only required if you set `save_to_neo4j=True` when calling `build_graph`.

## 📂 Examples

You can find more examples in the [`examples/`](./examples/) directory. Each example includes a `README.md` with instructions on how to run it.

- [`build_graph/`](./examples/build_graph/README.md): A simple demonstration of how to build a knowledge graph from a file.
- [`simple-reporting/`](./examples/simple-reporting/README.md): An advanced example of how to generate a report from the produced knowledge graph data.
- [`upload_ontology/`](./examples/upload_ontology/README.md): A basic example of how to upload an ontology file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any feedback or suggestions.

## 📧 Contact

For any feedback, questions, or support, please reach out to us at [hello@lettria.com](mailto:hello@lettria.com).

## 📄 License

This SDK is licensed under the MIT License.
