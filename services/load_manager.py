import threading
import time
from settings.general_settings import GeneralSettings


class LoadManager:
    """
    Manages the loading queue and controls the loading process.
    """

    active_load_count = 0
    queued_loads = []
    active_loads = []

    @staticmethod
    def manage_load_queue():
        """
        Manages the load queue by initiating loads if conditions are met.

        This method continuously checks the load queue and initiates loads if conditions permit.
        """
        while True:
            if (GeneralSettings.settings["max_simultaneous_loads"] > LoadManager.active_load_count and
                    len(LoadManager.queued_loads) > 0):
                try:
                    LoadManager.queued_loads[0].load_video()
                except Exception as error:
                    print(f"Error occurred in manage_load_queue: {error}")
                    pass
                LoadManager.queued_loads.pop(0)
            time.sleep(1)

    @staticmethod
    def can_initiate_load():
        """
        Checks if a new load can be initiated based on the current active loads.

        Returns:
            bool: True if a new load can be initiated, False otherwise.
        """
        return GeneralSettings.settings["max_simultaneous_loads"] > LoadManager.active_load_count

    @staticmethod
    def initialize() -> None:
        """
        Initializes the load manager by starting a separate thread for managing the load queue.
        """
        loading_manage_thread = threading.Thread(target=LoadManager.manage_load_queue)
        loading_manage_thread.daemon = True
        loading_manage_thread.start()
