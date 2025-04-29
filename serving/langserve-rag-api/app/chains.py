"""
This file defines various LLM chains. Each chain takes input, fills a prompt
template and processes the prompt with an LLM.

Included chains:

- llm_chain: A generic LLM that takes input and gives it to an LLM.
- json_chain: Chain that asks LLM to provide the answer in JSON format and
  parses output to that format.
- json_limerick_chain: Same as json_chain, but answers are produced as
  limericks.
- salesman_chain: An LLM RAG chain that uses a retriever to find relevant
  context to the input. In this case retriever is a custom retriever that
  picks a random city name. Input and context are both provided to the prompt,
  that tells LLM to sell a holiday to the given city no matter the input.
"""

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


# JSON parser that fills prompt with relevant instructions and parses output
json_parser = JsonOutputParser(pydantic_object=Question)

# Retriever that gives a random city name
retriever = CityRetriever()

# LLM chat endpoints. JSON LLMs output looks better when it is not streamed
llm = get_llm(streaming=True)
json_llm = get_llm(streaming=False)


llm_chain = llm | StrOutputParser()

json_chain = (
    json_prompt.partial(**{"answer_format": json_parser.get_format_instructions()})
    | json_llm
    | json_parser
)

json_limerick_chain = (
    json_limerick_prompt.partial(
        **{"answer_format": json_parser.get_format_instructions()}
    )
    | json_llm
    | json_parser
)

salesman_chain = (
    {"context": retriever | combine_docs, "question": RunnablePassthrough()}
    | salesman_prompt
    | llm
    | StrOutputParser()
)
