import customtkinter as ctk
import time
from typing import List, Dict, Tuple, Any, Literal
import threading
from settings import ThemeSettings


class ThemeManager:
    # List to keep track of all registered child objects
    registered_widgets: List[Any] = []

    # Variable to track current theme mode
    current_theme_mode: Literal["Dark", "Light", None] = None

    @staticmethod
    def get_color_based_on_theme_mode(color_pair: Tuple[str, str]) -> str:
        """Returns appropriate color based on the current theme mode."""
        if ThemeManager.current_theme_mode == "Dark":
            return color_pair[1]  # For dark theme
        else:
            return color_pair[0]  # For light theme

    @staticmethod
    def track_theme_mode_changes() -> None:
        """Periodically checks for changes in theme and updates registered widgets."""
        while True:
            current_mode = ctk.get_appearance_mode()
            if current_mode != ThemeManager.current_theme_mode:
                ThemeManager.current_theme_mode = current_mode
                ThemeManager.update_widgets_colors()
            time.sleep(1)

    @staticmethod
    def update_accent_color() -> None:
        """Updates accent color callback the change to registered widgets."""
        ThemeManager.update_widgets_accent_color()

    @staticmethod
    def update_widgets_colors() -> None:
        for widget in ThemeManager.registered_widgets:
            try:
                widget.update_widgets_colors()
            except Exception as error:
                print(f"theme_manager.py : {error}")

    @staticmethod
    def update_widgets_accent_color() -> None:
        """Updates accent color in all registered widgets."""
        for widget in ThemeManager.registered_widgets:
            try:
                widget.update_widgets_accent_color()
            except Exception as error:
                print(f"theme_manager.py : {error}")

    @staticmethod
    def initialize() -> None:
        """Starts the theme tracking system."""
        # Start tracking theme changes in a separate thread
        theme_tracking_thread = threading.Thread(target=ThemeManager.track_theme_mode_changes)
        theme_tracking_thread.daemon = True  # Daemonize the thread, so it exits when the main program exits
        theme_tracking_thread.start()

    @staticmethod
    def register_widget(widget: Any) -> None:
        """Registers a widget with the ThemeManager for theme updates."""
        ThemeManager.registered_widgets.append(widget)

    @staticmethod
    def unregister_widget(widget: Any) -> None:
        """Unregisters a widget from the ThemeManager."""
        ThemeManager.registered_widgets.remove(widget)
