import os


def validate_download_path(path: str) -> bool:
    paths = path.split(":")
    if not os.path.exists(paths[0]+':'):
        return False
    if len(paths) != 2:
        return False
    elif paths[1] != "":
        if not paths[1].startswith("\\"):
            return False
    path = paths[1]
    invalid_characters = ['?', '%', '*', ':', '|', '"', '<', '>']
    for invalid_char in invalid_characters:
        if invalid_char in path:
            return False
    return True
