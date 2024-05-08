import threading
import time
from settings.general_settings import GeneralSettings


class DownloadManager:
    """
    Manages the download queue and controls the download process.
    """

    active_download_count = 0
    queued_downloads = []
    active_downloads = []

    @staticmethod
    def manage_download_queue():
        """
        Manages the download queue by starting downloads if conditions are met.

        This method continuously checks the download queue and starts downloads if conditions permit.
        """
        while True:
            if (GeneralSettings.settings["max_simultaneous_downloads"] > DownloadManager.active_download_count and
                    len(DownloadManager.queued_downloads) > 0):
                try:
                    DownloadManager.queued_downloads[0].start_download_video()
                except Exception as error:
                    print(f"Error occurred in manage_download_queue: {error}")
                    pass
                DownloadManager.queued_downloads.pop(0)
            time.sleep(1)

    @staticmethod
    def can_initiate_download():
        """
        Checks if a new download can be initiated based on the current active downloads.

        Returns:
            bool: True if a new download can be initiated, False otherwise.
        """
        return GeneralSettings.settings["max_simultaneous_downloads"] > DownloadManager.active_download_count

    @staticmethod
    def initialize() -> None:
        """
        Initializes the download manager by starting a separate thread for managing the download queue.
        """
        downloading_manage_thread = threading.Thread(target=DownloadManager.manage_download_queue)
        downloading_manage_thread.daemon = True
        downloading_manage_thread.start()
