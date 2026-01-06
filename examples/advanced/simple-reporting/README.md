# Simple Reporting Example 📊

This guide shows how to build a simple reporting app with the T2G SDK. You'll index a PDF, create a knowledge graph, and generate reports from it.

## Quick Start 🚀

1.  **Setup Environment**:

    - Requires Docker, Docker Compose, and Python 3.8+. 🐳🐍
    - Copy `template.env` to `.env` and fill your credentials.

    ```bash
    cp template.env .env
    ```

2.  **Install Dependencies & Start Services**:

    ```bash
    pip install -r requirements.txt
    docker compose up -d
    ```

3.  **Run the Workflow**:

    - **Convert PDF to Markdown**:

      ```bash
      python pdf_to_markdown.py assets/LOREAL_Rapport_Annuel_2024.pdf
      ```

    - **Index the Document**:

      ```bash
      python index.py assets/LOREAL_Rapport_Annuel_2024.md
      ```

    - **Generate a Report**:
      ```bash
      python report.py "What are the main activities of L'Oréal?"
      ```

## Cleaning Up 🧹

When you're done, stop and remove the Docker containers:

```bash
docker compose down
```
