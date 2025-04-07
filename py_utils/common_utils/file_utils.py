import io
import json
import os
import pickle
import random
import re
import sys
import time
import zipfile
import base64
from io import BytesIO
from PIL import Image


def open_file_as_json(path):
    json_raw_file = open_file(path)
    try:
        json_file = json.loads(json_raw_file)
        return json_file
    except:
        print(f'Unable to parse {path} json file')
        return None


def open_file(path, mode='r', return_file=False):
    if not os.path.exists(path):
        print(f'File {path} not exist')
        return None

    with open(path, mode) as f:
        if return_file:
            return f
        return f.read()


def save_json_file(path, content, mode='w', increment=True):
    save_file(path, json.dumps(content), mode, increment)


def get_new_filename(file_name):
    file_name, extension = file_name.rsplit('.', 1)
    i = 1
    while True:
        new_name = f"{file_name}_{i}.{extension}"
        if not os.path.exists(new_name):
            return new_name
        i += 1


def save_file(path, content, mode='w', increment=True):
    try:
        if increment:
            if os.path.exists(path):
                path = get_new_filename(path)

        with open(path, mode) as file:
            file.write(content)
        print(f"Content saved to '{path}' successfully.")
    except IOError as e:
        print(f"Error saving content to '{path}': {e}")


def save_pickle_file(path, content, increment=False):
    if increment:
        if os.path.exists(path):
            path = get_new_filename(path)
    with open(path, 'wb') as file:
        pickle.dump(content, file)


def open_pickle_file(path):
    try:
        with open(path, mode='rb') as raw_file:  # Use a context manager to keep the file open
            return pickle.load(raw_file)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def open_binary_file(path):
    try:
        with open(path, mode='rb') as raw_file:  # Use a context manager to keep the file open
            return raw_file.read()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def create_folder(path):
    folder_path = os.path.dirname(path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def create_folders(*args):
    for arg in args:
        create_folder(arg)


def get_files_count_in_folder(path):
    entries = os.listdir(path)
    file_count = sum(1 for entry in entries if os.path.isfile(os.path.join(path, entry)))
    return file_count


def get_all_files_in_dir(path, include_full_path: bool = False) -> list:
    if not os.path.exists(path):
        return []
    files = []
    entries = os.listdir(path)
    for entry in entries:
        if os.path.isfile(os.path.join(path, entry)):
            file = f'{path}/{entry}' if include_full_path else entry
            files.append(file)
    return files


def get_all_files_in_dirs(path):
    if not os.path.exists(path):
        return []
    files = []
    entries = os.listdir(path)
    for entry in entries:
        if os.path.isfile(os.path.join(path, entry)):
            files.append(entry)
    return files


def get_all_folders_in_dir(path):
    if not os.path.exists(path):
        return []
    folders = []
    entries = os.listdir(path)
    for entry in entries:
        if not os.path.isfile(os.path.join(path, entry)):
            folders.append(entry)
    return folders


def get_files_w_max_depth(folder_path: str, include_current: bool = False, include_full_path: bool = True):
    files = get_all_files_in_dir(folder_path) if include_current else []
    folders = get_all_folders_in_dir(folder_path)
    for folder in folders:
        if type(folder) is str:
            path = f'{folder_path}/{folder}'
            _files = get_all_files_in_dir(path, include_full_path=include_full_path)
            files = files + _files
    return files


def get_unique_file_name(factor: int = 1000000):
    max_size = sys.maxsize
    max_size = int(max_size / factor)
    return f'{int(time.time())}_{random.randint(0, max_size)}'


def delete_file(path):
    try:
        os.remove(path)
        print(f"File '{path}' has been deleted successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied to delete the file '{path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_zip_file_in_memory(file_path):
    with zipfile.ZipFile(file_path, 'r') as zipf:
        file_list = zipf.namelist()

        if not file_list:
            return None

        with zipf.open(file_list[0]) as first_file:
            content = first_file.read()

        return content


def zip_folder(src_folder, zip_name):
    """Zip the contents of src_folder into zip_name."""
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(src_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, src_folder)
                zipf.write(file_path, arcname)


def zip_file(src_file, zip_name=None):
    # If no zip_name is provided, use the source file name and append '.zip'
    if zip_name is None:
        zip_name = os.path.splitext(src_file)[0] + '.zip'

    # Create a zip file and add the source file to it
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(src_file, os.path.basename(src_file))

    print(f"Zipped {src_file} to {zip_name}")


def string_to_zip_file(content, zip_name, file_name_in_zip):
    # Create a BytesIO object to hold the zip file in memory
    zip_buffer = io.BytesIO()

    # Create a zip file in memory and write the string content to it
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Write the string as a file inside the zip
        zipf.writestr(file_name_in_zip, content)

    # Save the zip file to disk
    create_folder(zip_name)
    with open(zip_name, 'wb') as f:
        f.write(zip_buffer.getvalue())

    print(f"String content zipped to {zip_name}")


def sanitize_file_name(path: str, start_path=None) -> str:
    file_extension = os.path.splitext(path)[1]
    path = os.path.normpath(path)
    path = re.sub(r'[^a-zA-Z0-9_\-]', '', path)
    if start_path:
        if not path.startswith(start_path):
            path = os.path.join(start_path, path)
    path = path.replace('json', '')
    path = path.replace('/', '_')
    path += file_extension
    return path


def save_base_64_image(base_64: str, output_path: str):
    try:
        image_data = base64.b64decode(base_64)

        image = Image.open(BytesIO(image_data))

        image.save(output_path)

        print(f"Image saved to {output_path} successfully.")
    except Exception as e:
        print(f"Error saving image: {e}")


if __name__ == '__main__':
    print(get_unique_file_name())
