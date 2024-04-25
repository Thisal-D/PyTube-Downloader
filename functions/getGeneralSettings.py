import json
import os


def get_general_settings() -> dict:
    general_settings_file_path = ".\\settings\\general.json"
    general_settings = json.load(open(general_settings_file_path, "r"))

    if not general_settings["download_directory"]:
        general_settings["download_directory"] = f"C:\\Users\\{os.getlogin()}\\Downloads\\PyTube Downloader"
    print(general_settings)
    return general_settings
