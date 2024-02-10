from Items.items import MeleeWeaponClass
from Items.items import RangedWeaponClass


wp_000 = MeleeWeaponClass("Dagger", "A steel dagger", 0, 8, 0.1)
wp_001 = MeleeWeaponClass("Iron sword", "An iron sword, good for squires", 30, 12, 0.2)
wp_002 = RangedWeaponClass("Hunting Bow", "The bow used by hunters trough the kingdom ", 0, 8, 0.1)
wp_003 = RangedWeaponClass("Heavy Crossbow", "Crossbow used by he royal army", 80, 24, 0.4)
wp_004 = MeleeWeaponClass("Steel Sword", "A very well made steel sword, perfect for combat", 160, 40, 0.2)
wp_005 = RangedWeaponClass("Yew Longbow", "The most lethal long range weapon", 240, 80, 0.3)
wp_006 = MeleeWeaponClass("Champion's Sword", "Sword that only the best deserve", 300, 100, 0.3)


store_melee_weapons = [wp_001, wp_004, wp_006]
store_ranged_weapons = [wp_003, wp_005]