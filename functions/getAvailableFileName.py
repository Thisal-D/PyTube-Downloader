import os


def get_available_file_name(file_name_extension: str) -> str:
    if os.path.exists(file_name_extension):
        split_path = file_name_extension.split(".")
        file_name, extension = ".".join(split_path[0:-1]), split_path[-1]
        i = 0
        while os.path.exists(f"{file_name} ({i}).{extension}"):
            i += 1

        return f"{file_name} ({i}).{extension}"
    else:
        return file_name_extension
