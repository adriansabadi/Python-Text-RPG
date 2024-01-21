import Items.items_effects as ie
from Items.items import ConsumableClass


item_0001 = ConsumableClass("Lesser Stamina Potion", "Recovers SP", 10, ie.recover_energy_item_lvl_1)
item_0002 = ConsumableClass("Minor Recovery Potion","Recovers HP, MP, SP", 30, ie.recover_all_lvl_1)

misc_items_shop = [item_0001, item_0002]