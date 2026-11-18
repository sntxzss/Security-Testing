USERS: dict[int, dict] = {}
_next_id = 0


def new_user_id() -> int:
    global _next_id
    _next_id += 1
    return _next_id