import pprint
import sys
import os
import time
from typing import List

# Get the parent directory of the current file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to sys.path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from chroma_store import get_chroma_with_collection
from time import sleep

from langchain_core.documents import Document

"""
Use this script to load the codes into vector database. 
Some of the pdfs are large and can cause out of memory error.
To avoid this i have seperated documents into large (over 7MB) and normal size.
When executing large documents, i have added a 30 second sleep between documents to allow GPU
to cool down.

Need to have codes juridiques stored locally in a dir in pdf format
"""


def load(file_path: str, progress: str):
    # Start timing the execution
    start_time = time.time()

    # Load the document
    loader = PyPDFLoader(file_path)
    print(f"Loading the document: {file_path}")
    data: List[Document] = loader.load()

    print(f"Document loaded: {file_path}")

    # Split the document into chunks

    text_splitter = RecursiveCharacterTextSplitter(
        separators=[r"\nArticle", r"\n\s*\n", r"\n", r"\s"],
        is_separator_regex=True,
        keep_separator="start",
        chunk_size=800,
        chunk_overlap=200,
    )

    all_splits = text_splitter.split_documents(data)

    # Initialize the vector store
    chroma_store = get_chroma_with_collection("route_et_travail_20250213")
    # Article L1132-1
    # Adding documents in batches of 100 with progress tracking
    batch_size = 100
    total_chunks = len(all_splits)
    progress_intervals = [
        int(total_chunks * i / 10) for i in range(1, 11)
    ]  # 10%, 20%, ..., 100%
    progress_index = 0

    print("Storing vectors...")
    print_batch = True
    for start in range(0, total_chunks, batch_size):

        end = min(start + batch_size, total_chunks)
        batch = all_splits[start:end]
        if print_batch:
            pprint.pprint(batch)

        print_batch = False
        chroma_store.add_documents(documents=batch)  # Add the current batch

        # Track progress
        if (
            progress_index < len(progress_intervals)
            and end >= progress_intervals[progress_index]
        ):
            print(
                f"Progress: {((progress_index + 1) * 10)}% ({end}/{total_chunks} chunks) of document {progress}..."
            )
            progress_index += 1

    # Print total execution time for this file
    end_time = time.time()
    execution_time = end_time - start_time
    print(
        f"Vectors stored for {file_path}. Execution time: {execution_time:.2f} seconds"
    )
    return execution_time


def load_from_dir(dir: str, sleep_val: int):
    # List all filenames ending with .pdf
    pdf_files: list[str] = [file for file in os.listdir(dir) if file.endswith(".pdf")]

    # Dictionary to store execution times for each file
    execution_report = {}

    # Process each PDF and track execution time
    for f in range(0, len(pdf_files)):
        if "code_de_la_route".lower() in pdf_files[f].lower():
            file_path = f"{dir}/{pdf_files[f]}"
            execution_time = load(file_path, f"{f+1} / {len(pdf_files)}")
            execution_report[pdf_files[f]] = execution_time
            sleep(sleep_val)  # Free VRAM

    # Print summary report
    print("\n=== Execution Time Report ===")
    for file_name, exec_time in execution_report.items():
        print(f"{file_name}: {exec_time:.2f} seconds")


# import chromadb
# from chromadb.api import ClientAPI
# from classes.config import app_config

# chroma_client: ClientAPI = chromadb.HttpClient(
#     host=app_config.CHROMA_SERVICE_NAME, port=app_config.CHROMA_PORT
# )
# print(chroma_client.list_collections())
load_from_dir("tools/documents", 10)
# load_from_dir("large_documents", 30)
# load_from_dir("documents", 10)
# \\n\s*Article\s+[A-Za-z]{0,3}\s*\d{0,6}(-\d{0,3})?
