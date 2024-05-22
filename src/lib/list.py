def match_one(list, key):
    it = [l for l in list if l.id == key]
    return it.pop() if len(it) != 0 else None
