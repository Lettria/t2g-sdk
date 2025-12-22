import asyncio
import logging
from google import genai
from google.genai import types as genai_types


async def main():

    file_name = "LOREAL_Rapport_Annuel_2024.pdf"
    doc_data = None
    with open(file_name, "rb") as f:
        doc_data = f.read()

    genai_client = genai.Client()

    prompt = """Convert this document in markdown."""
    parsed = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            genai_types.Part.from_bytes(
                data=doc_data,
                mime_type="application/pdf",
            ),
            prompt,
        ],
        config=genai_types.GenerateContentConfig(
            thinking_config=genai_types.ThinkingConfig(thinking_budget=128)
        ),
    )
    if parsed.text:
        with open(f"{file_name.rsplit('.', 1)[0]}.md", "w") as f:
            f.write(parsed.text)
        print(f"Parsed document saved to {file_name.rsplit('.', 1)[0]}.md")
    else:
        print("Failed to parse the document.")


if __name__ == "__main__":
    asyncio.run(main())
