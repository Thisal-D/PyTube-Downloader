import threading
import time
from settings.general_settings import GeneralSettings
from typing import Callable


class DownloadManager:
    """
    Manages the download queue and controls the download process.
    """
    active_download_count = 0
    queued_download_count = 0
    queued_downloads = []
    active_downloads = []
    status_change_callback: Callable = None

    @staticmethod
    def manage_download_queue():
        """
        Manages the download queue by starting downloads if conditions are met.

        This method continuously checks the download queue and starts downloads if conditions permit.
        """
        while True:
            if (GeneralSettings.settings["max_simultaneous_downloads"] > DownloadManager.active_download_count and
                    DownloadManager.queued_download_count > 0):
                try:
                    DownloadManager.queued_downloads[0].download_video()
                    DownloadManager.queued_download_count -= 1
                    DownloadManager.active_download_count += 1
                    DownloadManager.active_downloads.append(DownloadManager.queued_downloads[0])
                except Exception as error:
                    print(f"download_manager.py L33 : {error}")
                    pass
                DownloadManager.queued_downloads.pop(0)
                DownloadManager.status_change_callback()
            time.sleep(1)

    @staticmethod
    def register(video):
        DownloadManager.queued_downloads.append(video)
        DownloadManager.status_change_callback()
        DownloadManager.queued_download_count += 1

    @staticmethod
    def unregister_from_queued(video):
        if video in DownloadManager.queued_downloads:
            DownloadManager.queued_downloads.remove(video)
            DownloadManager.queued_download_count -= 1
        DownloadManager.status_change_callback()

    @staticmethod
    def unregister_from_active(video):
        if video in DownloadManager.active_downloads:
            DownloadManager.active_downloads.remove(video)
            DownloadManager.active_download_count -= 1
        DownloadManager.status_change_callback()

    @staticmethod
    def initialize(status_change_callback: Callable = None) -> None:
        """
        Initializes the download manager by starting a separate thread for managing the download queue.
        """
        DownloadManager.status_change_callback = status_change_callback
        downloading_manage_thread = threading.Thread(target=DownloadManager.manage_download_queue)
        downloading_manage_thread.daemon = True
        downloading_manage_thread.start()
