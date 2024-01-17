import time
import random as rd

import NPC.status as buffs


# Funciones que ayudan en otras funciones
def calculate_normal_attack_damage(npc_arg, player_arg, damage_modifier):
    damage = (npc_arg.attack_points * damage_modifier)
    damage = round(damage, 0)
    damage -= player_arg.defense_points
    damage = round(damage, 0)
    if damage <= 0:
        damage = 0
    return damage

def calculate_magic_attack_damage(npc_arg, player_arg, damage_modifier):
    damage = (npc_arg.magic_attack_points * damage_modifier)
    damage = round(damage, 0)
    damage -= player_arg.defense_points
    damage = round(damage, 0)
    if damage <= 0:
        damage = 0
    return damage

def reduce_stamina_by_percent(player_arg, stamina_reduction_percent):
    sp_lost = player_arg.max_sp * stamina_reduction_percent
    player_arg.sp -= sp_lost
    if player_arg.sp <= 0:
        player_arg.sp = 0
    return player_arg.sp

def reduce_stamina_by_fixed_number(player_arg, stamina_reduction):
    player_arg.sp -= stamina_reduction
    if player_arg.sp <= 0:
        player_arg.sp = 0
    return player_arg.sp

#Skills effects
def use_normal_attack(npc_arg, player_arg):
    damage = calculate_normal_attack_damage(npc_arg, player_arg, 1)
    player_arg.hp -= damage
    time.sleep(1)
    print(f"\n...{npc_arg.name} makes an attack of {damage} attack points...")
    return player_arg.hp

def use_magic_attack(npc_arg, player_arg):
    damage = calculate_magic_attack_damage(npc_arg, player_arg, 1)
    player_arg.hp -= damage
    time.sleep(1)
    print(f"\n...{npc_arg.name} makes a magic attack of {damage} attack points...")
    return player_arg.hp

def double_strength(npc_arg):
    time.sleep(1)
    print(f"\n¡{npc_arg.name} goes berserk!...")
    strength_buff = buffs.StrengthUp("Fury", 3, npc_arg, True, npc_arg.strength)
    time.sleep(1)
    print(f"\n...{npc_arg.name} has increased its Strength by {npc_arg.strength} points(s)...")
    return npc_arg.strength

def increase_magic_defense_by_50_points(npc_arg):
    magic_defense_buff = buffs.MagicDefenseUp("Magic Resistance Up", 4, npc_arg, True, 50)
    print(f"{npc_arg.name} has increased its Magic Defense by 50 points")
    return npc_arg.magic_defense_points

def increase_defense_by_50_points(npc_arg):
    defense_buff = buffs.DefenseUp("Magic Resistance Up", 2, npc_arg, True, 50)
    print(f"{npc_arg.name} has increased its Defense by 50 points")
    return npc_arg.defense_points


def allmigthy_push(npc_arg, player_arg):
    time.sleep(1)
    print(f"\n...{npc_arg.name} charges against your character...")
    time.sleep(1)
    if npc_arg.strength > player_arg.strength:
        sp_lost = reduce_stamina_by_percent(player_arg, 0.3)
        player_arg.sp -= sp_lost
        if player_arg.sp <= 0:
            player_arg.sp = 0
        print(f"\nYour character loses {sp_lost} stamina points!")
    else:
        sp_lost = 0
        print(f"The enemy fails to knock down your character")
    return player_arg.sp

def fireball(npc_arg, player_arg):
    damage = calculate_magic_attack_damage(npc_arg, player_arg, 2)
    player_arg.hp -= damage
    time.sleep(1)
    print(f"\n...{npc_arg.name} makes a magic attack of {damage} attack points...")
    return player_arg.hp

def charge(npc_arg, player_arg):
    time.sleep(1)
    print(f"\n...{npc_arg.name} prepares to charge...")
    time.sleep(1)
    dmg_mod = 3
    if npc_arg.agility >= player_arg.agility:
        hit_chance = 0.8
    elif npc_arg.agility < player_arg.agility:
        hit_chance = 0.3
    events = [True, False]
    probabilities = [hit_chance, (1 - hit_chance)]
    result = rd.choices(events, probabilities)
    if result == [True]:
        damage = calculate_normal_attack_damage(npc_arg, player_arg, dmg_mod)
        print(f"\n...{npc_arg.name} hits you, causing {damage} damage points...")
    elif result == [False]:
        damage = 0
        print(f"\n...{npc_arg.name} fails to hit you, causing no damage")
    player_arg.hp -= damage
    return player_arg.hp

def recover_hp_passive(npc_arg):
    if npc_arg.hp < npc_arg.max_hp:
        hp_restored_per_turn = (npc_arg.max_hp * 0.1)
        npc_arg.hp += hp_restored_per_turn
        if npc_arg.hp > npc_arg.max_hp:
            npc_arg.hp = npc_arg.max_hp
        print(f"{npc_arg.name} passively recovers {hp_restored_per_turn} health points")
    return

def recover_mp_passive(npc_arg):
    if npc_arg.mp < npc_arg.max_mp:
        mp_restored_per_turn = (npc_arg.max_mp * 0.1)
        npc_arg.mp += mp_restored_per_turn
        if npc_arg.mp > npc_arg.max_mp:
            npc_arg.mp = npc_arg.max_mp
        print(f"{npc_arg.name} passively recovers {mp_restored_per_turn} mana points")
    return

def melee_attack_that_decreases_mana_from_player(npc_arg, player_arg):
    damage_to_player_arg_mp = calculate_normal_attack_damage(npc_arg, player_arg, 2)
    player_arg.mp -= damage_to_player_arg_mp
    if player_arg.mp < 0:
        player_arg.mp = 0
    time.sleep(1)
    print(f"¡{npc_arg.name} attack consumes {damage_to_player_arg_mp} mana points from your character!")
    return