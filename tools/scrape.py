import sys
import os
import time

# Get the parent directory of the current file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
import requests
from bs4 import BeautifulSoup
from tools.logger import logger
import re
"""
Scrapes all code pdfs from french government website and saves as local pdfs.
"""
# URL of the Légifrance page containing the codes
url = 'https://www.legifrance.gouv.fr/liste/code?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF&page=1#code'

# Create a directory to save the downloaded PDFs
download_dir = 'legifrance_codes'
os.makedirs(download_dir, exist_ok=True)

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
# Find all links to the code documents
code_links = soup.find_all('a')  # Adjust the class name based on the actual HTML structure

download_links = [l for l in code_links if l.get("href") and "download/pdf" in l["href"]]

if len(download_links) != 77:
    logger.error(f"Did not find 77 download links, found {len(download_links)}")

def get_title(a_tag) -> str:
    return a_tag["href"].split('title=')[1]

def encode_as_filename(title):
    # Replace spaces with underscores
    sanitized = title.replace(" ", "_")
    
    # Remove or replace invalid characters for file names
    sanitized = re.sub(r"[\/:*?\"<>|']", "", sanitized)  # Remove invalid characters
    
    return sanitized

# Base URL for constructing the full download link
base_url = 'https://www.legifrance.gouv.fr'
logger.info(f"Found {len(download_links) } to download")
downloaded = 0
# Iterate through the found links and download the PDFs
for link in download_links:

    download_url = base_url + link['href']  # Construct the full URL to the code page
    pdf_response = requests.get(download_url)
    pdf_response.raise_for_status()
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(pdf_response.content, 'html.parser')
    file_links = soup.find_all('a')
    file_download_links = [l for l in file_links if l.get("href") and "download/file/pdf" in l["href"]]

    # Save the PDF to the download directory
    pdf_path = os.path.join(download_dir, f'{encode_as_filename(get_title(link))}.pdf')

    file_response = requests.get(base_url + file_download_links[0]["href"])
    file_response.raise_for_status()
    with open(pdf_path, 'wb') as pdf_file:
        n = 0
        n = pdf_file.write(file_response.content)
        if n > 0:
            downloaded += 1
            print(f'Downloaded: {get_title(link)}')


logger.info(f"Downloaded {downloaded} pdfs")