import threading
import time
from .GeneralSettings import GeneralSettings


class LoadManager:
    active_load_count = 0
    queued_loads = []
    active_loads = []

    @staticmethod
    def manage_load_queue():
        def check_and_enqueue_loads():
            while True:
                # print(f"@loadManager.py > Active loads : {LoadManager.active_load_count}")
                if (GeneralSettings.general_settings["simultaneous_loads"] > LoadManager.active_load_count and
                        len(LoadManager.queued_loads) > 0):
                    try:
                        LoadManager.queued_loads[0].load_video()
                    except Exception as error:
                        print("@1 LoadManager.py :", error)
                        pass
                    LoadManager.queued_loads.pop(0)
                time.sleep(1)

        threading.Thread(target=check_and_enqueue_loads, daemon=True).start()
