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
    
    SETTINGS = {
        "alert_window": {
            "msg_color": {
                "normal": "#ee0000"
            },
            "details": {
                "normal": "#00ee00"
            }
        },
        "context_menu": {
            "text_color": [
                "#101010",
                "#eeeeee"
            ]
        },
        "navigation_button": {
            "fg_color": {
                "hover": [
                    "#f2f4f9",
                    "#32373e"
                ],
                "normal": [
                    "#e2e4e9",
                    "#21262d"
                ]
            }
        },
        "navigation_frame": {
            "fg_color": {
                "hover": [
                    "#ffffff",
                    "#0a0c12"
                ],
                "normal": [
                    "#ffffff",
                    "#0a0c12"
                ]
            }
        },
        "opacity": 100,
        "opacity_r": 1.0,
        "radio_btn": {
            "text_color": {
                "hover": [
                    "#606060",
                    "#ffffff"
                ],
                "normal": [
                    "#909090",
                    "#939aa2"
                ]
            }
        },
        "root": {
            "accent_color": {
                "default": True,
                "hover": "#5f4ff1",
                "normal": "#412ff0"
            },
            "fg_color": {
                "hover": [
                    "#ffffff",
                    "#0a0c12"
                ],
                "normal": [
                    "#ffffff",
                    "#0a0c12"
                ]
            },
            "text_color": {
                "hover": [
                    "#0a0c12",
                    "#ffffff"
                ],
                "normal": [
                    "#0a0c12",
                    "#ffffff"
                ]
            },
            "theme_mode": 0
        },
        "scale": 100.0,
        "scale_r": 1.0,
        "settings_panel": {
            "accent_colors": {
                "0": {
                    "hover": "#5f4ff1",
                    "normal": "#412ff0"
                },
                "1": {
                    "hover": "#903efb",
                    "normal": "#7a14ff"
                },
                "2": {
                    "hover": "#57A1EB",
                    "normal": "#284CEA"
                },
                "3": {
                    "hover": "#FF851B",
                    "normal": "#FF7F11"
                },
                "4": {
                    "hover": "#0cf749",
                    "normal": "#22c14b"
                },
                "5": {
                    "hover": "#03A9F4",
                    "normal": "#039BE5"
                },
                "6": {
                    "hover": "#9C27B0",
                    "normal": "#8E24AA"
                },
                "7": {
                    "hover": "#CDDC39",
                    "normal": "#C0CA33"
                },
                "8": {
                    "hover": "#009688",
                    "normal": "#00796B"
                },
                "9": {
                    "hover": "#FF5722",
                    "normal": "#F4511E"
                },
                "a": {
                    "hover": "#FF9800",
                    "normal": "#F57C00"
                },
                "b": {
                    "hover": "#795548",
                    "normal": "#6D4C41"
                },
                "c": {
                    "hover": "#607D8B",
                    "normal": "#546E7A"
                },
                "d": {
                    "hover": "#FF5252",
                    "normal": "#E53935"
                },
                "e": {
                    "hover": "#FF3D00",
                    "normal": "#FFAB00"
                },
                "f": {
                    "hover": "#7091e6",
                    "normal": "#8697c4"
                }
            },
            "nav_text_color": [
                "#252525",
                "#dddddd"
            ],
            "text_color": [
                "#141212",
                "#eeeeee"
            ],
            "warning_color": {
                "hover": "#ff3131",
                "normal": "#f95568"
            }
        },
        "url_adding_button": {
            "fg_color": {
                "hover": [
                    "#ffffff",
                    "#272c33"
                ],
                "normal": [
                    "#f4f6fd",
                    "#161b22"
                ]
            }
        },
        "url_entry": {
            "border_color": {
                "hover": [
                    "#d0d7de",
                    "#40464e"
                ],
                "normal": [
                    "#d0d7de",
                    "#30363d"
                ]
            },
            "fg_color": {
                "hover": [
                    "#f9faff",
                    "#21262d"
                ],
                "normal": [
                    "#f6f8fa",
                    "#161b22"
                ]
            },
            "text_color": {
                "hover": [
                    "#1f2328",
                    "#dddddd"
                ],
                "normal": [
                    "#636c76",
                    "#ffffff"
                ]
            }
        },
        "video_object": {
            "btn_fg_color": {
                "hover": [
                    "#ffffff",
                    "#2c2e34"
                ],
                "normal": [
                    "#dedede",
                    "#1b1d23"
                ]
            },
            "btn_text_color": {
                "hover": [
                    "#202020",
                    "#ffffff"
                ],
                "normal": [
                    "#505050",
                    "#aaaaaa"
                ]
            },
            "error_color": {
                "hover": "#ff3131",
                "normal": "#ee0000"
            },
            "fg_color": {
                "hover": [
                    "#ffffff",
                    "#161616"
                ],
                "normal": [
                    "#eeeeee",
                    "#121212"
                ]
            },
            "remove_btn_text_color": {
                "hover": [
                    "#ffffff",
                    "#ffffff"
                ],
                "normal": [
                    "#cdcdcd",
                    "#cdcdcd"
                ]
            },
            "text_color": {
                "hover": [
                    "#707070",
                    "#aaaaaa"
                ],
                "normal": [
                    "#404040",
                    "#bbbbbb"
                ]
            }
        }
    }

    @staticmethod
    def initialize() -> None:
            
        """
        Initialize settings from a JSON file.

        """
        backup_exists = AppearanceSettings.is_backup_exists()
        if not backup_exists:
            AppearanceSettings.create_backup()
        
        if backup_exists and FileUtility.is_accessible(AppearanceSettings.backup_dir):
            AppearanceSettings.settings = JsonUtility.read_from_file(AppearanceSettings.backup_path)
        else:
            AppearanceSettings.settings = JsonUtility.read_from_file(AppearanceSettings.file_path)
        
        if not AppearanceSettings.are_all_keys_present(AppearanceSettings.SETTINGS, AppearanceSettings.settings):
            AppearanceSettings.add_missing_keys()
    
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
    def are_all_keys_present(required: dict, initialized: dict) -> bool:
        """
        Check if all required keys (nested) are present in the initialized settings.

        Args:
            required (dict): The dictionary defining the required structure.
            initialized (dict): The dictionary to check against the required structure.

        Returns:
            bool: True if all keys exist, False otherwise.
        """
        for key, value in required.items():
            if key not in initialized:
                return False
            # If the value is a dictionary, recursively check nested keys
            if isinstance(value, dict):
                if not isinstance(initialized[key], dict) or not AppearanceSettings.are_all_keys_present(value, initialized[key]):
                    return False
        return True
    
    @staticmethod
    def add_missing_keys() -> None:
        """
        Add any missing keys from the default settings to the initialized settings.

        This ensures that the settings include all required keys with their default values,
        even for nested dictionaries.
        """
        def recursive_add_missing(default: dict, initialized: dict) -> None:
            for key, value in default.items():
                if key not in initialized:
                    initialized[key] = value
                elif isinstance(value, dict) and isinstance(initialized[key], dict):
                    recursive_add_missing(value, initialized[key])

        recursive_add_missing(AppearanceSettings.SETTINGS, AppearanceSettings.settings)

    @staticmethod
    def create_backup() -> None:
        FileUtility.create_directory(AppearanceSettings.backup_dir)
        JsonUtility.write_to_file(
            AppearanceSettings.backup_path,
            JsonUtility.read_from_file("data\\appearance.json")
        )
        