import customtkinter as ctk
import time
from typing import List, Dict, Tuple, Any, Literal


class ThemeManager:
    child_objects: List[Any] = []
    theme_settings: Dict = None
    theme_mode: Literal["Dark", "Light", None] = None

    @staticmethod
    def get_color_based_on_theme(color: Tuple[str, str]) -> str:
        if ThemeManager.theme_mode == "Dark":
            return color[1]
        return color[0]

    @staticmethod
    def theme_tracker() -> None:
        while True:
            if ctk.get_appearance_mode() != ThemeManager.theme_mode:
                ThemeManager.theme_mode = ctk.get_appearance_mode()
                for child_object in ThemeManager.child_objects:
                    try:
                        child_object.reset_widgets_colors()
                    except Exception as error:
                        print("@1 ThemeManager.py :", error)
            time.sleep(1)

    @staticmethod
    def update_accent_color(new_accent_color: Dict) -> None:
        ThemeManager.theme_settings["root"]["accent_color"] = new_accent_color
        ThemeManager.update_child_widget_accent_color()

    @staticmethod
    def update_child_widget_accent_color():
        for child_object in ThemeManager.child_objects:
            try:
                child_object.update_accent_color()
            except Exception as error:
                print("@2 ThemeManager.py :", error)

    @staticmethod
    def bind_widget(widget: Any) -> None:
        ThemeManager.child_objects.append(widget)

    @staticmethod
    def unbind_widget(widget: Any) -> None:
        ThemeManager.child_objects.remove(widget)

    @staticmethod
    def configure_theme_settings(theme_settings: Dict):
        ThemeManager.theme_settings = theme_settings
