def format_path(path: str):
    path = path.strip().replace("/", "\\")
    print(path)
    while "\\\\" in path:
        path = path.replace("\\\\", "\\")
    paths = []
    for path in path.split("\\"):
        if path != " ":
            paths.append(path)
    path = "\\".join(paths)
    if path.endswith("\\"):
        path = path[0:-1]
    return path
