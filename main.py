from app import App
import customtkinter as ctk
from settings import (
    AppearanceSettings,
    GeneralSettings
)
import threading
from services import (
    LanguageManager,
)


try:
    # configure settings
    GeneralSettings.initialize()
    AppearanceSettings.initialize()
    LanguageManager.initialize()

    App.check_accessibility()

    # Initialize app.
    app = App()
    app.after(100, threading.Thread(target=app.initialize, daemon=True).start)
    # just run the app        
    app.run()
except Exception as error:
    print("main.py L-27:", error)

# Codes under here will only execute when the app is closed
