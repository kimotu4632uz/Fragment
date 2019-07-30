def finddict(list, key, value):
    for dict in list:
        if dict[key] == value:
            return dict
