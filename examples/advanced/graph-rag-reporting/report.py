from dotenv import load_dotenv
import asyncio
import sys
from simple_graph_retriever.client import GraphRetrievalClient
from simple_graph_retriever.models import RetrievalConfig, RetrievalResult
from google import genai
from google.genai import types as genai_types
from utils import wait_for_embedder, wait_for_neo4j

load_dotenv()


async def retrieve_graph_data(query: str) -> RetrievalResult | None:
    """
    Retrieves graph data based on a query.
    """
    await wait_for_neo4j(timeout=10)
    await wait_for_embedder(timeout=10)
    retrieval_client = GraphRetrievalClient()
    data = retrieval_client.retrieve_graph(
        query=query,
        config=RetrievalConfig(
            include_scores=True,
            community_score_drop_off_pct=0.3,
            chunk_score_drop_off_pct=0.3,
        ),
    )
    return data


async def generate_report_from_data(query: str, data: RetrievalResult) -> str | None:
    """
    Generates a report from existing graph data.
    """
    genai_client = genai.Client()
    report_prompt = f"""
        Provide a report summarizing the following information about {query}:
        {data.to_markdown()}

        The report should include key details and insights derived from the data.
        Be concise and informative.
        Only mention information that is related to {query} directly or indirectly.
        Use tables when relevant to present data clearly.
    """
    report = genai_client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=report_prompt,
        config=genai_types.GenerateContentConfig(
            thinking_config=genai_types.ThinkingConfig(thinking_budget=128)
        ),
    )
    return report.text if report else None


async def generate_report(query: str) -> tuple[RetrievalResult | None, str | None]:
    """
    Generates a report by retrieving graph data and using a generative AI model.
    """
    data = await retrieve_graph_data(query)
    if not data:
        return None, None
    report_text = await generate_report_from_data(query, data)
    return data, report_text


async def main(script_input: str):
    """
    Main function to run the report generation from the command line.
    """
    data, report_text = await generate_report(script_input)

    if not data:
        print("No data found.")
        return

    print(f"Found nodes: {len(data.nodes)}")
    print(f"Found relationships: {len(data.relationships)}")
    print(" ")

    if report_text:
        report_path = f"./output/report_{script_input.lower().replace(' ', '_')}.md"
        with open(report_path, "w") as f:
            f.write(f"# Report on {script_input}\n\n")
            f.write(report_text)
        print(f"Report generated and saved successfully at {report_path}")
    else:
        print("No report generated because the response was empty.")


if __name__ == "__main__":
    input_query = sys.argv[1] if len(sys.argv) > 1 else "Money KPIs"
    asyncio.run(main(input_query))
