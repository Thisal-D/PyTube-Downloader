def validate_simultaneous_count(count: str) -> bool:
    try:
        count = int(count)
        if 11 > count > 0:
            return True
        else:
            return False
    except ValueError:
        return False
