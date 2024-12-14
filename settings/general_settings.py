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

    SETTINGS = {
        "automatic_download": {
            "quality": 0,
            "status": "disable"
        },
        "create_sep_path_for_playlists": False,
        "create_sep_path_for_qualities": False,
        "create_sep_path_for_videos_audios": False,
        "download_directory": False,
        "lang_code": "en",
        "language": "English",
        "load_thumbnail": True,
        "max_simultaneous_downloads": 1,
        "max_simultaneous_converts": 1,
        "max_simultaneous_loads": 1,
        "re_download_automatically": False,
        "reload_automatically": False,
        "update_delay": 0.5,
        "alerts": True,
        "window_geometry": "900x500-7+0"
    }
    
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
            GeneralSettings.settings = JsonUtility.read_from_file(GeneralSettings.backup_path)
        else:
            GeneralSettings.settings = JsonUtility.read_from_file(GeneralSettings.file_path)
            
        if not GeneralSettings.are_all_keys_present():
            GeneralSettings.add_missing_keys()
            
        if GeneralSettings.settings.get("download_directory") is False:
            GeneralSettings.settings["download_directory"] = GeneralSettings.default_download_dir

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
    def are_all_keys_present() -> bool:
        """
        Check if all required settings keys are present in the initialized settings.
        
        Returns:
            bool: True if all keys exist, False otherwise.
        """
        for key in GeneralSettings.SETTINGS.keys():
            if key not in GeneralSettings.settings.keys():
                return False
        return True
    
    def add_missing_keys() -> None:
        """
        Add any missing keys from the default settings to the initialized settings.
        
        This ensures that the settings include all required keys with their default values.
        """
        for key in GeneralSettings.SETTINGS.keys():
            if key not in GeneralSettings.settings.keys():
                GeneralSettings.settings[key] = GeneralSettings.SETTINGS[key]
        
    @staticmethod 
    def create_backup() -> None:
        FileUtility.create_directory(GeneralSettings.backup_dir)
        JsonUtility.write_to_file(
            GeneralSettings.backup_path,
            JsonUtility.read_from_file("data\\general.json")
        )
        