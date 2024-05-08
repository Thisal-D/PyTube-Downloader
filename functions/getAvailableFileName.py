import os


def get_available_file_name(path: str) -> str:
    split_path = path.split(".")
    file_name, extension = ".".join(split_path[0:-1]), split_path[-1]
    generate_file_name = file_name
    i = 2

    while os.path.exists(f"{generate_file_name}.{extension}"):
        generate_file_name = f"{file_name} ({i})"
        i += 1

    return f"{file_name}.{extension}"
