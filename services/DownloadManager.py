import threading
import time


class DownloadManager:
    active_download_count = 0
    max_concurrent_downloads = 1
    queued_downloads = []
    active_downloads = []

    @staticmethod
    def manage_download_queue():
        def check_and_enqueue_downloads():
            while True:
                # print(f"@DownloadManager.py > Active Downloads : {DownloadManager.active_download_count}")
                if DownloadManager.max_concurrent_downloads > DownloadManager.active_download_count and len(
                        DownloadManager.queued_downloads) > 0:
                    try:
                        DownloadManager.queued_downloads[0].start_download_video()
                    except Exception as error:
                        print("@1 DownloadManager.py :", error)
                        pass
                    DownloadManager.queued_downloads.pop(0)
                time.sleep(1)

        threading.Thread(target=check_and_enqueue_downloads).start()

    @staticmethod
    def set_max_concurrent_downloads(count: int):
        DownloadManager.max_concurrent_downloads = count
