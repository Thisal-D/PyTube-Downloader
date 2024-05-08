from typing import Union


def get_converted_size(s: Union[int, float], decimal_points: int) -> str:
    data_units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    index = 0

    while len(str(int(s))) > 3 and (index+1) < len(data_units):
        s = s / 1024
        index += 1
    if decimal_points > 0:
        converted_size = f"{round(s, decimal_points)} {data_units[index]}"
    else:
        converted_size = f"{int(s)} {data_units[index]}"

    return converted_size
