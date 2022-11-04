import os

from ..constants import TEMP_FILE_FOLDER

def create_temp():
    if not temp_exists():
        os.makedirs(TEMP_FILE_FOLDER)

def delete_temp():
    if temp_exists():
        delete_folder(TEMP_FILE_FOLDER)

def delete_folder(folder_path: str):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        if os.path.isdir(file_path):
            delete_folder(file_path)
        else:
            os.remove(file_path)

    os.rmdir(folder_path)

def temp_exists():
    return os.path.exists(TEMP_FILE_FOLDER)

