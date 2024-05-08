def get_converted_time(s: int) -> str:
    h = int(s / 3600)
    m = int((s - (h * 3600)) / 60)
    s = s - (h * 3600) - (m * 60)

    if h > 0:
        converted_time = f"{h}:{m:0>2}:{s:0>2}"
    else:
        converted_time = f"{m}:{s:0>2}"

    return converted_time
