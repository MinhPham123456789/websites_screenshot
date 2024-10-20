import sys
import os
from urllib.parse import urlparse

def check_and_create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")
    image_path = f'{directory_path}/images'
    if not os.path.exists(image_path):
        os.makedirs(image_path)
        print(f"Directory '{image_path}' created.")
    else:
        print(f"Directory '{image_path}' already exists.")
    return directory_path, image_path

def read_file_to_array(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Strip newline characters from each line
            lines = [line.strip() for line in lines]
            return lines

    except FileNotFoundError:
        print("The file was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def get_url_path_tail(url):
    # Parse the URL
    parsed_url = urlparse(url)
    # Extract components
    scheme = parsed_url.scheme          # e.g., 'https'
    netloc = parsed_url.netloc          # e.g., 'www.example.com'
    path = parsed_url.path              # e.g., '/path/to/resource'
    params = parsed_url.params          # e.g., '' (empty in this case)
    query = parsed_url.query            # e.g., 'query1=value1&query2=value2'
    fragment = parsed_url.fragment      # e.g., '' (empty in this case)
    path_tail = path.split('/')[-1]     # get path tail
    return f'{path_tail}'

def get_absolute_path(path):
    return os.path.abspath(path)