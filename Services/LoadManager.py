import threading
import time


class LoadManager:
    active_load_count = 0
    max_concurrent_loads = 1
    queued_loads = []
    active_loads = []

    @staticmethod
    def manage_load_queue():
        def check_and_enqueue_loads():
            while True:
                # print(f"@loadManager.py > Active loads : {LoadManager.active_load_count}")
                if (LoadManager.max_concurrent_loads > LoadManager.active_load_count and
                        len(LoadManager.queued_loads) > 0):
                    try:
                        LoadManager.queued_loads[0].load_video()
                    except Exception as error:
                        print("@1 LoadManager.py :", error)
                        pass
                    LoadManager.queued_loads.pop(0)
                time.sleep(1)

        threading.Thread(target=check_and_enqueue_loads).start()

    @staticmethod
    def set_max_concurrent_loads(count: int):
        LoadManager.max_concurrent_loads = count
