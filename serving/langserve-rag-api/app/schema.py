from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

class Question(BaseModel):
    question: str = Field(description="original question")
    answer: str = Field(description="answer to the question")
