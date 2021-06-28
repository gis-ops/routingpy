def get_max_depth(list_):
    """Returns the maximum depth of a nested list."""
    return isinstance(list_, list) and max(map(get_max_depth, list_)) + 1
