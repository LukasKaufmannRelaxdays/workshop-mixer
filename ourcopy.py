def deepcopy(thing):
    if type(thing) == list:
        return [deepcopy(x) for x in thing]
    if type(thing) == dict:
        return {k: deepcopy(v) for k, v in thing.items()}
    return thing
