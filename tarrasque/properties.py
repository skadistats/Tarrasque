from .consts import *
from .utils import *

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

  def is_ehandle(self, passed=None, set=None):
    if passed is None:
      passed = {}
    if set is None:
      set = {}

    return EHandleProperty(self, passed, set)

  def value_map(self, value_map):
    chained = self
    class ValueMapProperty(BaseProperty):
      def get_property(self, entity):
        value = chained.get_property(entity)
        if value in value_map:
          return value_map[value]
        else:
          raise ValueError("Unknown value map value {}".format(value))
    return ValueMapProperty()

class EHandleProperty(BaseProperty):
  def __init__(self, chained_from, passed, set):
    self.chained = chained_from
    self.passed = passed
    self.set = set

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

    instance = target(**kwargs)

    for from_, to_ in self.set.items():
      if from_ == "self":
        setattr(instance, to_, entity)
      else:
        setattr(instance, to_, getattr(entity, from_))

    return instance

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
    if index == NEGATIVE:
      return None

    # Work around a bug in skadi
    key = (self.property_key[1], "%04d" % index)
    return entity.properties[key]

class PositionProperty(BaseProperty):
  def __init__(self, property_class, cellbits_class="DT_BaseEntity"):
    self.prop = property_class
    self.cellbits_class = cellbits_class

  def get_property(self, entity):
    prop = entity.properties
    cell_x = prop[(self.prop, "m_cellX")]
    cell_y = prop[(self.prop, "m_cellY")]
    offset_x, offset_y = prop[(self.prop, "m_vecOrigin")]
    cellbits = prop[(self.cellbits_class, "m_cellbits")]

    return cell_to_coords(cell_x, cell_y, offset_x, offset_y, cellbits)