from Items.items import MeleeWeaponClass
from Items.items import RangedWeaponClass


wp_000 = MeleeWeaponClass("Dagger", "Dummy Text", 0, 10, 0.1)
wp_001 = MeleeWeaponClass("Iron sword", "Dummy Text", 20, 12, 0.2)
wp_002 = RangedWeaponClass("Hunting Bow", "Dummy Text", 0, 8, 0.1)
wp_003 = RangedWeaponClass("Yew Crossbow", "Dummy Text", 40, 24, 0.4)
wp_004 = MeleeWeaponClass("Champion's Sword", "Dummy Text", 1000, 100, 0.2)


store_melee_weapons = [wp_001, wp_004]
store_ranged_weapons = [wp_003]