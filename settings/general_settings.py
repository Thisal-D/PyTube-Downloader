from typing import Dict
from utils import JsonUtility, FileUtility
import os


class GeneralSettings:
    """
    A class to manage general settings for the application.
    """
    settings: Dict = {}
    file_dir = f"data"
    file_path = file_dir + "\\general.json"
    backup_dir = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\PyTube Downloader\\data"
    backup_path = backup_dir + "\\general.json"
    default_download_dir = f"C:\\users\\{os.getlogin()}\\downloads\\PyTube Downloader\\"

    @staticmethod
    def initialize() -> None:
        """
        Initialize settings from a JSON file.

        Returns:
            GeneralSettings: An instance of GeneralSettings initialized with the settings from the JSON file.
        """

        # Create settings backup on user:/app
        backup_exists = GeneralSettings.is_backup_exists()
        if not backup_exists:
            GeneralSettings.create_backup()
          
        if backup_exists and FileUtility.is_accessible(GeneralSettings.backup_dir):
            settings = JsonUtility.read_from_file(GeneralSettings.backup_path)
        else:
            settings = JsonUtility.read_from_file(GeneralSettings.file_path)

        if settings.get("download_directory") is False:
            settings["download_directory"] = GeneralSettings.default_download_dir

        GeneralSettings.settings = settings

    @staticmethod
    def save_settings() -> None:
        """
        Save the current settings to a file.
        """
        if not GeneralSettings.is_backup_exists():
            GeneralSettings.create_backup()
            
        JsonUtility.write_to_file(GeneralSettings.backup_path, GeneralSettings.settings)
        JsonUtility.write_to_file(GeneralSettings.file_path, GeneralSettings.settings)
        
    @staticmethod                
    def is_backup_exists() -> bool:
        """
        Check is backup settings exists
        """
        if os.path.exists(GeneralSettings.backup_path):
            return True
        return False
    
    @staticmethod 
    def create_backup() -> None:
        FileUtility.create_directory(GeneralSettings.backup_dir)
        JsonUtility.write_to_file(
            GeneralSettings.backup_path,
            JsonUtility.read_from_file("data\\general.json")
        )
        