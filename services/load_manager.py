import threading
import time
from settings.general_settings import GeneralSettings
from typing import Callable, List


class LoadManager:
    """
    Manages the loading queue videos and controls the loading process.
    """

    # Class variables to keep track of active and queued loads
    active_load_count: int = 0
    queued_load_count: int = 0
    queued_loads: List = []
    active_loads: List = []
    status_change_callback: Callable = None

    @staticmethod
    def manage_load_queue() -> None:
        """
        Manages the load queue by initiating loads if conditions are met.

        This method continuously checks the load queue and initiates loads if conditions permit.
        Delay is 1 second (1000 milliseconds).
        """
        while True:
            if (GeneralSettings.settings["max_simultaneous_loads"] > LoadManager.active_load_count and
                    LoadManager.queued_load_count > 0):
                try:
                    # Dequeue a video, initiate loading, and update counts
                    LoadManager.queued_load_count -= 1
                    LoadManager.queued_loads[0].load_video()
                    LoadManager.active_load_count += 1
                    LoadManager.active_loads.append(LoadManager.queued_loads.pop(0))
                except Exception as error:
                    # Log the error for analysis
                    print(f"load_manager.py L38 : {error}")
                    pass
                LoadManager.status_change_callback()
            # wait 1 seconds (1000 milliseconds) before checking the queue again
            time.sleep(1)

    @staticmethod
    def register(video) -> None:
        """
        Registers a video to be loaded.

        Adds the video to the load queue and updates the queued load count.
        """
        LoadManager.queued_loads.append(video)
        LoadManager.queued_load_count += 1
        LoadManager.status_change_callback()

    @staticmethod
    def unregister_from_queued(video) -> None:
        """
        Unregisters a video from the load queue.

        Removes the video from the load queue and updates the queued load count.
        """
        if video in LoadManager.queued_loads:
            LoadManager.queued_loads.remove(video)
            LoadManager.queued_load_count -= 1
        LoadManager.status_change_callback()

    @staticmethod
    def unregister_from_active(video) -> None:
        """
        Unregisters a video from the active load list.

        Removes the video from the active load list and updates the active load count.
        """
        if video in LoadManager.active_loads:
            LoadManager.active_loads.remove(video)
            LoadManager.active_load_count -= 1
        LoadManager.status_change_callback()

    @staticmethod
    def initialize(status_change_callback: Callable) -> None:
        """
        Initializes the load manager by starting a separate thread for managing the load queue.

        Args:
            status_change_callback (Callable, optional): A callback function to be called on status changes.
        """
        LoadManager.status_change_callback = status_change_callback
        loading_manage_thread = threading.Thread(target=LoadManager.manage_load_queue)
        loading_manage_thread.daemon = True
        loading_manage_thread.start()
