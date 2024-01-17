from Items.items import MeleeWeaponClass
from Items.items import RangedWeaponClass


wp_000 = MeleeWeaponClass("Dagger", "A steel dagger", 0, 10, 0.1)
wp_001 = MeleeWeaponClass("Iron sword", "An iron sword, good for squires", 20, 12, 0.2)
wp_002 = RangedWeaponClass("Hunting Bow", "The bow used by hunters troughout the kingdom ", 0, 8, 0.1)
wp_003 = RangedWeaponClass("Yew Crossbow", "Crossbow used by he royal army", 40, 24, 0.4)
wp_004 = MeleeWeaponClass("Champion's Sword", "Sword that only the best deserve", 1000, 100, 0.2)


store_melee_weapons = [wp_001, wp_004]
store_ranged_weapons = [wp_003]