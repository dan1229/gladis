def str_to_bool(v):
    return str(v).lower() in (
        "yes",
        "true",
        "t",
        "1",
        "on",
    )
