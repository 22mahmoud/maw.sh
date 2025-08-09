def get_all_subclasses(cls):
    subclasses = cls.__subclasses__()
    return subclasses + [g for s in subclasses for g in get_all_subclasses(s)]
