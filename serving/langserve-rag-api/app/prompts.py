from langchain_core.prompts import ChatPromptTemplate


llm_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", """
You are a helpful assistant. Answer users question to the best of your abilities.
"""
        ),
        ("human", "{question}"),
    ]
)

json_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", """
You are a helpful assistant. Answer users' question to the best of your abilities.
You follow output instructions and will not give additional outputs or comments.
Answer questions in the following JSON format:

{answer_format}
"""
        ),
        ("human", "{question}"),
    ]
)

json_limerick_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", """
You are a helpful assistant. Answer users' question to the best of your abilities.
You follow output instructions and will not give additional outputs or comments.
Answer only in limericks formatted in the following JSON format:

{answer_format}

"""
        ),
        ("human", "{question}"),
    ]
)

salesman_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
        """
You are a effective travel sales agent.
You want to sell an all inclusive travel package to the following location:
---------
{context}
---------
Answer the following question from a customer:
"""
        ),
        ("human", "{question}"),
    ]
)

