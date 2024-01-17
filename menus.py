import os
import random as rd
import time
import math as mt

import Player.players as pl
import Items.weapons as wp
import Items.armors as ar
import Items.consumables as co


def print_preview_info_from_items_in_shop(item_list_arg:list, title:str):
    os.system('cls')
    print(title)
    i = 0
    for item in item_list_arg:
        item.print_item_shop_preview_info(i)
        i += 1

def purchase_dialog(player_arg:pl.PlayerClass, item_list_arg:list, item_index_in_list:int):
    try:
        while True:
            os.system('cls')
            selected_item = item_list_arg[item_index_in_list]
            selected_item.print_item_details()
            print(f"COST: {selected_item.item_buy_cost} coins")
            print("Do you wish to buy this item?\nYes(Y) or No(N):")
            user_choice = input("> ").strip().lower()
            if user_choice == "y":
                selected_item.buy_this_item(player_arg)
                time.sleep(2)
                break
            elif user_choice == "n":
                break
            else:
                time.sleep(1)
                print("Type Y or N")
                time.sleep(1)
    except ValueError:
        print("VALUE ERROR")
        time.sleep(4)
    except IndexError:
        print("INDEX ERROR")
        time.sleep(4)

def print_a_shop(player_arg:pl.PlayerClass, list_arg:list, title:str):
    while True:
            print_preview_info_from_items_in_shop(list_arg, title)
            user_choice = input("Select an object:\n> ").strip().lower()
            if user_choice == "-e" :
                break
            elif user_choice.isdecimal():
                purchase_dialog(player_arg, list_arg, int(user_choice)) 
            else:
                os.system('cls')
                time.sleep(1)
                print("Please type one of the options")
                time.sleep(1)

def print_player_main_stats_page(player_arg:pl.PlayerClass):
    os.system('cls')
    print("Character")
    print(f"Name: {player_arg.player_name}")
    print(f"Level: {player_arg.level}")
    print(f"HP:{player_arg.hp}/{player_arg.max_hp}")
    print(f"MP:{player_arg.mp}/{player_arg.max_mp}")
    print(f"SP:{player_arg.sp}/{player_arg.max_sp}")
    print(f"Coins: {player_arg.coins}")
    print(f"Health Flasks: {player_arg.flask_life}")
    print(f"Mana Flasks: {player_arg.flask_mana}")
    
def print_player_attributes_page(player_arg:pl.PlayerClass):
    os.system('cls')
    print("Attributes")
    print(f"Strength:{player_arg.base_strength}(+{player_arg.bonus_strength})")
    print(f"Agility:{player_arg.base_agility}(+{player_arg.bonus_agility})")
    print(f"Intelligence:{player_arg.base_intelligence}(+{player_arg.bonus_intelligence})")
    
def print_player_melee_stats_page(player_arg:pl.PlayerClass):
    os.system('cls')
    print("Melee Stats")
    print(f"Weapon name: {player_arg.melee_weapon_slot.item_name}")
    print(f"Weapon attack points:{player_arg.melee_weapon_slot.weapon_attack_points}")
    print(f"Character melee attack points:{player_arg.melee_attack_points}")
    print(f"Critical Melee Chance:{player_arg.melee_critical_chance*100}%")

def print_player_ranged_stats_page(player_arg:pl.PlayerClass):
    os.system('cls')
    print("Ranged Stats")
    print(f"Weapon name: {player_arg.ranged_weapon_slot.item_name}")
    print(f"Weapon attack points:{player_arg.ranged_weapon_slot.weapon_attack_points}")
    print(f"Character ranged attack points:{player_arg.ranged_attack_points}")
    print(f"Critical Ranged Chance:{player_arg.ranged_critical_chance*100}%")

def print_player_spell_stats_page(player_arg:pl.PlayerClass):
    os.system('cls')
    print("Spell Stats")
    print(f"Spell name: {player_arg.combat_spell_slot.spell_name}")
    print(f"Spell attack points: {player_arg.combat_spell_slot.attack_points}")
    print(f"Character magic attack points:{player_arg.magic_attack_points}%")
    print(f"Critical Spell Chance:{player_arg.magic_critical_chance*100}%")

def print_player_armor_stats_page(player_arg:pl.PlayerClass):
    os.system('cls')
    print("Defense Stats")
    print(f"Armor equipped: {player_arg.armor_slot.item_name}")
    print(f"Defense points:{player_arg.defense_points}")


