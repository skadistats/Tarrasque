from .consts import *

class BaseProperty(object):
  def get_property(self, entity):
    raise NotImplementedError()

  def __get__(self, entity, objtype=None):
    # Check if we're chaining the thing
    if isinstance(entity, type(BaseProperty)):
      return self
    # Otherwise run the property
    else:
      return self.get_property(entity)

  def is_ehandle(self, passed=None):
    if passed is None:
      passed = []

    return EHandleProperty(self, passed)

class EHandleProperty(BaseProperty):
  def __init__(self, chained_from, passed):
    self.chained = chained_from
    self.passed = passed or {}

  def get_property(self, entity):
    assert entity.world, "EHandleProperty must be on class with stream binding"

    # Hopefully an ehandle
    ehandle = self.chained.get_property(entity)
    if ehandle == NEGATIVE:
      return
    kwargs = {}
    kwargs["ehandle"] = ehandle
    kwargs["stream_binding"] = entity.stream_binding
    for from_, to_ in self.passed.items():
      if from_ == "self":
        kwargs[to_] = entity
      else:
        kwargs[to_] = getattr(entity, from_)

    target = self._find_target(ehandle, entity.world)

    return target(**kwargs)

  def _find_target(self, ehandle, world):
    from . import entity
    dt = world.recv_tables[world.classes[ehandle]].dt
    if dt in entity.ENTITY_CLASSES:
      return entity.ENTITY_CLASSES[dt]
    for regexp, cls in entity.ENTITY_WILDCARDS:
      if regexp.match(dt):
        return cls

    return entity.create_default_class(dt_name, world)

class Property(BaseProperty):
  def __init__(self, property_class, property_name):
    self.property_key = (property_class, property_name)

  def get_property(self, entity):
    return entity.properties[self.property_key]

class ArrayProperty(Property):
  def __init__(self, property_class, property_name, index_var="index"):
    self.index_var = index_var
    Property.__init__(self, property_class, property_name)

  def get_property(self, entity):
    index = getattr(entity, self.index_var)

    # Work around a bug in skadi
    key = (self.property_key[1], "%04d" % index)
    return entity.properties[key]
