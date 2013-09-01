def eq_(val1, val2, message=None):
  if val1 == val2:
    return

  if message is None:
    message = "{} != {}".format(val1, val2)
  raise AssertionError(message)

def gt_(val1, val2, message=None):
  if val1 > val2:
    return

  if message is None:
    message = "{} <= {}".format(val1, val2)
  raise AssertionError(message)

def lt_(val1, val2, message=None):
  if val1 < val2:
    return

  if message is None:
    message = "{} >= {}".format(val1, val2)
  raise AssertionError(message)
