import time
import threading


class LoadingIndicatorController:
    dots_count: int = 1
    update_delay: float = 0.7
    max_dots_count: int = 4

    @staticmethod
    def start_loading_indicator():
        def update_loading_indicator():
            while True:
                for LoadingIndicatorController.dots_count in range(1, LoadingIndicatorController.max_dots_count+1):
                    time.sleep(LoadingIndicatorController.update_delay)

        threading.Thread(target=update_loading_indicator, daemon=True).start()

    @staticmethod
    def set_indicator_update_delay(update_delay: float):
        LoadingIndicatorController.update_delay = update_delay

    @staticmethod
    def start():
        LoadingIndicatorController.start_loading_indicator()
