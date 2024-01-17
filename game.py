import os
import time
import random as rd

import Items.items as it
import Player.players as pl
import NPC.enemies as en
import menus as me


def end_of_turn_actions(player_arg:pl.PlayerClass, enemy_target_arg:en.HostileNPC):
    player_arg.update_buffs_duration()
    player_arg.update_spells_cooldown()
    enemy_target_arg.update_buffs_duration()
    enemy_target_arg.update_skills_cooldown()
    return

def player_victory_reward(player_arg:pl.PlayerClass, enemy_target:en.HostileNPC):
    time.sleep(2)
    player_arg.coins += enemy_target.coins_drop
    player_arg.experience += enemy_target.experience_reward
    print(f"+{enemy_target.coins_drop} coins")
    print(f"+{enemy_target.experience_reward} experience")
    time.sleep(2)
    player_arg.restore_player_after_victory()
    player_arg.check_experience_to_decide_if_level_up()
    time.sleep(4)
    return

def check_victory_conditions(player_arg:pl.PlayerClass, enemy_target:en.HostileNPC):
    battle_is_ongoing = True
    #VICTORY CONDITIONS
    if enemy_target.hp <= 0:
        time.sleep(1)
        print("VICTORY")
        player_victory_reward(player_arg, enemy_target)
        battle_is_ongoing = False
    #DEFEAT CONDITIONS
    elif player.hp <= 0:
        print("DEFEAT")
        time.sleep(3)
        battle_is_ongoing = False
    return battle_is_ongoing

def print_general_info(player_arg:pl.PlayerClass, enemy_target:en.HostileNPC, battle_turn_arg):
    print(f'''///___________________TURN: {battle_turn_arg}___________________|
-----PLAYER STATS--------------------------
PLAYER NAME: {player_arg.player_name}
PLAYER HP: {player_arg.hp}/{player_arg.max_hp}
PLAYER MP: {player_arg.mp}/{player_arg.max_mp}
-----ENEMY STATS---------------------------
ENEMY NAME: {enemy_target.name}
ENEMY HP: {enemy_target.hp}/{enemy_target.max_hp}
ENEMY MP: {enemy_target.mp}/{enemy_target.max_mp}''')

def print_enemy_info(enemy_target:en.HostileNPC):
    print(f"ENEMY NAME: {enemy_target.name}")
    print(f"ENEMY HP: {enemy_target.hp}/{enemy_target.max_hp}")
    print(f"ENEMY MP: {enemy_target.mp}/{enemy_target.max_mp}")
    print(f"ENEMY ATTACK POINTS: {enemy_target.attack_points}")
    print(f"ENEMY MAGIC ATTACK POINTS: {enemy_target.magic_attack_points}")
    print(f"ENEMY DEFENSE POINTS: {enemy_target.defense_points}")
    print(f"ENEMY STRENGTH: {enemy_target.base_strength}(+{enemy_target.bonus_strength})")
    print(f"ENEMY AGILITY: {enemy_target.base_agility}(+{enemy_target.bonus_agility})")
    print(f"ENEMY INTELLIGENCE: {enemy_target.base_agility}(+{enemy_target.bonus_agility})")
    enemy_target.print_enemy_status()

