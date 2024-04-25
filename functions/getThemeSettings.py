import json


def list_to_tuple(data: dict):
    for key in data.keys():
        if type(data[key]) is dict:
            for key2 in data[key].keys():
                if type(data[key][key2]) is dict:
                    for key3 in data[key][key2].keys():
                        if type(data[key][key2][key3]) is list:
                            data[key][key2][key3] = tuple(data[key][key2][key3])
                elif type(data[key][key2]) is list:
                    data[key][key2] = tuple(data[key][key2])
        else:
            if type(data[key]) is list:
                data[key] = tuple(data[key])

    print(data)
    return data


def get_theme_settings():
    file_name = ".\\settings\\theme.json"
    settings = json.load(open(file_name, "r"))

    return list_to_tuple(settings)
