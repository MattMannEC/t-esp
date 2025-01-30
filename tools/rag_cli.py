import sys
import os
import time

# Get the parent directory of the current file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from chroma_store import get_chroma_with_collection
from time import sleep

"""
Use this script to load the codes into vector database. 
Some of the pdfs are large and can cause out of memory error.
To avoid this i have seperated documents into large (over 7MB) and normal size.
When executing large documents, i have added a 30 second sleep between documents to allow GPU
to cool down.
"""

def load(file_path: str, progress: str):
    # Start timing the execution
    start_time = time.time()

    # Load the document
    loader = PyPDFLoader(file_path)
    print(f"Loading the document: {file_path}")
    data = loader.load()
    print(f"Document loaded: {file_path}")

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(data)

    # Initialize the vector store
    chroma_store = get_chroma_with_collection("codes_20250124", "localhost")

    # Adding documents in batches of 100 with progress tracking
    batch_size = 100
    total_chunks = len(all_splits)
    progress_intervals = [int(total_chunks * i / 10) for i in range(1, 11)]  # 10%, 20%, ..., 100%
    progress_index = 0

    print("Storing vectors...")
    for start in range(0, total_chunks, batch_size):
        end = min(start + batch_size, total_chunks)
        batch = all_splits[start:end]
        chroma_store.add_documents(documents=batch)  # Add the current batch

        # Track progress
        if progress_index < len(progress_intervals) and end >= progress_intervals[progress_index]:
            print(f"Progress: {((progress_index + 1) * 10)}% ({end}/{total_chunks} chunks) of document {progress}...")
            progress_index += 1

    # Print total execution time for this file
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Vectors stored for {file_path}. Execution time: {execution_time:.2f} seconds")
    return execution_time


# Define the folder path
# folder_path = "legifrance_codes"
folder_path = "large_documents"

# List all filenames ending with .pdf
pdf_files: list[str] = [file for file in os.listdir(folder_path) if file.endswith('.pdf')]

# Dictionary to store execution times for each file
execution_report = {}

# Process each PDF and track execution time
for f in range(0, len(pdf_files)):
    file_path = f"{folder_path}/{pdf_files[f]}"
    execution_time = load(file_path, f"{f+1} / {len(pdf_files)}")
    execution_report[pdf_files[f]] = execution_time
    sleep(30)

# Print summary report
print("\n=== Execution Time Report ===")
for file_name, exec_time in execution_report.items():
    print(f"{file_name}: {exec_time:.2f} seconds")
