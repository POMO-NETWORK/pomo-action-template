
def empty_string_to_null(s: str | None) -> str | None:
    return None if s is None or len(s) == 0 else s
