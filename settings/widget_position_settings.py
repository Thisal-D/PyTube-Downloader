from typing import Dict
from utils import JsonUtility


class WidgetPositionSettings:
    """
    A class to manage scale settings for the application.
    """
    settings: Dict = {}

    @staticmethod
    def initialize(file_path: str) -> None:
        """
        Initialize settings from a JSON file.

        Args:
            file_path (str): The file path to the JSON settings file.

        Returns:
            WidgetPositionSettings: An instance of GeneralSettings initialized with the settings from the JSON file.
        """
        settings = JsonUtility.read_from_file(file_path)

        WidgetPositionSettings.settings = settings
