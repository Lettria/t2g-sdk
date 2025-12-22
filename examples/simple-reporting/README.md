# Simple Reporting Example

This example demonstrates a more advanced use case where a file is indexed, and then a report is generated based on the retrieved graph data.

This example relies on the `simple_graph_retriever` and `google-generativeai` packages.

## How to Run

1.  **Set up your environment:**
    Make sure you have the required environment variables set for the `T2GClient`. See the main [README.md](../../README.md#configuration) for more details.
    You will also need to configure the `simple_graph_retriever` and `google-generativeai` clients.

2.  **Install dependencies:**

    ```bash
    pip install simple_graph_retriever google-generativeai
    ```

3.  **Index the data:**
    First, you need to index the `napoleon_wikipedia.txt` file.

    ```bash
    python index.py
    ```

4.  **Generate a report:**
    After the indexing is complete, you can generate a report. You can pass a query as an argument to the script.
    ```bash
    python reporting.py "Battles"
    ```
    This will create a `report_Napoleon.md` file in the same directory.
