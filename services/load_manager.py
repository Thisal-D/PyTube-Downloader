import threading
import time
from settings.general_settings import GeneralSettings
from typing import Callable


class LoadManager:
    """
    Manages the loading queue and controls the loading process.
    """
    active_load_count = 0
    queued_load_count = 0
    queued_loads = []
    active_loads = []
    status_change_callback: Callable = None

    @staticmethod
    def manage_load_queue():
        """
        Manages the load queue by initiating loads if conditions are met.

        This method continuously checks the load queue and initiates loads if conditions permit.
        """
        while True:
            if (GeneralSettings.settings["max_simultaneous_loads"] > LoadManager.active_load_count and
                    LoadManager.queued_load_count > 0):
                try:
                    LoadManager.queued_loads[0].load_video()
                    LoadManager.active_loads.append(LoadManager.queued_loads[0])
                    LoadManager.queued_load_count -= 1
                    LoadManager.active_load_count += 1
                except Exception as error:
                    print(f"load_manager.py L33 : {error}")
                    pass
                LoadManager.queued_loads.pop(0)
                LoadManager.status_change_callback()
            time.sleep(1)

    @staticmethod
    def register(video):
        LoadManager.queued_loads.append(video)
        LoadManager.queued_load_count += 1
        LoadManager.status_change_callback()

    @staticmethod
    def unregister_from_queued(video):
        if video in LoadManager.queued_loads:
            LoadManager.queued_loads.remove(video)
            LoadManager.queued_load_count -= 1
        LoadManager.status_change_callback()

    @staticmethod
    def unregister_from_active(video):
        if video in LoadManager.active_loads:
            LoadManager.active_loads.remove(video)
            LoadManager.active_load_count -= 1
        LoadManager.status_change_callback()

    @staticmethod
    def initialize(status_change_callback: Callable = None) -> None:
        """
        Initializes the load manager by starting a separate thread for managing the load queue.
        """
        LoadManager.status_change_callback = status_change_callback
        loading_manage_thread = threading.Thread(target=LoadManager.manage_load_queue)
        loading_manage_thread.daemon = True
        loading_manage_thread.start()
