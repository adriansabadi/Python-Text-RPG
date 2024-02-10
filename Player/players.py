import os
import time
import math as mt
import random as rd

import Items.armors as ar
import Items.items as it
import Player.spells as sp
import Items.weapons as wp


class PlayerClass:
    def __init__(self, name, strength_arg, agility_arg, intelligence_arg):
        self.player_name = name
        self.level = 1
        self.experience = 0
        self.attribute_points = 0
        self.status = []
        self.coins = 0
        #  Flasks that player will use to restore character mana and health
        #  The max flasks determines the maximum quantity of flasks available
        #  Flasks get upgraded in another function, up to maximum of 4 times
        #  Flasks values list contains the values restored per upgrade level
        #  If the flasks upgrade level is 4, the value restored will index 4
        self.max_flasks = 2
        self.flask_life = 2
        self.flask_mana = 2
        self.flask_upgrade_level = 0
        self.flask_values_per_upgrade = (20, 40, 60, 80, 100)
        #  Inventory is a list where every item possessed by the character goes
        #  The items are filtered later by functions when they are required
        self.inventory = [wp.wp_002, wp.wp_000, ar.ar_000]
        #  Similar to inventory, spell book list is w
        self.spell_book = [sp.sp_001, sp.sp_002]
        # In the slots goes the items that will be equipped by the character
        # Each of these items determines multiple stats
        self.combat_spell_slot = sp.sp_001
        self.melee_weapon_slot = wp.wp_000
        self.ranged_weapon_slot = wp.wp_002
        self.armor_slot = ar.ar_000
        # Player in-game Attributes
        # Base Attributes
        # Base attributes can't be modified by buffs
        self.base_strength = strength_arg
        self.base_agility = agility_arg
        self.base_intelligence = intelligence_arg
        #  Bonus Attributes
        #  This are the attributes modified by buffs
        self.bonus_strength = 0
        self.bonus_agility = 0
        self.bonus_intelligence = 0
        # Total Attributes
        # Attributes that sum the base and bonus ones
        # This are the ones used by most actions
        self.strength = self.base_strength + self.bonus_strength
        self.agility = self.base_agility + self.bonus_agility
        self.intelligence = self.base_intelligence + self.bonus_intelligence
        #  Primary  Stats
        self.max_hp = 10 + (self.strength*10)  #Player max hit points(hp)
        self.max_mp = (self.intelligence*10)  #Player max mana points(mp)
        self.max_sp = (self.strength*4)  #Player max stamina points(sp)
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.sp = self.max_sp
        #  Secondary Stats
        self.melee_attack_points = 0
        self.ranged_attack_points = 0
        self.melee_critical_chance = 0
        self.ranged_critical_chance = 0
        self.magic_attack_points = 0
        self.magic_critical_chance = 0
        self.defense_points = self.armor_slot.defense_points
        #Bonus stats
        self.bonus_critical_melee = 0
        self.bonus_critical_ranged = 0
        self.bonus_critical_magic_attack_points = 0
        self.bonus_melee_critical_chance = 0
        self.bonus_ranged_critical_chance = 0
        self.bonus_magic_critical_chance = 0
        #Using update_stats function to calculate the stats since instance creation
        self.update_stats()

    # This functions handle the calculation of stats that depend from others
    # These stats are used in others functions
    def calculate_melee_attack_points(self):
        melee_attack_points_mod = 0.9 + (self.strength*0.1)
        self.melee_attack_points = round((self.melee_weapon_slot.weapon_attack_points*melee_attack_points_mod), 0)
        return self.melee_attack_points
    
    def calculate_critical_melee_attack_points(self):
        critical_melee_attack_points_mod = 2.8 + (self.strength*0.2)
        critical_melee_attack_base = round((self.melee_attack_points*critical_melee_attack_points_mod), 0)
        min_critical = round((critical_melee_attack_base - (critical_melee_attack_base*0.1)), 0)
        max_critical = round((critical_melee_attack_base + (critical_melee_attack_base*0.1)), 0)
        critical_melee_attack = rd.randint(min_critical, max_critical)
        return critical_melee_attack
    
    def calculate_ranged_attack_points(self):
        ranged_attack_points_mod = 0.9 + (self.agility*0.1)
        self.ranged_attack_points = round((self.ranged_weapon_slot.weapon_attack_points*ranged_attack_points_mod), 0)
        return self.ranged_attack_points
    
    def calculate_critical_ranged_attack_points(self):
        critical_ranged_attack_points_mod = 2.8 + (self.agility*0.2)
        critical_ranged_attack_base = round((self.ranged_attack_points*critical_ranged_attack_points_mod), 0)
        min_critical = round((critical_ranged_attack_base - (critical_ranged_attack_base*0.1)), 0)
        max_critical = round((critical_ranged_attack_base + (critical_ranged_attack_base*0.1)), 0)
        critical_ranged_attack = rd.randint(min_critical, max_critical)
        return critical_ranged_attack
    
    def calculate_magic_attack_points(self):
        magic_attack_points_mod = 0.9 + (self.intelligence*0.1)
        self.magic_attack_points = round((self.combat_spell_slot.attack_points*magic_attack_points_mod), 0)
        return self.magic_attack_points
    
    def calculate_critical_magic_attack_points(self):
        critical_magic_attack_points_mod = 2.8 + (self.intelligence*0.2)
        critical_magic_attack_points_base = round((self.magic_attack_points*critical_magic_attack_points_mod), 0)
        min_critical = round((critical_magic_attack_points_base - (critical_magic_attack_points_base*0.1)), 0)
        max_critical = round((critical_magic_attack_points_base + (critical_magic_attack_points_base*0.1)), 0)
        critical_magic_attack = rd.randint(min_critical, max_critical)
        return critical_magic_attack

    def calculate_melee_damage(self, enemy):
        damage = round(self.melee_attack_points - enemy.defense_points)
        if damage <= 0:
            damage = 0
        return damage
    
    def calculate_critical_melee_damage(self, enemy):
        damage = self.calculate_critical_melee_attack_points()
        damage = round(damage - enemy.defense_points)
        if damage <= 0:
            damage = 0
        return damage

    def calculate_ranged_damage(self, enemy):
        damage = round(self.ranged_attack_points - enemy.defense_points)
        if damage <= 0:
            damage = 0
        return damage
    
    def calculate_critical_ranged_damage(self, enemy):
        damage = self.calculate_critical_ranged_attack_points()
        damage = round(damage - enemy.defense_points)
        if damage <= 0:
            damage = 0
        return damage
    
    def calculate_magic_damage(self, enemy):
        damage = self.calculate_magic_attack_points()
        damage = round(damage - enemy.defense_points)
        if damage <= 0:
            damage = 0
        return damage
    
    def calculate_critical_magic_damage(self, enemy):
        damage = self.calculate_critical_magic_attack_points()
        damage = round(damage - enemy.defense_points)
        if damage <= 0:
            damage = 0
        return damage
    
    def calculate_melee_critical_chance(self):
        self.melee_critical_chance = round(((self.strength*0.015) + (self.bonus_melee_critical_chance)), 2)
        return self.melee_critical_chance
    
    def calculate_ranged_critical_chance(self):
        self.ranged_critical_chance = round(((self.agility*0.015) + (self.bonus_ranged_critical_chance)), 2)
        return self.ranged_critical_chance
    
    def calculate_magic_critical_chance(self):
        self.magic_critical_chance = round(((self.intelligence*0.015) + (self.bonus_magic_critical_chance)), 2)
        return self.magic_critical_chance
    
    # This functions will trigger or not a critical attack based on probabilities
    def trigger_critical_melee_attack(self):
        self.calculate_melee_critical_chance()
        events = [True, False]
        probabilities = [self.melee_critical_chance, (1 - self.melee_critical_chance)]
        critical_outcome = rd.choices(events, probabilities)
        time.sleep(1)
        if critical_outcome == [True]:
            print("¡¡CRITICAL ATTACK!!")
        else:
            print("...")
        return critical_outcome
    
    def trigger_critical_ranged_attack(self):
        self.calculate_ranged_critical_chance()
        events = [True, False]
        probabilities = [self.ranged_critical_chance, (1 - self.ranged_critical_chance)]
        critical_outcome = rd.choices(events, probabilities)
        time.sleep(1)
        if critical_outcome == [True]:
            print("¡¡CRITICAL ATTACK!!")
        else:
            print("...")
        return critical_outcome

    def trigger_critical_magic_attack(self):
        self.calculate_magic_critical_chance()
        events = [True, False]
        probabilities = [self.magic_critical_chance, (1 - self.magic_critical_chance)]
        critical_outcome = rd.choices(events, probabilities)
        time.sleep(1)
        if critical_outcome == [True]:
            print("¡¡CRITICAL ATTACK!!")
        else:
            print("...")
        return critical_outcome
    
    #  Its objective is to update the stats each time a change is produced
    #  It may be when an item its equipped or a buff affects the character
    def update_stats(self):
        self.strength = self.base_strength + self.bonus_strength
        self.agility = self.base_agility + self.bonus_agility
        self.intelligence = self.base_intelligence + self.bonus_intelligence

        self.max_hp = 10 + (self.strength*10)
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        self.max_mp = (self.intelligence*10)
        if self.mp > self.max_mp:
            self.mp = self.max_mp
        self.max_sp = (self.strength*4)
        if self.sp > self.max_sp:
            self.sp = self.max_sp

        self.melee_attack_points = self.calculate_melee_attack_points()
        self.ranged_attack_points = self.calculate_ranged_attack_points()
        self.melee_critical_chance = self.calculate_melee_critical_chance()
        self.ranged_critical_chance = self.calculate_ranged_critical_chance()
        
        self.magic_attack_points = self.calculate_magic_attack_points()
        self.magic_critical_chance = self.calculate_magic_critical_chance()
        return
    
    # This function searches for objects from a given class inside a list
    # It returns another list with the desired objects
    # Useful to filter the Inventory and Spell book lists
    def return_a_list_of_objects_from_a_class(self, list_arg:list, class_arg):
        list_to_return = []
        for object in list_arg:
            if type(object) == class_arg:
                list_to_return.append(object)
        return list_to_return
    
    def print_preview_info_from_items_in_list(self, title:str, list_to_print_arg:list):
        print(title)
        i = 0
        for item in list_to_print_arg:
            item.print_item_inventory_preview_info(i)
            i += 1
    
    def print_support_spells_in_spell_book(self):
        print("SUPPORT SPELLS")
        support_spells_list = self.return_a_list_of_objects_from_a_class(self.spell_book, sp.SupportSpells)
        i = 0
        for spell in support_spells_list:
            print(f"({i}).SPELL NAME:{spell.spell_name}  COST:{spell.mana_cost} COOLDOWN:{spell.cooldown} Ready in:{spell.cooldown_counter} turns")
            i += 1
    
    def print_combat_spells_in_spell_book(self):
        print("COMBAT SPELLS")
        combat_spells_list = self.return_a_list_of_objects_from_a_class(self.spell_book, sp.CombatSpells)
        i = 0
        for spell in combat_spells_list:
            print(f"({i}).SPELL NAME:{spell.spell_name}  COST:{spell.mana_cost} ATTACK POINTS: {spell.attack_points}")
            i += 1
    
    #  Functions for item and spell management
    def select_item_to_equip(self, item_class_arg, title:str):
        while True:
            try:
                print("Type one of the options or -e to go back")
                items_list = self.return_a_list_of_objects_from_a_class(self.inventory, item_class_arg)
                self.print_preview_info_from_items_in_list(title, items_list)
                user_choice = input("> ").strip().lower()
                if user_choice == "-e":
                    break
                elif user_choice.isdecimal():
                    items_list[int(user_choice)].equip_item(self)
                    self.update_stats()
                    return
                else:
                    print("\nPlease type one of the options\n")
            except IndexError:
                print("\nINDEX ERROR!!!\n")
                time.sleep(4)
            except:
                print("\nUNKNOWN ERROR, PLEASE REPORT\n")
                time.sleep(4)
                break
    
    def select_combat_spell(self):
        time.sleep(1)
        while True:
            try:
                print("Type one of the options or -e to go back")
                combat_spells_list = self.return_a_list_of_objects_from_a_class(self.spell_book, sp.CombatSpells)
                self.print_combat_spells_in_spell_book()
                user_choice = input("> ").strip().lower()
                if user_choice == "-e":
                    break
                elif user_choice.isdecimal():
                    spell_index_in_list = int(user_choice)
                    selected_combat_spell = combat_spells_list[spell_index_in_list]
                    self.combat_spell_slot = selected_combat_spell
                    print(f"\n{self.combat_spell_slot.spell_name} selected")
                    time.sleep(1)
                    return self.combat_spell_slot 
                else:
                    print("\nPlease type one of the options\n")
                    continue
            except ValueError:
                print("\nVALUE ERROR!!!\n")
            except IndexError:
                print("\nINDEX ERROR!!!\n")
    
    #  Functions for player actions in battle
    def use_melee_attack(self, enemy_target):
        time.sleep(1)
        print(f"You select to use a melee attack...")
        sp_cost = round((self.max_sp * self.melee_weapon_slot.stamina_cost), 0)
        self.sp -= sp_cost
        crit_chance = self.trigger_critical_melee_attack()
        if crit_chance == [False]:
            damage = self.calculate_melee_damage(enemy_target)
            print(f"Character has done {damage} attack points and consumes {sp_cost} stamina points...")
        elif crit_chance == [True]:
            damage = self.calculate_critical_melee_damage(enemy_target)
            print(f"Character has done {damage} critical attack points and consumes {sp_cost} stamina points...")
        enemy_target.hp -= damage
        if enemy_target.hp <= 0:
            enemy_target.hp = 0
        time.sleep(1)
        print(f"\nEnemy HP remaining: {enemy_target.hp}")
        time.sleep(1)
        return enemy_target.hp

    def use_ranged_attack(self, enemy_target):
        time.sleep(1)
        print(f"You select to use a ranged attack...")
        sp_cost = round((self.max_sp * self.ranged_weapon_slot.stamina_cost), 0)
        self.sp -= sp_cost
        crit_chance = self.trigger_critical_ranged_attack()
        if crit_chance == [False]:
            damage = self.calculate_ranged_damage(enemy_target)
            print(f"Character has done {damage} attack points and consumes {sp_cost} stamina points...")
        elif crit_chance == [True]:
            damage = self.calculate_critical_ranged_damage(enemy_target)
            print(f"Character has done {damage} critical attack points and consumes {sp_cost} stamina points...")
        enemy_target.hp -= damage
        if enemy_target.hp <= 0:
            enemy_target.hp = 0
        time.sleep(1)
        print(f"\nEnemy HP remaining: {enemy_target.hp}")
        time.sleep(1)
        return enemy_target.hp
    
    def use_combat_spell(self, enemy_target):
        time.sleep(1)
        print(f"You select to use a magic attack...")
        self.mp = self.mp - self.combat_spell_slot.mana_cost
        crit_chance = self.trigger_critical_magic_attack()
        if crit_chance == [False]:
            magic_damage = self.calculate_magic_damage(enemy_target)
            print(f"Character has done {magic_damage} magic attack points")
        elif crit_chance == [True]:
            magic_damage = self.calculate_critical_magic_damage(enemy_target)
            print(f"Character has done {magic_damage} critical magic attack points")
        enemy_target.hp -= magic_damage
        if enemy_target.hp <= 0:
            enemy_target.hp = 0
        time.sleep(1)
        print(f"Enemy HP remaining: {enemy_target.hp}")
        time.sleep(1)
        return enemy_target.hp
    
    def use_a_support_spell(self, enemy_target_arg=None):
        while True:
            try:
                print("Type one of the options or -e to go back")
                support_spells_list = self.return_a_list_of_objects_from_a_class(self.spell_book, sp.SupportSpells)
                self.print_support_spells_in_spell_book()
                user_choice = input("> ").strip().lower()
                if user_choice == "-e":
                    break
                elif user_choice.isdecimal():
                    spell_index_in_list = int(user_choice)
                    selected_support_spell = support_spells_list[spell_index_in_list]
                    if selected_support_spell.cooldown_counter == 0:
                        if self.mp >= selected_support_spell.mana_cost:
                            if selected_support_spell.targets_affected == "self":
                                selected_support_spell.effect(self)
                            elif selected_support_spell.targets_affected == "target":
                                selected_support_spell.effect(self, enemy_target_arg)
                            else:
                                print("\nTARGET ERROR!!!\n")
                                continue
                            self.mp -= selected_support_spell.mana_cost
                            selected_support_spell.start_cooldown_counter()
                            print("")
                            print(f"{selected_support_spell.spell_name} used")
                            print(f"-{selected_support_spell.mana_cost} mana points")
                            print("")
                        else:
                            print("\nNOT ENOUGH MANA POINTS!!!\n")
                    else:
                        print("\nSPELL ON COOLDOWN!!!\n")
                else:
                    print("\nPlease type one of the options\n")
            except IndexError:
                print("\nINDEX ERROR!!!\n")
            except ValueError:
                print("\nVALUE ERROR!!!\n")
    
    def use_a_consumable_item(self, title:str="CONSUMABLES"):
        while True:
            try:
                print("Type one of the options or -e to go back")
                consumable_list = self.return_a_list_of_objects_from_a_class(self.inventory, it.ConsumableClass)
                self.print_preview_info_from_items_in_list(title, consumable_list)
                user_choice = input("> ").strip().lower()
                if user_choice == "-e":
                    break
                elif user_choice.isdecimal():
                    consumable_list[int(user_choice)].use_item(self)
                    self.update_stats()
                    return
                else:
                    print("\nPlease type one of the options\n")
            except IndexError:
                print("\nINDEX ERROR!!!\n")
                time.sleep(4)
            except:
                print("\nUNKNOWN ERROR, PLEASE REPORT\n")
                time.sleep(4)
                break
                
    def use_life_flask(self):
        if self.flask_life != 0:
            self.hp += self.flask_values_per_upgrade[self.flask_upgrade_level]
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            self.flask_life -= 1
            time.sleep(1)
            print(f"\nCharacter recovers {self.flask_values_per_upgrade[self.flask_upgrade_level]} health points")
            time.sleep(1)
        elif self.hp == self.max_hp:
            time.sleep(1)
            print("\nCharacter with full health")
            time.sleep(1)
        elif self.flask_life == 0:
            time.sleep(1)
            print("\nNo health flasks available")
            time.sleep(1)

    def use_mana_flask(self):
        if self.flask_mana != 0:
            self.mp += self.flask_values_per_upgrade[self.flask_upgrade_level]
            if self.mp > self.max_mp:
                self.mp = self.max_mp
            self.flask_mana -= 1
            time.sleep(1)
            print(f"\nCharacter recovers {self.flask_values_per_upgrade[self.flask_upgrade_level]} mana points")
            time.sleep(1)
        elif self.mp == self.max_mp:
            time.sleep(1)
            print("\nCharacter with full mana")
            time.sleep(1)
        elif self.flask_mana == 0:
            time.sleep(1)
            print("\nNo mana flasks available")
            time.sleep(1)
    
    def recover_breath(self):
        #It needs to return a bool to decide if player finished its turn
        if self.sp <= self.max_sp:
            self.sp += (self.max_sp*0.4)
            if self.sp > self.max_sp:
                self.sp = self.max_sp
            time.sleep(1)
            print("\nThe character recovers stamina points...")
            time.sleep(1)
        elif self.sp == self.max_sp:
            time.sleep(1)
            print("\nThe character is fully recovered, you can't use this action")
            time.sleep(1)
    
    def print_player_status(self):
        print("STATUS")
        for buff_stack in self.status:
            print(f"·{buff_stack.name}  Turns left:{buff_stack.turns_until_remove_this_status_modifier}")
    
    #  Functions to manage player level and base attributes
    def level_up(self):
        self.attribute_points += 1
        self.level += 1
        print(f"The character has reached level {self.level}\n")
        return self.level
    
    def check_experience_to_decide_if_level_up(self):
        while True:
            level_up_cost = (((self.level+1)*5) ** 2)
            if self.experience >= level_up_cost:
                self.level_up()
                continue
            else:
                break

    def add_strength(self):
        self.base_strength += 1
        self.update_stats()
        self.hp = self.max_hp
        self.sp = self.max_sp
        self.attribute_points -= 1
        print(f"Character Strength has been increased")
        return self.base_strength
    
    def add_agility(self):
        self.base_agility += 1
        self.update_stats()
        self.attribute_points -= 1
        print(f"Character Agility has been increased")
        return self.base_agility
    
    def add_intelligence(self):
        self.base_intelligence += 1
        self.update_stats()
        self.mp = self.max_mp
        self.attribute_points -= 1
        print(f"Character Intelligence has been increased")
        return self.base_intelligence
  
    #  Functions to update buffs and skills and restore the character
    def natural_regeneration_after_each_turn(self):
        if self.mp < self.max_mp:
            self.mp += round((self.max_mp * 0.1), 0)
            if self.mp > self.max_mp:
                self.mp = self.max_mp
        if self.sp < self.max_sp:
            self.sp += round((self.max_sp * 0.1), 0)
            if self.sp > self.max_sp:
                self.sp = self.max_sp
        return
    
    def update_buffs_duration(self):
        for buff_stack in self.status:
            if buff_stack.turns_until_remove_this_status_modifier > 0:
                buff_stack.turns_until_remove_this_status_modifier -= 1
                if buff_stack.turns_until_remove_this_status_modifier == 0:
                    buff_stack.remove_this_status_modifier_from_target(self)
                    continue
        self.update_stats()
    
    def update_spells_cooldown(self):
        support_spells_list = self.return_a_list_of_objects_from_a_class(self.spell_book, sp.SupportSpells)
        for support_spell in support_spells_list:
            support_spell.reduce_cooldown()
    
    def remove_all_player_active_buffs(self):
        for buff_stack in self.status:
            buff_stack.remove_this_status_modifier_from_target(self)
    
    def restart_all_spells_cooldown(self):
        support_spells_list = self.return_a_list_of_objects_from_a_class(self.spell_book, sp.SupportSpells)
        for support_spell in support_spells_list:
            support_spell.refresh_spell()
    
    def restore_player_after_victory(self):
        self.remove_all_player_active_buffs()
        self.restart_all_spells_cooldown()
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.sp = self.max_sp
        print("Character restored")
        time.sleep(1)
        return