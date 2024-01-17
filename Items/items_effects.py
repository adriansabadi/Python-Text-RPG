def recover_all_lvl_1(player):
    player.sp += 10
    player.hp += 10
    player.mp += 10
    if player.sp > player.max_sp:
        player.sp = player.max_sp
    if player.hp > player.max_hp:
        player.hp = player.max_hp
    if player.mp > player.max_mp:
        player.mp = player.max_mp
    print(f"Character recovers {10} health points, {10} mana points y {10} stamina points")
    return

def recover_energy_item_lvl_1(player):
    player.sp += 20
    if player.sp > player.max_sp:
        player.sp = player.max_sp
    print(f"Character recovers {20} stamina points")
    return player.sp

def recover_life_item_lvl_1(player):
    player.hp += 20
    if player.hp > player.max_hp:
        player.hp = player.max_hp
    print(f"Character recovers {20} health points")
    return player.hp
