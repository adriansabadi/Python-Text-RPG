import NPC.effects as effects


class EnemySkills():
    def __init__(self, skill_name_arg, description_arg):
        self.skill_name = skill_name_arg
        self.description = description_arg


class ActiveSkills(EnemySkills):
    def __init__(self, skill_name_arg, description_arg, target_affected_arg, effect_arg, cooldown_arg, mana_cost_arg):
        self.target_affected = target_affected_arg
        self.effect = effect_arg
        self.cooldown = cooldown_arg
        self.cooldown_counter = 0
        self.mana_cost = mana_cost_arg
        super().__init__(skill_name_arg, description_arg)
    
    def start_cooldown_counter(self):
        self.cooldown_counter = self.cooldown
        return
    
    def refresh_spell(self):
        self.cooldown_counter = 0
        return
    
    def reduce_cooldown(self):
        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1
            if self.cooldown_counter == 0:
                self.refresh_spell()
        return self.cooldown_counter


class PassiveSkills(EnemySkills):
    def __init__(self, skill_name_arg, description_arg, target_affected_arg, effect_arg):
        self.target_affected = target_affected_arg
        self.effect = effect_arg
        super().__init__(skill_name_arg, description_arg)


es_0001 = ActiveSkills("Normal attack", "Enemy uses a normal attack","target", effects.use_normal_attack, 0, 0)
es_0002 = ActiveSkills("Magic attack", "Enemy uses magic projectiles to attack", "target",effects.use_magic_attack, 0, 5)
es_0003 = ActiveSkills("Fury", "Enemy doubles its Strength", "self", effects.double_strength, 7, 100)
es_0004 = ActiveSkills("Push", "Enemy knocks out its objective", "target", effects.almighty_push, 4, 0)
es_0005 = ActiveSkills("Fireball", "Classic fireball", "target", effects.fireball, 0, 20)
es_0006 = ActiveSkills("Charge", "Enemy charges against its objective", "target", effects.charge, 4, 0)
es_0007 = ActiveSkills("Magic Protection", "Increases its Magic Defense by 10 points", "self", effects.increase_magic_defense_by_50_points, 6, 150)
es_0008 = PassiveSkills("Passive Health Regeneration", "Recovers health points at the end of each turn", "self", effects.recover_hp_passive)
es_0009 = PassiveSkills("Passive Mana Regeneration", "Recovers mana points at the end of each turn", "self", effects.recover_mp_passive)
es_0010 = ActiveSkills("Anti-magic Cut", "Burns its objective mana points", "target", effects.melee_attack_that_decreases_mana_from_player, 3, 100)
