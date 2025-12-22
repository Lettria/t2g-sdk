import asyncio
import json
import logging
import sys
from t2g_sdk.client import T2GClient
from t2g_sdk.exceptions import T2GException
from t2g_sdk.models import Job
from simple_graph_retriever.client import GraphRetrievalClient
from simple_graph_retriever.models import RetrievalConfig
from google import genai
from google.genai import types as genai_types


async def main(script_input: str):
    genai_client = genai.Client()
    retrieval_client = GraphRetrievalClient()
    data = retrieval_client.retrieve_graph(
        query=script_input,
        config=RetrievalConfig(
            community_score_drop_off_pct=0.3, chunk_score_drop_off_pct=0.3
        ),
    )
    if not data:
        print("No data found.")
        return

    print(
        "Founded nodes:",
        len(data.nodes),
    )
    print(
        "Founded relationships:",
        len(data.relationships),
    )
    report_prompt = f"""
        Provide a report summarizing the following information about {script_input}:
        {data.model_dump_json(indent=2)}

        The report should include key details and insights derived from the data.
        Be concise and informative.
        Only mention informations that are related to {script_input} directly or indirectly.
    """

    report = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=report_prompt,
        config=genai_types.GenerateContentConfig(
            thinking_config=genai_types.ThinkingConfig(thinking_budget=128)
        ),
    )
    if report.text:
        with open(f"report_{script_input}.md", "w") as f:
            f.write(f"# Report on {script_input}\n\n")
            f.write(report.text)


if __name__ == "__main__":
    script_input = sys.argv[1] if len(sys.argv) > 1 else "battles"
    asyncio.run(main(script_input))
