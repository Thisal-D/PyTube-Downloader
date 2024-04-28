import customtkinter as ctk
import time
from typing import List, Dict, Tuple, Any


class ThemeManager:
    child_objects: List = []
    theme: str = "-"

    @staticmethod
    def get_color_based_on_theme(color: Tuple[str, str]) -> str:
        if ThemeManager.theme == "Dark":
            return color[1]
        return color[0]

    @staticmethod
    def theme_tracker() -> None:
        while True:
            if ctk.get_appearance_mode() != ThemeManager.theme:
                ThemeManager.theme = ctk.get_appearance_mode()
                for child_object in ThemeManager.child_objects:
                    try:
                        child_object.reset_widgets_colors()
                    except Exception as error:
                        print("@1 ThemeManager.py :", error)
            time.sleep(1)

    @staticmethod
    def update_accent_color(new_accent_color: Dict) -> None:
        for child_object in ThemeManager.child_objects:
            try:
                child_object.update_accent_color(new_accent_color)
            except Exception as error:
                print("@2 ThemeManager.py :", error)

    @staticmethod
    def bind_widget(widget: Any) -> None:
        ThemeManager.child_objects.append(widget)

    @staticmethod
    def unbind_widget(widget: Any) -> None:
        ThemeManager.child_objects.remove(widget)