def print_player_overview(player_arg:pl.PlayerClass):
    time.sleep(1)
    os.system('cls')
    print("CHARACTER STATS")
    print("(1) Character main page")
    print("(2) Attributes page")
    print("(3) Melee Stats page")
    print("(4) Ranged Stats page")
    print("(5) Spell Stats page")
    print("(6) Defense Stats page")
    print("(-e) to go back")
    while True:
        user_choice = input("> ").strip().lower()
        match user_choice:
            case "-e":
                break
            case "1":
                print_player_main_stats_page(player_arg)
                print("1/6")
            case "2":
                print_player_attributes_page(player_arg)
                print("2/6")
            case "3":
                print_player_melee_stats_page(player_arg)
                print("3/6")
            case "4":
                print_player_ranged_stats_page(player_arg)
                print("4/6")
            case "5":
                print_player_spell_stats_page(player_arg)
                print("5/6")
            case "6":
                print_player_armor_stats_page(player_arg)
                print("6/6")
            case _:
                print("Please type one of the options")
                time.sleep(1)
                continue

def print_commands():
    print('''
COMMANDS
(a) use a melee attack
(d) use a ranged attack
(m) use a magic attack
(s) use a support spell
(h) use a heal flask
(j) use a mana flask
(r) pass the turn and recover stamina points
(i) select and use a consumable item from inventory
(1) select a melee weapon to equip on the melee weapon slot
(2) select a ranged weapon to equip on the ranged weapon slot
(3) select an armor to equip on the armor slot
(4) select a spell to equip on the combat  spell slot
(5) show player stats overview
(6) show player status
(7) show full enemy info    
''')

def upgrade_flasks_menu(player_arg:pl.PlayerClass):
    while True:
        if player_arg.flask_upgrade_level <= 4:
            print("UPGRADE FLASKS")
            print("Type Y for upgrade or N to go back")
            upgrade_cost = 10 ** (player_arg.flask_upgrade_level + 2) 
            print(f"UPGRADE COST: {upgrade_cost}")
            user_choice = input("> ").strip().lower()
            if player_arg.coins >= upgrade_cost:
                match user_choice:
                    case "y":
                        player_arg.flask_upgrade_level += 1
                        print(f"Flask upgrade level: {player_arg.flask_upgrade_level}")
                    case "n":
                        break
                    case _:
                        print("Please type Y or N")
                        time.sleep(2)
                        continue
        else:
            print("You have reached the max upgrade level")
            time.sleep(2)
            break

def attributes_menu(player_arg:pl.PlayerClass):
    while True:
        os.system('cls')
        print("ATTRIBUTES")
        print(f"Strength(F):{player_arg.strength} ")
        print(f"Agility(A):{player_arg.agility}")
        print(f"Intelligence(I):{player_arg.intelligence}")
        print(f"Available attribute points: {player_arg.atribute_points}")
        user_choice = input("Type the desired attribute or -e to go back\n> ").strip().lower()
        if user_choice == "-e":
            break
        else:
            if player_arg.atribute_points >= 1:
                match user_choice:
                    case "f":
                        player_arg.add_strength()
                    case "a":
                        player_arg.add_agility()
                    case "i":
                        player_arg.add_intelligence()
                    case _:
                        os.system('cls')
                        print("Please type one of the options")
                        time.sleep(2)
                        continue
                print(f"Remaining attribute points: {player_arg.atribute_points}")
                time.sleep(2)
            elif player_arg.atribute_points < 1:
                os.system('cls')
                print("\nNO ATTRIBUTE POINTS AVAILABLE")
                time.sleep(2)
                print("Level up to get more attribute points\n")
                time.sleep(2)
                continue

def shops_menu(player_arg):
    while True:
        os.system('cls')
        print('''SHOPS
1. MELEE WEAPONS
2. RANGED WEAPONS
3. ARMORS
4. ITEMS''')
        user_choice = input("> ").strip().lower()
        match user_choice:
            case "1":
                print_a_shop(player_arg, wp.store_melee_weapons, "MELEE WEAPONS")
            case "2":
                print_a_shop(player_arg, wp.store_ranged_weapons, "RANGED WEAPONS")
            case "3":
                print_a_shop(player_arg, ar.store_armor, "ARMORS")
            case "4":
                print_a_shop(player_arg, co.misc_items_shop, "ITEMS")
            case "-e":
                break
            case _:
                print("\nType one of the options\n")





