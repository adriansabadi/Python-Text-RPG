import Player.effects as ef

class Spells():
    def __init__(self, spell_name_arg, description_arg, mana_cost_arg):
        self.spell_name = spell_name_arg
        self.description = description_arg
        self.mana_cost = mana_cost_arg
    

class CombatSpells(Spells):
    def __init__(self, spell_name_arg, description_arg, mana_cost_arg, attack_points_arg):
        self.attack_points = attack_points_arg
        super().__init__(spell_name_arg, description_arg, mana_cost_arg)
    

class SupportSpells(Spells):
    def __init__(self, spell_name_arg, description_arg, mana_cost_arg, cooldown_arg, effect_arg, targets_affected_arg):
        self.cooldown = cooldown_arg
        self.cooldown_counter = 0
        self.effect = effect_arg
        self.targets_affected = targets_affected_arg
        super().__init__(spell_name_arg, description_arg, mana_cost_arg)
        
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
    

sp_001 = CombatSpells("Fireball", "Classic fireball", 10, 10)
sp_002 = SupportSpells("Increase Strength", "Increases character Strength", 20, 3, ef.player_strength_up, "self")

