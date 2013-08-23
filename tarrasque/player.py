from .entity import *
from .consts import *
from .properties import *

class PlayerResourceProperty(ArrayProperty):
  def get_property(self, entity):
    index = getattr(entity, self.index_var)
    if index == NEGATIVE:
      return None

    ehandle, properties = entity.world.find_by_dt("DT_DOTA_PlayerResource")

    # Work around a bug in skadi
    key = (self.property_key[1], "%04d" % index)
    return properties[key]

@register_entity("DT_DOTAPlayer")
class Player(DotaEntity):
  index = Property("DT_DOTAPlayer", "m_iPlayerID")\
    .apply(FuncTrans(lambda i: None if i == -1 else i))

  hero = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_hSelectedHero"))\
    .apply(EntityTrans(set={"self": "player"}))

  reliable_gold = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iReliableGold"))

  unreliable_gold = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iUnreliableGold"))

  name = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iszPlayerNames"))

  team = RemoteProperty("DT_DOTA_PlayerResource")\
    .used_by(IndexedProperty("DT_DOTA_PlayerResource", "m_iPlayerTeams"))\
    .apply(MapTrans(TEAM_VALUES))

  @property
  def total_gold(self):
    return self.reliable_gold + self.unreliable_gold
