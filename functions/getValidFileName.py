def get_valid_file_name(url: str) -> str:
    valid_file_name = url

    replaces = ["\\", "/", ":", '"', "?", "<", ">", "|", "*"]
    for re in replaces:
        valid_file_name = valid_file_name.replace(re, "~")

    return valid_file_name
