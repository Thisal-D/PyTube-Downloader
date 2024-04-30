from typing import Dict


class GeneralSettings:
    general_settings: Dict = None

    @staticmethod
    def configure_general_settings(settings: Dict):
        GeneralSettings.general_settings = settings
