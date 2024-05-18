from typing import Dict, List, Any
from utils import JsonUtility
from settings import GeneralSettings


class LanguageManager:
    current_language: str = ""
    data: Dict = None
    registered_widgets: List[Any] = []
    
    @staticmethod
    def update_language() -> None:
        LanguageManager.initialize()
        LanguageManager.update_widgets_text()
        
    @staticmethod
    def update_widgets_text() -> None:
        """
        Updates language in all registered widgets based on the current language.
        """
        for widget in LanguageManager.registered_widgets:
            try:
                widget.update_widgets_text()
            except Exception as error:
                print(f"language_manager.py L-25 : {error}")
    
    @staticmethod
    def initialize() -> None:
        lang_file = f"data\\languages\\{GeneralSettings.settings["lang_code"]}.json"
        LanguageManager.data = JsonUtility.read_from_file(lang_file)

    @staticmethod
    def register_widget(widget: Any) -> None:
        """
        Registers a widget with the LanguageManager for language updates.

        Args:
            widget (Any): The widget to register.
        """
        LanguageManager.registered_widgets.append(widget)

    @staticmethod
    def unregister_widget(widget: Any) -> None:
        """
        Unregisters a widget from the LanguageManager.

        Args:
            widget (Any): The widget to LanguageManager.
        """
        LanguageManager.registered_widgets.remove(widget)