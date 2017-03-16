def resolve_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return [value]

    return value


def resolve_tuple(value, default=None):
    if value is None:
        return tuple()

    if default is None:
        default = lambda v: (v,)

    # Resolve tuple
    if not isinstance(value, tuple):
        return default(value)

    return value


def resolve_tuples(items, default=None):
    if items is None:
        return []

    if default is None:
        default = lambda v: (v,)

    # Convert `items` to list
    if not isinstance(items, list):
        items = [items]

    # Resolve tuples
    return [
        resolve_tuple(item, default)
        for item in items
    ]