def choose_player_action_in_battle(player_arg:pl.PlayerClass, enemy_target_arg:en.HostileNPC):
    player_move = True
    action = input("ACTION:\n> ").strip().lower() 
    match action:
        case "1":
            player_arg.select_item_to_equip(it.MeleeWeaponClass, "MELEE WEAPONS")
        case "2":
            player_arg.select_item_to_equip(it.RangedWeaponClass, "RANGED WEAPONS")
        case "3":
            player_arg.select_item_to_equip(it.ArmorClass, "ARMORS")
        case "4":
            player_arg.select_combat_spell()
        case "5":
            me.print_player_overview(player_arg)
        case "6":
            player_arg.print_player_status()
        case "7":
            print_enemy_info(enemy_target_arg)
        case "a":
            if player_arg.sp == 0:
                print("\nNO STAMINA\n")
                time.sleep(1)
            elif player_arg.sp >= (player_arg.max_sp * player_arg.melee_weapon_slot.stamina_cost):
                enemy_target_arg.hp = player_arg.use_melee_attack(enemy_target_arg)
                player_move = False
            else:
                print("\nNOT ENOUGH STAMINA POINTS\n")
                time.sleep(1)
        case "d":
            if player_arg.sp == 0:
                print("\nNO STAMINA\n")
                time.sleep(1)
            elif player_arg.sp >= (player_arg.max_sp * player_arg.ranged_weapon_slot.stamina_cost):
                enemy_target_arg.hp = player_arg.use_ranged_attack(enemy_target_arg)
                player_move = False
            else:
                print("\nNOT ENOUGH STAMINA POINTS\n")
                time.sleep(1)
        case "h":
            player_arg.use_life_flask()
        case "i":
            player_arg.use_a_consumable_item()
        case "j":
            player_arg.use_mana_flask()
        case "m":
            if player_arg.mp == 0:
                print("\nNO MANA POINTS\n")
            elif player_arg.mp >= player_arg.combat_spell_slot.mana_cost:
                enemy_target_arg.hp = player_arg.use_combat_spell(enemy_target_arg)
                player_move = False
            elif player_arg.mp < player_arg.combat_spell_slot.mana_cost:
                print("\nNOT ENOUGH MANA POINTS\n")
        case "r":
            player_arg.recover_breath()
            player_move = False
            return player_move
        case "s":
            player_arg.use_a_support_spell(enemy_target_arg)
        case "-help":
            me.print_commands()
        case _:
            print("Type one of the options")
    return player_move

def go_to_battle(player_arg:pl.PlayerClass):
    enemy_target = en.enemy_wave_1()
    turn = 1
    player_move = True
    battle_is_ongoing = True
    while battle_is_ongoing == True:
        # PLAYER TURN
        while player_move == True and battle_is_ongoing == True:
            print_general_info(player_arg, enemy_target, turn)
            print("Type -help to see the commands")
            # SELECTING PLAYER MOVE
            # If the selected action finishes player turn, returns player_move as False
            player_move = choose_player_action_in_battle(player_arg, enemy_target)
            # CHECKING THAT BATTLE IS NOT OVER AT THE END OF PLAYER TURN
            battle_is_ongoing = check_victory_conditions(player_arg, enemy_target)

        # ENEMY NPC TURN
        while player_move != True and battle_is_ongoing == True:
            print(f"\nTURN: {turn}")
            print_general_info(player_arg, enemy_target, turn)
            player_arg.natural_regeneration_after_each_turn()
            enemy_target.use_actions(player_arg)
            enemy_target.use_turn_based_passive_v1()
            # CHECKING THAT BATTLE IS NOT OVER AT THE END OF ENEMY TURN
            battle_is_ongoing = check_victory_conditions(player_arg, enemy_target)
            # DOING ACTIONS LIKE UPDATING SKILLS COOLDOWN AT THE END OF THE BATTLE TURN
            end_of_turn_actions(player_arg, enemy_target)
            # INCREASING TURN AND GOING BACK TO PLAYER TURN
            turn += 1
            player_move = True

def main(player_arg:pl.PlayerClass):
    while True:
        os.system('cls')
        print("\nRPG TEXT ADVENTURE")
        print('''MAIN MENU
Select what to do
(1) Next battle
(2) Show character stats
(3) Atributes
(4) Store
(5) Exit''')
        user_choice = input("> ").strip().lower()
        match user_choice:
            case "1":
                os.system('cls')
                time.sleep(1)
                go_to_battle(player_arg)
            case "2":
                me.print_player_overview(player_arg)
                os.system('cls')
            case "3":
                me.attributes_menu(player_arg)
                os.system('cls')
            case "4":
                me.shops_menu(player_arg)
                os.system('cls')
            case "5":
                os.system('cls')
                print("CLOSING GAME")
                time.sleep(3)
                os.system('cls')
                exit()
            case _:
                print("UNKNOW COMMAND")
                continue

print("WELCOME TO THE GAME")
print("CREATE YOUR CHARACTER\n")
player = pl.PlayerClass(input("Character name:\n"), 4, 4, 4)
print(f"{player.player_name} created")


main(player)