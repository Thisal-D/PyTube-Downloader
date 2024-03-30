import json

def getGeneralSettings():
    file_name = ".\\settings\\general.json"
    settings  = json.load(open(file_name, "r"))
    return settings