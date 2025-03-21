import random
from typing import ClassVar

from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document

class CityRetriever(BaseRetriever):

    answers: ClassVar = [
        "Paris",
        "New York",
        "Helsinki",
    ]

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun):

        answer = random.sample(self.answers, 1)
        return [Document(page_content=str(answer[0]))]

def combine_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

