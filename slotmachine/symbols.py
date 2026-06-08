import re

def strset_has(_str, _set):
    connect = False
    for x in _set:
        if string_has(_str, x):
            connect = True
    return connect

def string_has(str1, str2):
    if str1 in str2:
        return True
    else:
        return False

def strset_compare(_str, _set, strict=False):
    return any(string_compare(_str, x, strict) for x in _set)

def string_compare(str1, str2, strict = False):
    if re.fullmatch(str.lower(str1), str.lower(str2)):
        return True
    elif 'W' in str1 or 'W' in str2:
        return not strict
    return False