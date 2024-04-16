import json

def saveSettings(file, settings):
    file = open(file, "w")
    json.dump(obj=settings, fp=file, indent=8, sort_keys=True)
    file.close()