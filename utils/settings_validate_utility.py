import os
import tkinter as tk


class SettingsValidateUtility:
    @staticmethod
    def validate_simultaneous_count(count_str: str, with_range: bool) -> bool:
        """
        Validate the simultaneous count entered by the user.

        Args:
            count_str (str): The value entered by the user.

        Returns:
            bool: True if the value is a valid simultaneous count, False otherwise.
        """
        try:
            count = int(count_str)
            if with_range:
                if 0 < count < 11:
                    return True
                else:
                    return False
            else:
                return True
        except ValueError:
            return False

    @staticmethod
    def validate_download_path(path: str) -> bool:
        """
        Validate the download path entered by the user.

        Args:
            path (str): The download path entered by the user.

        Returns:
            bool: True if the path is valid, False otherwise.
        """
        paths = path.split(":")
        if not os.path.exists(paths[0] + ':'):
            return False
        if len(paths) != 2:
            return False
        elif paths[1] != "":
            if not paths[1].startswith("\\"):
                return False
        path = paths[1]
        invalid_characters = ['?', '%', '*', ':', '|', '"', '<', '>']
        for invalid_char in invalid_characters:
            if invalid_char in path:
                return False
        return True

    @staticmethod
    def validate_accent_color(color: str) -> bool:
        """
        Validate the accent color entered by the user.

        Args:
            color (str): The color value entered by the user.

        Returns:
            bool: True if the color is valid, False otherwise.
        """
        try:
            normal_color, hover_color = color.split(",")
            try:
                tk.Button(fg=normal_color, bg=hover_color)
                return True
            except Exception as error:
                print(f"validate_accent_color : {error}")
                return False
        except Exception as error:
            print(f"validate_accent_color : {error}")
            return False
