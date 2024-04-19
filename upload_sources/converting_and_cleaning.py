#!/usr/bin/env python

import os
import re
import time
import shutil
import zipfile
import numpy as np
from pathlib import Path
from xml.etree import ElementTree as ET

from utils.QueueManager import QueueManager

datasource = 'datasource'
target_dir = 'cleaning'
ignore_list = 'settings/ignore_list.txt'

def error(msg: str, rc: int) -> int:
    """ Method: for displaying message and returning error code """
    print("Error: {}".format(msg))
    return rc

# Create a list of all the ignored files
def create_blacklist(ignore_file: str) -> list:
    ignore_items = []
    if os.path.exists(ignore_file):
        fp = open(ignore_file, 'r')
        ignore_items = [ f.replace('\n','') for f in fp.readlines() ]
        fp.close()
    return ignore_items

# Cleaning Process
def cleanup_data(input_string) -> str:
    data_cleanup = re.sub(r'\*\+\?\$\^\\',' ', input_string)
    data_cleanup = data_cleanup.replace(':',' ')
    data_cleanup = data_cleanup.replace('(','')
    data_cleanup = data_cleanup.replace(')','')
    data_cleanup = data_cleanup.replace('[','')
    data_cleanup = data_cleanup.replace(']','')
    data_cleanup = re.sub(r'\&', ' und ', data_cleanup)
    return data_cleanup

def find_docx_files(root_directory) -> list:
    """
    Finds and returns the paths of all .docx files in the specified directory and its subdirectories using list comprehension.
    :param root_directory: The directory to search in.
    :return: A list of paths to .docx files.
    """
    return [os.path.join(root, file) for root, dirs, files in os.walk(root_directory) for file in files if file.endswith(".docx")]

def read_docx(file_path) -> list:
    """
    Unzips a .docx file and reads the text content into a list of strings.

    Parameters:
    - file_path: Path to the .docx file

    Returns:
    - List of paragraphs as strings.
    """
    # The namespace is required to correctly traverse the XML tree.
    namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    paragraphs = []

    # Open the .docx file as a ZIP archive
    with zipfile.ZipFile(file_path) as docx:
        # Extract the XML content of the document
        with docx.open('word/document.xml') as document_xml:
            tree = ET.parse(document_xml)
            root = tree.getroot()
            # Find all paragraphs in the document
            for paragraph in root.iter(namespace + 'p'):
                texts = []
                for node in paragraph.iter(namespace + 't'):
                    iteration = cleanup_data(node.text.lower().rstrip())
                    if iteration:
                        # Check for nested data
                        for text in iteration.split(','):
                            texts.append(text.rstrip())
                if texts:
                    paragraphs.append(''.join(texts))
    return paragraphs

# Create the target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)
ignore_items = create_blacklist(ignore_list)
print(ignore_items)

# Transfer docx files to cleaning directory.
if os.path.exists(datasource):
    # Find all .docx files in the datasource directory
    for filepath in Path(datasource).rglob('*.docx'):
        if not filepath in ignore_items and os.path.isfile(filepath):
            # Construct the new filename by removing spaces
            new_filename = filepath.name.replace(' ', '')
            # Construct the full target path for the file
            target_path = os.path.join(target_dir, new_filename)
            # Copy the file to the target directory
            shutil.copy2(filepath, target_path)
            # print(f"Copied {filepath} to {target_path}")
else:
    error("Missing or unable to find {}".format(datasource), 1)

limit = 5
iteration = 0
docx_files = find_docx_files(target_dir)
for file_path in docx_files:
    iteration += 1
    if limit > iteration:
        print(file_path.lower())
        paragraphs = read_docx(file_path)
        print(paragraphs)
