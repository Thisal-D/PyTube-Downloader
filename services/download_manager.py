import threading
import time
from settings.general_settings import GeneralSettings
from typing import Callable, List, Dict
from pytube import request as pytube_request
from pytubefix import request as pytubefix_request

class DownloadManager:
    """
    Manages the download queue and controls the download process.
    """

    # Class variables to keep track of active and queued loads
    active_download_count: int = 0
    queued_download_count: int = 0
    queued_downloads: List = []
    active_downloads: List = []
    status_change_callback: Callable = None
  
    resolutions: List = [
        'Audio Only',
        '144p',
        '240p',
        '360p',
        '480p',
        '720p',
        '1080p',
        '1440p',
        '2160p',
        '4320p',
        '8640p',
        '17280p'
    ]
    
    default_chunk_size: int = 2097152

    @staticmethod
    def manage_download_queue():
        """
        Manages the download queue by starting downloads if conditions are met.

        This method continuously checks the download queue and starts downloads if conditions permit.
        Delay is 1 second (1000 milliseconds).
        """
        while True:
            if (GeneralSettings.settings["max_simultaneous_downloads"] > DownloadManager.active_download_count and
                    DownloadManager.queued_download_count > 0):
                try:
                    DownloadManager.queued_download_count -= 1
                    DownloadManager.queued_downloads[0].download_video()
                    DownloadManager.active_download_count += 1
                    DownloadManager.active_downloads.append(DownloadManager.queued_downloads.pop(0))
                except Exception as error:
                    # Log the error for analysis
                    print(f"download_manager.py L38 : {error}")
                    pass
                DownloadManager.status_change_callback()
            # Wait 1 second (1000 milliseconds) before checking the queue again
            time.sleep(1)

    @staticmethod
    def register(video):
        """
        Registers a video to be downloaded.

        Adds the video to the download queue and updates the queued download count.
        """
        DownloadManager.queued_downloads.append(video)
        DownloadManager.queued_download_count += 1
        DownloadManager.status_change_callback()

    @staticmethod
    def unregister_from_queued(video):
        """
        Unregisters a video from the download queue.

        Removes the video from the download queue and updates the queued download count.
        """
        if video in DownloadManager.queued_downloads:
            DownloadManager.queued_downloads.remove(video)
            DownloadManager.queued_download_count -= 1
        DownloadManager.status_change_callback()

    @staticmethod
    def unregister_from_active(video):
        """
        Unregisters a video from the active download list.

        Removes the video from the active download list and updates the active download count.
        """
        if video in DownloadManager.active_downloads:
            DownloadManager.active_downloads.remove(video)
            DownloadManager.active_download_count -= 1
        DownloadManager.status_change_callback()

    @staticmethod
    def initialize(status_change_callback: Callable = None) -> None:
        """
        Initializes the download manager by starting a separate thread for managing the download queue.

        Args:
            status_change_callback (Callable, optional): A callback function to be called on status changes.
        """
        DownloadManager.status_change_callback = status_change_callback
        DownloadManager.configure_chunk_size()
        downloading_manage_thread = threading.Thread(target=DownloadManager.manage_download_queue)
        downloading_manage_thread.daemon = True
        downloading_manage_thread.start()
        
    @staticmethod
    def configure_chunk_size():
        pytube_request.default_range_size = GeneralSettings.settings["chunk_size"]
        pytubefix_request.default_range_size = GeneralSettings.settings["chunk_size"]
        