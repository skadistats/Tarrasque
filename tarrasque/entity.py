import inspect
from importlib import import_module
import sys

from .consts import *

class DotaEntity(object):
  def __init__(self, stream_binding, ehandle):
    self.stream_binding = stream_binding
    self.ehandle = ehandle

  @property
  def dt_key(self):
    return self.world.recv_tables[self.world.classes[self.ehandle]].dt

  @property
  def world(self):
    return self.stream_binding.world

  @property
  def tick(self):
    return self.stream_binding.tick

  @property
  def properties(self):
    """
    Return the data associated with the handle for the current tick.
    """
    return self.world.find(self.ehandle)

  @property
  def exists(self):
    try:
      self.world.find(self.ehandle)
    except KeyError:
      return False
    else:
      return True

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

  def targets(self, name, passed=None):
    if passed is None:
      passed = []

    module_name = sys._getframe(4).f_globals['__name__']
    module_file = sys._getframe(4).f_globals.get('__file__')
    return TargetProperty(self, name, module_name, module_file, passed)

class TargetProperty(BaseProperty):
  def __init__(self, chained_from, target_name, module_name, module_file,
               passed):
    self.chained = chained_from
    self.passed = passed or {}

    self.target_name = target_name
    self.module_name = module_name
    self.module_file = module_file

  def _find_target(self, name, module_name, module_file):
    if name.find(".") == -1:
      module = module_name
    else:
      module, _, name = name.rpartition(".")

    if not module in sys.modules:
      if "__init__.py" in module_file:
        namespace = module_name
      else:
        namespace = module_name.rpartition(".")[0]

      if module:
        module = import_module(namespace).__name__
    return getattr(sys.modules[module_name], name)

  def get_property(self, entity):
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

    target = self._find_target(self.target_name, self.module_name,
                               self.module_file)

    return target(**kwargs)

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
