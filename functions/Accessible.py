import os
from .getAvailableFileName import get_available_file_name
from .createDownloadDirectory import create_download_directory


def accessible(path: str) -> bool:
    file = path + "\\" + get_available_file_name("pytube.pytube")
    try:
        create_download_directory(path)
        with open(file, "w"):
            pass
        os.remove(file)
        return True
    except Exception as error:
        print(f"@ Accessible.py : {error}")
        return False
