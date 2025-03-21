from app.utils import read_secrets
from langchain_openai import ChatOpenAI


def get_llm(secrets_file=None, streaming=False):

    if not secrets_file:
        secrets_file = "./secrets/api_keys.env"

    secrets = read_secrets(secrets_file)

    assert len(secrets["OPENAI_API_KEY"]) > 0, "OpenAI API key is missing from secrets"
    assert len(secrets["OPENAI_BASE_URL"]) > 0, "OpenAI Base URL is missing from secrets"
    assert len(secrets["OPENAI_MODEL"]) > 0, "OpenAI Model is missing from secrets"

    if len(secrets.get('AZURE_AUTH', '')) > 0:

        llm = ChatOpenAI(
            temperature=0.1,
            base_url=secrets["OPENAI_BASE_URL"],
            api_key=secrets["OPENAI_API_KEY"], #pyright: ignore
            default_headers = {
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
