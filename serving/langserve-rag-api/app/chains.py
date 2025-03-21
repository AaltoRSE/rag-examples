import os

import langchain

langchain.verbose = True
langchain.debug = True

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser

from app.retrievers import CityRetriever, combine_docs
from app.prompts import salesman_prompt, json_prompt, json_limerick_prompt, llm_prompt
from app.schema import Question
from app.llms import get_llm

json_parser = JsonOutputParser(pydantic_object=Question)


retriever = CityRetriever()

llm = get_llm(streaming=True)
json_llm = get_llm(streaming=False)

llm_chain = (
    llm
    | StrOutputParser()
)

json_chain = (
    json_prompt.partial(**{"answer_format": json_parser.get_format_instructions()})
    | json_llm
    | json_parser
)

json_limerick_chain = (
    json_limerick_prompt.partial(**{"answer_format": json_parser.get_format_instructions()})
    | json_llm
    | json_parser
)

salesman_chain = (
    {"context": retriever | combine_docs, "question": RunnablePassthrough()}
    | salesman_prompt
    | llm
    | StrOutputParser()
)

# Uncomment if you wnat to test llm during server reload
#rag_chain.invoke("Where should I travel?")
