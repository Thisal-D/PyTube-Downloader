import json

def getThemeSettings():
    file_name = ".\\settings\\theme.json"
    settings  = json.load(open(file_name, "r"))
    for key in settings.keys():
        if type(settings[key]) == list:
            settings[key] = tuple(settings[key])
    return settings