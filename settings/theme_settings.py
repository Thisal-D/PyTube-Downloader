from typing import Dict
from utils import JsonUtility


class ThemeSettings:
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
        JsonUtility.write_to_file(ThemeSettings.file_path, ThemeSettings.settings)

    @staticmethod
    def initialize(file_path: str) -> None:
        """
        Initialize settings from a JSON file.

        Args:
            file_path (str): The file path to the JSON settings file.
        """
        ThemeSettings.settings = JsonUtility.read_from_file(file_path)
        ThemeSettings.file_path = file_path
