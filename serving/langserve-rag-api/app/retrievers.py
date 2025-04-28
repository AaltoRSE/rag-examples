import random
from typing import ClassVar

from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document


class CityRetriever(BaseRetriever):
    """
    This class implements a custom retriever for the salesman LLM chain.

    LangChain contains multiple existing retrievers that can be used to
    retriever relevant documents form a vector store. Most of the time these
    can be used instead of implementing custom solutions.

    This class however shows how a custom retriever can be implemented.

    This class returns a random city name with each call.
    """

    answers: ClassVar = [
        "Paris",
        "New York",
        "Helsinki",
    ]

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ):
        """This function returns Documents. In this case it returns a random
        city."""

        answer = random.sample(self.answers, 1)
        return [Document(page_content=str(answer[0]))]


def combine_docs(docs: list[Document]) -> str:
    """This function takes a list of Documents and combines them into a single
    string. Each document is separated by two newlines.

    Args:
        docs (list[Document]): List of documents

    Returns:
        str: Combined documents.
    """
    return "\n\n".join(doc.page_content for doc in docs)
