# langchain-pdf-loaders


## Intro

LangChain is a commonly used toolbox for constructing RAG applications.

It provides numerous Document loaders, including PDF loaders.

The different loaders documented
[here](https://python.langchain.com/docs/integrations/document_loaders/#pdfs).

Most of the loaders are very simple to use. You simply need to install the
required packages and then write code such as this:

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(pdf)

docs = loader.load()
```

When given a PDF filename, a loader will create a list of
[Document-objects](https://python.langchain.com/api_reference/core/documents/langchain_core.documents.base.Document.html).
These represent any kind of document and its corresponding metadata.
Some PDF loaders might provide more documents that others.


## Testing different loaders with langchain-pdf-loaders.py

Different PDF loaders can provide varying results based on the type of PDF you're
loading. To help out on the process of choosing a document loader we have created a script
that you can use to test out different document loaders.

This script is called `langchain-pdf-loaders.py`. Here is it's help page:

```console
$ python langchain-pdf-loaders.py --help
usage: langchain-pdf-loaders.py [-h] [-S SEARCH] [--loaders LOADERS] [--print-search] [--print-page-contents]
                                [--example {1,2}] [--json JSON]
                                [PDF ...]

positional arguments:
  PDF                   PDFs to load (if it is an URL, PDF will be downloaded)

options:
  -h, --help            show this help message and exit
  -S SEARCH, --search SEARCH
                        A phrase that will searched from the documents. Can be a Python regular expression.
  --loaders LOADERS     Loader to test. Comma separated list of these possible loaders: pdfminer, pdfplumber,
                        pymupdf, pypdf, pypdfium2, unstructured
  --print-search        Print the page that has the found search phrase.
  --print-page-contents
                        Print Document page_content after loading them.
  --example {1,2}       Number of the example that will be used, if no PDFs are provided.
  --json JSON           File where JSON output should be written.
```

All of the document loading is handled by simple functions in the script,
so copying the relevant parts to your own code should a simple task.


### Installation

You can install an environment with all of the tested loaders by using the
included environment.yml.

Install the environment with:
```sh
mamba env create -f environment.yml
```
or
```sh
conda env create -f environment.yml
```


### Checking the examples

You can run analysis for the example PDFs (downloaded from LangChain's
repository)
with:

```sh
python langchain-pdf-loaders.py
```

To run the second example, run
```sh
python langchain-pdf-loaders.py --example 2
```


### Running with your own PDF

You can provide the tool with your own PDF files. If the PDF name is an URL,
PDF will be downloaded first
```sh
python langchain-pdf-loaders.py my_pdf.pdf
```


### Searching a phrase from a PDF

Often you'll want to search for a pharse from the document to verify that
the document has been loaded correctly. You can do this by using the
`-S/--search`-option:

```sh
python langchain-pdf-loaders.py my_pdf.pdf --search "my phrase"
```


### Printing document contents that match the search

You can print the document pages that match the search phrase by setting
the `--print-search`-option.

```sh
python langchain-pdf-loaders.py my_pdf.pdf --search "my phrase" --print-search
```


### Printing all pages

You can print out all pages by using the `--print-page-contents`-option.

```sh
python langchain-pdf-loaders.py my_pdf.pdf --print-page-contents
```


### Choosing loaders

You can limit the loaders you want to use by choosing them via
`--loaders`-option.

```sh
python langchain-pdf-loaders.py my_pdf.pdf --loaders pymupdf,unstructured
```


### Printing JSON output

If you want to view the output in more detail, you can use the
`--json`-option and the code will write a JSON file with all of the loaded
contents.

```sh
python langchain-pdf-loaders.py my_pdf.pdf --json my_pdf.json
```
