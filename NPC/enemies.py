import time
import random as rd

import NPC.skills as sk


class HostileNPC:
    def __init__(self, name_arg, base_max_hp_arg, base_max_mp_arg, base_attack_points_arg, base_magic_attack_points_arg, base_defense_points_arg, 
                 base_magic_defense_points_arg, base_strength_points_arg, base_agility_points_arg, base_intelligence_points_arg, skills_arg,
                coins_arg, experience_reward_arg):
        self.name = name_arg
        #Base attributes
        self.base_max_hp = base_max_hp_arg
        self.base_hp = self.base_max_hp
        self.base_max_mp = base_max_mp_arg
        self.base_mp = self.base_max_mp
        self.base_attack_points = base_attack_points_arg
        self.base_magic_attack_points = base_magic_attack_points_arg
        self.base_defense_points = base_defense_points_arg
        self.base_magic_defense_points = base_magic_defense_points_arg
        self.base_strength = base_strength_points_arg
        self.base_agility = base_agility_points_arg
        self.base_intelligence = base_intelligence_points_arg
        #Bonus attributes
        self.bonus_hp = 0
        self.bonus_mp = 0
        self.bonus_attack_points = 0
        self.bonus_magic_attack_points = 0
        self.bonus_defense_points = 0
        self.bonus_magic_defense_points = 0
        self.bonus_strength = 0
        self.bonus_agility = 0
        self.bonus_intelligence = 0
        #Atributos totales
        self.max_hp = self.base_max_hp + self.bonus_hp
        self.max_mp = self.base_max_mp + self.bonus_mp
        self.hp = self.base_hp + self.bonus_hp
        self.mp = self.base_mp + self.bonus_mp
        self.attack_points = self.base_attack_points + self.bonus_attack_points
        self.magic_attack_points = self.base_magic_attack_points + self.bonus_magic_attack_points
        self.defense_points = self.base_defense_points + self.bonus_defense_points
        self.magic_defense_points = self.base_magic_defense_points + self.bonus_defense_points
        self.strength = self.base_strength + self.bonus_strength
        self.agility = self.base_agility + self.bonus_agility
        self.intelligence = self.base_intelligence + self.bonus_intelligence

        self.skills = skills_arg
        
        self.coins_drop = coins_arg
        self.experience_reward = experience_reward_arg
        self.status = []
        self.update_stats()

    def update_stats(self):
        self.max_hp = self.base_max_hp + self.bonus_hp
        self.max_mp = self.base_max_mp + self.bonus_mp
        self.attack_points = self.base_attack_points + self.bonus_attack_points
        self.magic_attack_points = self.base_magic_attack_points + self.bonus_magic_attack_points
        self.defense_points = self.base_defense_points + self.bonus_defense_points
        self.magic_defense_points = self.base_magic_defense_points + self.bonus_defense_points
        self.strength = self.base_strength + self.bonus_strength
        self.agility = self.base_agility + self.bonus_agility
        self.intelligence = self.base_intelligence + self.bonus_intelligence
        return

    def return_a_list_of_usable_skills(self):
        list_of_usable_skills = []
        for skill in self.skills:
            if type(skill) == sk.ActiveSkills and skill.cooldown_counter == 0:
                list_of_usable_skills.append(skill)
        return list_of_usable_skills

    def use_actions(self, target_arg):
        list_of_usable_skills = self.return_a_list_of_usable_skills()
        usable_skills = 0
        for skill in list_of_usable_skills:
            usable_skills += 1
        print(f"Number of skills:{usable_skills}")
        while True:
            action_dice = rd.randint(0, usable_skills-1)
            chosen_skill = list_of_usable_skills[action_dice]
            if self.mp >= chosen_skill.mana_cost:
                print(f"{self.name} uses {chosen_skill.skill_name}")
                if chosen_skill.target_affected == "self":
                    chosen_skill.effect(self)
                elif chosen_skill.target_affected == "target":
                    chosen_skill.effect(self, target_arg)
                else:
                    print("SKILL TARGET ERROR")
                    continue
                self.mp -= chosen_skill.mana_cost
                self.update_stats()
                chosen_skill.start_cooldown_counter()
                time.sleep(2)
                break
            else:
                continue
    
    def use_turn_based_passive_v1(self):
        for skill in self.skills:
            if type(skill) == sk.PassiveSkills:
                skill.effect(self)
                time.sleep(1)
    
    def update_skills_cooldown(self):
        for skill in self.skills:
            if type(skill) == sk.ActiveSkills:
                skill.reduce_cooldown()
    
    def restart_all_skill_cooldowns(self):
        for skill in self.skills:
            if type(skill) == sk.ActiveSkills:
                skill.refresh_spell()
    
    def update_buffs_duration(self):
        for buff_stack in self.status:
            if buff_stack.turns_until_remove_this_status_modifier > 0:
                buff_stack.turns_until_remove_this_status_modifier -= 1
                if buff_stack.turns_until_remove_this_status_modifier == 0:
                    buff_stack.remove_this_status_modifier_from_target(self)
                    continue
    
    def print_enemy_status(self):
        print("STATUS")
        for buff_stack in self.status:
            print(f"·{buff_stack.name}  Turns left:{buff_stack.turns_until_remove_this_status_modifier}")

    def remove_all_npc_active_buffs(self):
        for buff_stack in self.status:
            buff_stack.remove_this_status_modifier_from_target(self)
    

def enemy_wave_1():
    id_001 = HostileNPC("Special Enemy", 3000, 500, 80, 100, 40, 40, 20, 20, 20, [sk.es_0001, sk.es_0003, sk.es_0004, sk.es_0007, sk.es_0008, sk.es_0009, sk.es_0010], 10000, 10000)
    id_002 = HostileNPC("Wild Beast", 20, 0, 12, 0, 3, 0, 2, 4, 0, [sk.es_0001, sk.es_0003], 20, 30)
    id_003 = HostileNPC("Swordsman", 40, 0, 18, 0, 6, 0, 5, 3, 2, [sk.es_0001, sk.es_0003, sk.es_0004], 50, 80)
    id_004 = HostileNPC("Archer", 40, 0, 18, 0, 4, 0, 4, 6, 2, [sk.es_0001], 40, 60)
    id_005 = HostileNPC("Wizard", 40, 80, 12, 22, 4, 8, 3, 2, 8, [sk.es_0001, sk.es_0002, sk.es_0005], 60, 90)
    id_006 = HostileNPC("Light Cavalry", 50, 0, 24, 0, 6, 0, 5, 6, 3, [sk.es_0001, sk.es_0003], 100, 120)

    wave_1 = [id_002, id_003, id_004, id_005, id_006]
    enemy_target = rd.choice(wave_1)
    return enemy_target


