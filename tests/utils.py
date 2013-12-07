def eq_(val1, val2, message=None):
    if type(val1) == type(val2) == float:
        if abs(val1 - val2) < 0.001:
            return
    else:
        if val1 == val2:
            return

    if message is None:
        message = "{} != {}".format(val1, val2)
    raise AssertionError(message)

def neq_(val1, val2, message=None):
    if val1 != val2:
        return

    if message is None:
        message = "{} == {}".format(val1, val2)
    raise AssertionError(message)

def gt_(val1, val2, message=None):
    if val1 > val2:
        return

    if message is None:
        message = "{} <= {}".format(val1, val2)
    raise AssertionError(message)

def gteq_(val1, val2, message=None):
    if val1 >= val2:
        return

    if message is None:
        message = "{} < {}".format(val1, val2)
    raise AssertionError(message)

def lt_(val1, val2, message=None):
    if val1 < val2:
        return

    if message is None:
        message = "{} >= {}".format(val1, val2)
    raise AssertionError(message)

def in_(val, lst, message=None):
    if val in lst:
        return

    if message is None:
        message = "{} not in {}".format(val, lst)
    raise AssertionError(message)
