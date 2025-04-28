# rag-examples contribution guide

If you have existing examples related to RAG setups and would like to
add it to this repository, you can contribute them by creating a pull
request.

## Examples structure

1. Each example should be in a subfolder of the relevant topic. For example,
   example `langchain-pdf-ingestion`-example concerns data loading and
   preprocessing, so it is under `data-ingestion`-folder.
   If there is no folder that describes the topic of your example, you can
   create a new folder.
2. Each example should contain a `README.md` that describes the example
   and gives instructions on how to run the example.
3. If the example uses a Python environment, include a `requirements.txt` or
   `environment.yml` that can be used to create the environment needed by
   the example.
4. If the code is meant to be run in a cluster environment, please add an
   example job submission script.

We recommend that you run the example through a relevant linter so that the
code syntax follows the known best practices (e.g. using
[black](https://github.com/psf/black/) with Python code), but this is not
necessary for submission.
