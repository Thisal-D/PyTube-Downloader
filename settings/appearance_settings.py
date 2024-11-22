from typing import Dict
from utils import JsonUtility, FileUtility
import os


class AppearanceSettings:
    """
    A class to manage appearance settings for the application.
    """
    settings: Dict = {}
    file_dir = f"data"
    file_path = file_dir + "\\appearance.json"
    backup_dir = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\PyTube Downloader\\data"
    backup_path = backup_dir + "\\appearance.json"
    
    themes = ("dark", "light", "system")

    @staticmethod
    def initialize() -> None:
            
        """
        Initialize settings from a JSON file.

        """
        backup_exists = AppearanceSettings.is_backup_exists()
        if not backup_exists:
            AppearanceSettings.create_backup()
        
        if backup_exists and FileUtility.is_accessible(AppearanceSettings.backup_dir):
            settings = JsonUtility.read_from_file(AppearanceSettings.backup_path)
        else:
            settings = JsonUtility.read_from_file(AppearanceSettings.file_path)
        
        AppearanceSettings.settings = settings
    
    @staticmethod
    def save_settings() -> None:
        """
        Save the current settings to a file.
        """
        if not AppearanceSettings.is_backup_exists():
            AppearanceSettings.create_backup()
            
        JsonUtility.write_to_file(AppearanceSettings.backup_path, AppearanceSettings.settings)
        JsonUtility.write_to_file(AppearanceSettings.file_path, AppearanceSettings.settings)
        
    @staticmethod                
    def is_backup_exists() -> bool:
        """
        Check is backup settings exists
        """
        if os.path.exists(AppearanceSettings.backup_path):
            return True
        return False
    
    @staticmethod
    def create_backup() -> None:
        FileUtility.create_directory(AppearanceSettings.backup_dir)
        JsonUtility.write_to_file(
            AppearanceSettings.backup_path,
            JsonUtility.read_from_file("data\\appearance.json")
        )
        