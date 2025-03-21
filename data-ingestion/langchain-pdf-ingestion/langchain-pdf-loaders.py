#!/usr/bin/env python
# coding=utf-8

import os
import re
import sys
import json
import time
import argparse
from mimetypes import guess_type
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import urlopen
from collections import defaultdict

import langchain


EXAMPLE_PDFS = [
    "https://github.com/langchain-ai/langchain/blob/master/libs/community/tests/integration_tests/examples/layout-parser-paper.pdf?raw=true",
    "https://github.com/langchain-ai/langchain/blob/master/docs/docs/example_data/nke-10k-2023.pdf?raw=true",
]

EXAMPLE_PDF_SEARCHES = [
    r"There has been a surge of interest in creating open-source tools for document\s+image processing",
    "annual report",
]


def load_pdfminer(pdf):

    from langchain_community.document_loaders import PDFMinerLoader

    loader = PDFMinerLoader(pdf)

    docs = loader.load()

    return docs


def load_pdfplumber(pdf):

    from langchain_community.document_loaders import PDFPlumberLoader

    loader = PDFPlumberLoader(pdf)

    docs = loader.load()

    return docs


def load_pymupdf(pdf):

    from langchain_community.document_loaders import PyMuPDFLoader

    loader = PyMuPDFLoader(pdf)

    docs = loader.load()

    return docs


def load_pypdf(pdf):

    from langchain_community.document_loaders import PyPDFLoader

    loader = PyPDFLoader(pdf)

    docs = loader.load()

    return docs


def load_pypdfium2(pdf):

    from langchain_community.document_loaders import PyPDFium2Loader

    # Catch warnings from PyPDFium2

    loader = PyPDFium2Loader(pdf)

    docs = loader.load()

    return docs


def load_unstructured(pdf):

    from langchain_community.document_loaders import UnstructuredPDFLoader

    loader = UnstructuredPDFLoader(pdf)

    docs = loader.load()

    return docs


def download_pdf(url, filename):

    print(f"Downloading {filename} from {url}")
    try:
        with urlopen(url) as req:
            data = req.read()
    except HTTPError as e:
        print(f"\nCould not download:\n{url}\n\nError:\n{e}")
        sys.exit(1)
    with open(filename, "wb") as f:
        f.write(data)


def search_docs(docs, search):

    found_pages = []
    reg = re.compile(search)
    for i, doc in enumerate(docs):
        result = reg.search(doc.page_content)
        if result is not None:
            found_pages.append(i)

    return found_pages


def print_separator(before=1, after=1):

    print(before * "\n" + 60 * "=" + after * "\n")


if __name__ == "__main__":

    loader_funcs = dict(
        (loader_name.replace("load_", ""), loader_func)
        for loader_name, loader_func in locals().items()
        if loader_name.startswith("load_")
    )
    all_loaders = sorted(list(loader_funcs.keys()))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pdf_urls",
        metavar="PDF",
        default=[],
        nargs="*",
        type=str,
        help="PDFs to load (if it is an URL, PDF will be downloaded)",
    )
    parser.add_argument(
        "-S",
        "--search",
        default=[""],
        type=str,
        nargs=1,
        help="A phrase that will searched from the documents. Can be a Python regular expression.",
    )
    parser.add_argument(
        "--loaders",
        default=[",".join(all_loaders)],
        nargs=1,
        type=str,
        help=f"Loader to test. Comma separated list of these possible loaders: {', '.join(all_loaders)}",
    )
    parser.add_argument(
        "--print-search",
        action="store_true",
        default=False,
        help=f"Print the page that has the found search phrase.",
    )
    parser.add_argument(
        "--print-page-contents",
        action="store_true",
        default=False,
        help=f"Print Document page_content after loading them.",
    )
    parser.add_argument(
        "--example",
        choices=[1, 2],
        default=1,
        type=int,
        help=f"Number of the example that will be used, if no PDFs are provided.",
    )
    parser.add_argument(
        "--json",
        default=[""],
        nargs=1,
        type=str,
        help=f"File where JSON output should be written.",
    )

    args = parser.parse_args()

    pdf_urls = args.pdf_urls
    search = args.search[0]

    if len(args.pdf_urls) == 0:
        print(f"No PDFs given. Using example case number {args.example}.")
        pdf_urls.append(EXAMPLE_PDFS[args.example - 1])
        if len(search) == 0:
            search = EXAMPLE_PDF_SEARCHES[args.example - 1]

    pdfs = []
    for pdf_url in pdf_urls:
        parsed_url = urlparse(pdf_url)
        pdf_name = parsed_url.path
        if not os.path.isfile(pdf_name):
            pdf_name = os.path.basename(pdf_name)
        if not os.path.isfile(pdf_name) and len(parsed_url.scheme) > 0:
            download_pdf(pdf_url, pdf_name)
        if not os.path.isfile(pdf_name):
            print(f"\nCould not find or download PDF:\n{pdf_url}")
            sys.exit(1)
        if not guess_type(pdf_name)[0] == "application/pdf":
            print(f"\nFile does not look like a PDF:\n{pdf_name}")
            sys.exit(1)
        pdfs.append(pdf_name)

    loaders = args.loaders[0].split(",")

    output_json = defaultdict(lambda: defaultdict(list))

    for pdf in pdfs:

        for loader in loaders:

            print_separator()

            print(f"Loaded PDF: {pdf}")
            print(f"Loader: {loader}")

            if loader not in loader_funcs:
                print(f"Loader {loader} is unknown! Available loaders: {all_loaders}")
                sys.exit(1)

            t1 = time.time()
            docs = loader_funcs[loader](pdf)
            t2 = time.time()

            print(f"Time taken: {t2-t1:.2f} seconds")

            print(f"Number of Documents created: {len(docs)}")

            if len(search) > 0:
                found_pages = search_docs(docs, search)
                search_found = len(found_pages) > 0
                print(f"Searched phrase found: {search_found}")

                if search_found and args.print_search:
                    for found_page in found_pages:
                        print_separator(before=1, after=0)
                        print(f"Found the searched phrase in page {found_page}:")
                        print_separator(before=0, after=1)
                        print(docs[found_page].page_content)

            for i, doc in enumerate(docs, start=1):

                if args.print_page_contents:
                    print(f"Document number {i} contents:\n")
                    print_separator()
                    print(doc.page_content)

                output_json[pdf][loader].append(
                    {
                        "document": pdf,
                        "document_number": i,
                        "loader": loader,
                        "page_content": doc.page_content,
                        "metadata": doc.metadata,
                    }
                )

    if len(args.json[0]) > 0:
        print_separator()
        with open(args.json[0], "w") as f:
            f.write(json.dumps(output_json, sort_keys=True, indent=4))
        print(f"JSON output written to {args.json[0]}\n")
