from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field


class Question(BaseModel):
    """
    This class describes the data schema for a question-answer pair.

    Used by JsonOutputParser to create the format specification for the prompt
    and to parse the output provided by the LLM.
    """

    question: str = Field(description="Original question")
    answer: str = Field(description="Answer to the question")
