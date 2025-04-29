from app.utils import read_secrets
from langchain_openai import ChatOpenAI


def get_llm(
    secrets_file: str = "./secrets/api_keys.env", streaming: bool = False
) -> ChatOpenAI:
    """This function creates a LangChain LLM chat that will be called by the LLM chains.

    Args:
        secrets_file (str): Path to the secrets file that contains the secrets needed to
            contact an OpenAI compatible endpoint. Default is ./secrets/api_keys.env.
        streaming (bool): Whether output from the LLM should be streamed or not.
    Returns:
        ChatOpenAI: LLM endpoint.
    """

    secrets = read_secrets(secrets_file)

    assert len(secrets["OPENAI_API_KEY"]) > 0, "OpenAI API key is missing from secrets"
    assert (
        len(secrets["OPENAI_BASE_URL"]) > 0
    ), "OpenAI Base URL is missing from secrets"
    assert len(secrets["OPENAI_MODEL"]) > 0, "OpenAI Model is missing from secrets"

    if len(secrets.get("AZURE_AUTH", "")) > 0:

        llm = ChatOpenAI(
            temperature=0.1,
            base_url=secrets["OPENAI_BASE_URL"],
            api_key=secrets["OPENAI_API_KEY"],  # pyright: ignore
            default_headers={
                "Ocp-Apim-Subscription-Key": secrets["OPENAI_API_KEY"],
            },
        )
    else:

        llm = ChatOpenAI(
            model=secrets["OPENAI_MODEL"],
            temperature=0.1,
            api_key=secrets["OPENAI_API_KEY"],
            base_url=secrets["OPENAI_BASE_URL"],
        )

    llm.disable_streaming = not streaming

    return llm
