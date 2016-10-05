def obj_to_dict(obj):
    return dict((name, getattr(obj, name)) for name in dir(obj) if not name.startswith('__'))