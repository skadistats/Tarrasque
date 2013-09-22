from .entity import *
from .properties import *
from .consts import *

@register_entity("DT_DOTA_Item")
@register_entity_wildcard("DT_DOTA_Item_*")
class Item(DotaEntity):
    """
    Item class
    """

    
    off_cooldown_time = Property('DT_DOTABaseAbility', 'm_fCooldown')
    """
    The time when the item will come off cooldown
    """
    
    @property
    def is_on_cooldown(self):
        current_time = self.stream_binding.info.game_time
        return current_time <= self.off_cooldown_time
    

    cooldown_length = Property('DT_DOTABaseAbility', 'm_flCooldownLength')
    """
    These are all the same as the functions in the ability class,
    I'm lazy, go read them, they are fairly self-explanatory :D
    """

    mana_cost = Property('DT_DOTABaseAbility', 'm_iManaCost')

    cast_range = Property('DT_DOTABaseAbility', 'm_iCastRange')

    purchase_time = Property('DT_DOTA_Item', 'm_flPurchaseTime')
    """
    The time when the item was purchased
    """
    
    droppable = Property('DT_DOTA_Item', 'm_bDroppable')
    """
    Presumably if the item is droppable (ex: not Aegis)
    """

    initial_charges = Property('DT_DOTA_Item', 'm_iInitialCharges')
    """
    Presumably charges when item is bought (ex: 8 for diffusal)
    """
    
    sharability = Property('DT_DOTA_Item', 'm_iSharability')
    """
    Presumably whether the item can be shared (ex: Tango, RoH)
    """
    
    current_charges = Property('DT_DOTA_Item', 'm_iCurrentCharges')
    """
    Presumably the item's current charges (ex: 7 for Diffusal if used once)
    """
    
    requires_charges = Property('DT_DOTA_Item', 'm_bRequiresCharges')
    """
    Presumably whether the item needs charges to work (ex: Diffusal)
    """

    sellable = Property('DT_DOTA_Item', 'm_bSellable')
    """
    Presumably whether the item can be sold or not (ex: Not BKB)
    """
    
    stackable = Property('DT_DOTA_Item', 'm_bStackable')
    """
    Presumably whether the item can be stacked (ex: Wards)
    """
    
    disassemblable = Property('DT_DOTA_Item', 'm_bDisassemblable')
    """
    Presumably whether you can disassemble the item (ex: Arcane Boots)
    """
    
    killable = Property('DT_DOTA_Item', 'm_bKillable')
    """
    Presumably whether the item can be denied (ex: not Gem)
    """
    
    permanent = Property('DT_DOTA_Item', 'm_bPermanent')
    """
    Seems to be if the item will disappear when it runs out of stacks
    (i.e consumable. Ex: Tango, not Diffusal)
    """
    
    alertable = Property('DT_DOTA_Item', 'm_bAlertable')
    """
    Presumably whether you can right-click 'Alert allies' with it
    (ex: Smoke, Arcane Boots, 'Gather for Arcane Boots here!')
    """

    purchasable = Property('DT_DOTA_Item', 'm_bPurchasable')
    """
    Presumably whether you can buy the item or not (ex: not Aegis)
    """
    
    recipe = Property('DT_DOTA_Item', 'm_bRecipe')
    """
    Presumably whether the item is a recipe or not (ex: any Recipe)
    """

    purchaser = Property('DT_DOTA_Item', 'm_hPurchaser')\
                .apply(EntityTrans())
    """
    The hero object of the purchaser of the item
    """
    
    def __repr__(self):
        if self.name:
            return "Item('{}')".format(self.name)
        else:
            return super(Item, self).__repr__()
