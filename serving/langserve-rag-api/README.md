# langserve-rag-api

## Local installation

### Install micromamba

If you have acceess to
[mamba](https://mamba.readthedocs.io/en/latest/index.html) via some other
method (maybe you have already installed
[miniforge](https://github.com/conda-forge/miniforge)), you can skip
this step.

Otherwise, install micromamba following
[these instructions](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html#linux-and-macos).

For x86_64 Linux, this would be:

```sh
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
```

Once you have access to `mamba`/`micromamba`, create an environment with
```sh
bin/micromamba env create -f environment.yml
```
when using micromamba or with
```sh
mamba env create -f environment.yml
```
when using mamba.

### Setting up OpenAI API keys

This RAG example utilizes OpenAI compatible endpoint.
You can either launch your own or use any other compatible one.

You can set these via environment variables or through
`secrets/api_keys.env`.

The following keys need to be set:

- `OPENAI_API_KEY`: API key for the OpenAI endpoint
- `OPENAI_BASE_URL`: Base URL for the OpenAI endpoint.
- `OPENAI_MODEL`: Model to use from the OpenAI endpoint.

If you're using API keys from Aalto Azure OpenAI endpoint,
you need to set `AZURE_AUTH=1` as well.

Example secrets are shown in `secrets/example_api_keys.env`.

Remember that you should never share your API keys and you
should never commit your API keys to a repository.

## Starting up the server

Activate the environment with:

```sh
eval "$(./bin/micromamba shell hook -s posix)"
micromamba activate langserve-rag-api
```

When using `mamba`, use either
```sh
mamba activate langserve-rag-api
```
or
```sh
source activate langserve-rag-api
```

Now you can launch the server with
```sh
uvicorn app.server:app --host 0.0.0.0 --port 8080 --reload
```

This will start the server in the reload mode where changes
to the code base will reload the server automatically.

## Testing the different API endpoints

You can go to http://localhost:8080 with your browser to
see the available endpoints.

There are four llm endpoints that you can test out in
their respective playgrounds:

- http://localhost:8080/llm/playground - Direct access to the LLM.
- http://localhost:8080/json/playground/ - LLM that answers the question in a JSON format.
- http://localhost:8080/limerick/playground/ - LLM that answers the question with a limerick in a JSON format.
- http://localhost:8080/salesman/playground/ - LLM that uses RAG functionality to retrieve a random city from a list of three cities and tries to sell you a travel package to said city.


## Code structure

- `app/server.py` - This is the main server. It sets up the endpoints and starts the uvicorn app.
  Endpoints are set up by calling `add_routes`-function and they utilize runnable LLM chains from `app.chains`:
```python
add_routes(
    app,
    llm_chain,
    path='/llm'
)
```
- `app/chains.py` - This file contains the chains that can be run. Each chain consists of callables that are 
  called one after the other. User's question is given to a prompt, which is then passed to an LLM, which
  then produces output to a parser. In a case of a RAG setup, users question is first passed through a
  retriever that adds context to the prompt from retrieved documents:
```python
salesman_chain = (
    {"context": retriever | combine_docs, "question": RunnablePassthrough()}
    | salesman_prompt
    | llm
    | StrOutputParser()
)
```
- `app/llms.py` - This file specifies how the LLMs are created.
- `app/prompts.py` - This file contains prompts used by the LLM chains. Some prompts take only the
  question as input, but others take also retrieved context (in RAG situations) and some take additional
  instruction on how the output should be parsed.
- `app/retriever.py` - This file contains a custom retriever for the salesman RAG. This retriever could be
  any kind of retriever that takes a string of text (users question) and retrieves relevant documents.
  LangChain has plenty of existing retrievers for most use cases so creating a custom retriever is only
  relevant if those retrievers are not applicable for the data in question.
- `app/schema.py` - This file contains a desired answering schema for the questions. Useful when using
  parsers as they can automatically create answering instructions for the LLM based on the schema and
  then detect the answer from the output of the model.
- `app/utils.py` - This file contains utils that help with reading secrets.
