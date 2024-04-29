import json


def save_settings(settings_file, settings):
    file = open(settings_file, "w")
    json.dump(obj=settings, fp=file, indent=8, sort_keys=True)
    file.close()
