import threading
import time
from typing import Callable
import os
from settings.general_settings import GeneralSettings


class VideoConvertManager:
    """
    Manages the convert queue and controls the convert process.
    """
    
    FFMPEG_PATH = os.path.join("ffmpeg", "ffmpeg.exe")
    
    # Class variables to keep track of active and queued loads
    active_convert_count = 0
    queued_convert_count = 0
    queued_converts = []
    active_converts = []


    @staticmethod
    def manage_convert_queue():
        """
        Manages the convert queue by starting converts if conditions are met.

        This method continuously checks the convert queue and starts converts if conditions permit.
        Delay is 1 second (1000 milliseconds).
        """
        while True:
            if (GeneralSettings.settings["max_simultaneous_converts"] > VideoConvertManager.active_convert_count and
                    VideoConvertManager.queued_convert_count > 0):
                try:
                    VideoConvertManager.queued_convert_count -= 1
                    VideoConvertManager.queued_converts[0].convert_video()
                    VideoConvertManager.active_convert_count += 1
                    VideoConvertManager.active_converts.append(VideoConvertManager.queued_converts.pop(0))
                except Exception as error:
                    # Log the error for analysis
                    print(f"convert_manager.py L38 : {error}")
                    pass
                #VideoConvertManager.status_change_callback()
            # Wait 1 second (1000 milliseconds) before checking the queue again
            time.sleep(1)
        
    @staticmethod
    def register(video):
        """
        Registers a video to be converted.

        Adds the video to the convert queue and updates the queued convert count.
        """
        VideoConvertManager.queued_converts.append(video)
        VideoConvertManager.queued_convert_count += 1
        
        #VideoConvertManager.status_change_callback()

    @staticmethod
    def unregister_from_queued(video):
        """
        Unregisters a video from the convert queue.

        Removes the video from the convert queue and updates the queued convert count.
        """
        if video in VideoConvertManager.queued_converts:
            VideoConvertManager.queued_converts.remove(video)
            VideoConvertManager.queued_convert_count -= 1
        #VideoConvertManager.status_change_callback()

    @staticmethod
    def unregister_from_active(video):
        """
        Unregisters a video from the active convert list.

        Removes the video from the active convert list and updates the active convert count.
        """
        if video in VideoConvertManager.active_converts:
            VideoConvertManager.active_converts.remove(video)
            VideoConvertManager.active_convert_count -= 1
        #VideoConvertManager.status_change_callback()

    @staticmethod
    def initialize(status_change_callback: Callable = None) -> None:
        """
        Initializes the convert manager by starting a separate thread for managing the convert queue.

        Args:
            status_change_callback (Callable, optional): A callback function to be called on status changes.
        """
        #VideoConvertManager.status_change_callback = status_change_callback
        video_converting_manage_thread = threading.Thread(target=VideoConvertManager.manage_convert_queue)
        video_converting_manage_thread.daemon = True
        video_converting_manage_thread.start()
