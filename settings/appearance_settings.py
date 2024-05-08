from typing import Dict
from utils import JsonUtility


class AppearanceSettings:
    """
    A class to manage theme settings for the application.
    """
    settings: Dict = {}
    file_path: str = ""

    @staticmethod
    def save_settings() -> None:
        """
        Save the current settings to a file.
        """
        JsonUtility.write_to_file(AppearanceSettings.file_path, AppearanceSettings.settings)

    @staticmethod
    def initialize(file_path: str) -> None:
        """
        Initialize settings from a JSON file.

        Args:
            file_path (str): The file path to the JSON settings file.
        """
        AppearanceSettings.settings = JsonUtility.read_from_file(file_path)
        AppearanceSettings.file_path = file_path
