# Simple Reporting Example

This example demonstrates how to use the T2G SDK to build a simple reporting application. The application indexes a PDF document, creates a knowledge graph, and then uses the graph to generate a report based on a user's query.

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- An API key for Gemini

## Setup

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_folder>/examples/simple-reporting
   ```

2. **Set up the environment:**

   - Create a virtual environment:

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

   - Install the required Python packages:

     ```bash
     pip install -r requirements.txt
     ```

   - Configure T2G SDK environment variables. See the main [README.md](../../README.md#configuration) for more details.

   - Set you Gemini API KEY
     ```bash
     export GEMINI_API_KEY=<your_api_key>
     ```

3. **Start the services:**

   Use Docker Compose to start the required services (Neo4j, Qdrant, and TEI):

   ```bash
   docker compose up -d
   ```

## Workflow

The application workflow consists of three main steps:

1. **Convert PDF to Markdown:**

   The `to_markdown.py` script converts the provided PDF document (`LOREAL_Rapport_Annuel_2024.pdf`) into a Markdown file.

   ```bash
   python to_markdown.py
   ```

   This will create a file named `LOREAL_Rapport_Annuel_2024.md`.

2. **Index the document:**

   The `index.py` script takes the Markdown file, processes it with the T2G SDK, and stores the resulting knowledge graph in Neo4j.

   ```bash
   python index.py LOREAL_Rapport_Annuel_2024.md
   ```

3. **Generate a report:**

   The `reporting.py` script allows you to query the knowledge graph and generate a report. You can provide a query as a command-line argument.

   ```bash
   python reporting.py "your query here"
   ```

   For example:

   ```bash
   python reporting.py "main activities"
   ```

   The script will use the query to retrieve relevant information from the knowledge graph, generate a report using a language model, and save the report to a Markdown file named `report_<your_query>.md`.

## Cleaning up

To stop and remove the Docker containers, run:

```bash
docker-compose down
```
