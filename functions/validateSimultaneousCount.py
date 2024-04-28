def validate_simultaneous_count(count: str) -> bool:
    max_count = 10
    try:
        count = int(count)
        if 11 > count > 0:
            return True
        else:
            return False
    except ValueError:
        return False
