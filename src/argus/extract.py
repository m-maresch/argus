from typing import Any, Dict, List
from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


class ExtractionResult(BaseModel):
    inferred_fields: List[str] = Field(
        description="The list of snake_case keys inferred from the user's implicit request (e.g., ['title', 'description', 'location']).",
        examples=[["title", "description", "location"]],
    )
    records: List[Dict[str, Any]] = Field(
        description="List of extracted records. Each record must use the exact keys listed in 'inferred_fields'."
    )


EXTRACTION_INSTRUCTIONS = """
You are an expert data extraction engine.
INSTRUCTIONS:
1. Analyze the user's task to determine what data attributes they implicitly want to collect.
2. Define these attributes as snake_case strings in 'inferred_fields'.
3. Parse the provided result, extract all relevant items, and map them into dictionaries inside the 'records' list using those exact inferred keys.
"""


def extract(user_prompt, result):
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite").with_structured_output(
        ExtractionResult
    )

    extraction_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                EXTRACTION_INSTRUCTIONS,
            ),
            (
                "human",
                "User's Task: {task}\n\n--- RESULT ---\n{result}",
            ),
        ]
    )

    chain = extraction_prompt | llm

    extracted = chain.invoke(
        {
            "task": user_prompt,
            "result": result,
        }
    )
    return extracted
