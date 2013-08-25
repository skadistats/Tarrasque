from .consts import *
from .utils import *

class BaseProperty(object):
  exposed = True

  def get_value(self, entity):
    raise NotImplementedError()

  def __get__(self, entity, objtype=None):
    if not self.exposed:
      return self

    # Check if we're chaining the thing
    if issubclass(type(entity), BaseProperty) or entity is None:
      return self
    # Otherwise run the property
    else:
      val = self.get_value(entity)
      if isinstance(val, long):
        return int(val)
      return val

  def map(self, chained):
    self.exposed = False

    map_prop = self
    class MapProperty(ArrayProperty):
      def __init__(self):
        return

      def get_value(self, entity):
        vals = map_prop.get_value(entity)
        if vals is None:
          return

        output = []
        for value in vals:
          class PseudoProp(object):
            def get_value(self, entity):
              return value
          chained.chained = PseudoProp()
          output.append(chained.get_value(entity))
        return output
    return MapProperty()

  def filter(self, filter_func):
    self.exposed = False

    array_prop = self
    class FilterProperty(ArrayProperty):
      def __init__(self):
        return

      def get_value(self, entity):
        output = []
        vals = array_prop.get_value(entity)
        if vals is None:
          return

        for value in vals:
          if filter_func(value):
            output.append(value)
        return output
    return FilterProperty()

class ProviderProperty(BaseProperty):
  def used_by(self, chainer):
    chainer.set_chained(self)
    self.exposed = True
    return chainer

class LocalProperty(ProviderProperty):
  def get_value(self, entity):
      return entity.properties

class RemoteProperty(ProviderProperty):
  def __init__(self, dt_name):
    self.dt = dt_name

  def get_value(self, entity):
    world = entity.world
    _, properties = world.find_by_dt(self.dt)
    return properties

class ExtractorProperty(BaseProperty):
  chained = LocalProperty()

  def set_chained(self, chained):
    self.chained = chained

  def apply(self, chained):
    chained.set_chained(self)
    self.exposed = False
    return chained

class ValueProperty(ExtractorProperty):
  def __init__(self, dt_class, dt_prop):
    self.key = (dt_class, dt_prop)

  def get_value(self, entity):
    props = self.chained.get_value(entity)
    return props[self.key]

Property = ValueProperty

class ArrayProperty(ExtractorProperty):
  def __init__(self, dt_class, dt_prop, array_length=32):
    self.array_length = array_length
    self.key = (dt_class, dt_prop)

  def get_value(self, entity):
    props = self.chained.get_value(entity)
    output = []
    for i in range(self.array_length):
      index_key = "%04d" % i
      # key = (self.key[0], self.key[1] + "." + index_key)
      key = (self.key[1], index_key)
      output.append(props[key])
    return output

class IndexedProperty(ExtractorProperty):
  def __init__(self, dt_class, dt_prop, index_val="index"):
    self.index_val = index_val
    self.key = (dt_class, dt_prop)

  def get_value(self, entity):
    props = self.chained.get_value(entity)
    if props is None:
      return

    index = getattr(entity, self.index_val)
    if index is None:
      return

    return props[(self.key[1], "%04d" % index)]

class PositionProperty(ExtractorProperty):
  def __init__(self, property_class, cellbits_class="DT_BaseEntity"):
    self.prop = property_class
    self.cellbits_class = cellbits_class

  def get_value(self, entity):
    prop = self.chained.get_value(entity)
    if prop is None:
      return

    cell_x = prop[(self.prop, "m_cellX")]
    cell_y = prop[(self.prop, "m_cellY")]
    offset_x, offset_y = prop[(self.prop, "m_vecOrigin")]
    cellbits = prop[(self.cellbits_class, "m_cellbits")]

    return cell_to_coords(cell_x, cell_y, offset_x, offset_y, cellbits)

class TransformerProperty(BaseProperty):
  chained = None

  def set_chained(self, chained):
    self.chained = chained

class MapTrans(TransformerProperty):
  def __init__(self, value_map):
    self.value_map = value_map

  def get_value(self, entity):
    raw = self.chained.get_value(entity)
    if raw is None:
      return

    return self.value_map[raw]

class FuncTrans(TransformerProperty):
  def __init__(self, value_func):
    self.value_func = value_func

  def get_value(self, entity):
    raw = self.chained.get_value(entity)
    if raw is None:
      return

    return self.value_func(raw)

class EntityTrans(TransformerProperty):
  def __init__(self, passed=None, set=None):
    self.passed = passed or dict()
    self.set = set or dict()

  def get_value(self, entity):
    # Hopefully an ehandle
    ehandle = self.chained.get_value(entity)
    if ehandle == NEGATIVE or ehandle == None:
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

    return entity.create_default_class(dt, world)
