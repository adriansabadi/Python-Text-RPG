class StatusModifier():
    this_is_a_status_modifier = True
    def __init__(self, name_arg, duration_arg, target_arg, is_removable_arg):
        self.name = name_arg
        self.duration = duration_arg
        self.turns_until_remove_this_status_modifier = duration_arg
        self.is_removable = is_removable_arg
        self.add_this_status_modifier_to_target(target_arg)
    
    def add_this_status_modifier_to_target(self, target):
        target.status.append(self)
        target.update_stats()
        return
    
    def remove_this_status_modifier_from_target(self, target):
        target.status.remove(self)
        target.update_stats()
        return


class Buff(StatusModifier):
    def __init__(self, name_arg, duration_arg, target_arg, is_removable_arg):
        super().__init__(name_arg, duration_arg, target_arg, is_removable_arg)
    

class Debuff(StatusModifier):
    def __init__(self, name_arg, duration_arg, is_removable_arg):
        super().__init__(name_arg, duration_arg, is_removable_arg)


class PlayerStrengthUp(Buff):
    def __init__(self, name_arg, duration_arg, target_arg, is_removable_arg, value):
        self.strength_to_add = value
        super().__init__(name_arg, duration_arg, target_arg, is_removable_arg)
        
    def add_this_status_modifier_to_target(self, target):
        target.bonus_strength += self.strength_to_add
        return super().add_this_status_modifier_to_target(target)
    
    def remove_this_status_modifier_from_target(self, target):
        target.bonus_strength -= self.strength_to_add
        return super().remove_this_status_modifier_from_target(target)


class PlayerAgilityUp(Buff):
    def __init__(self, name_arg, duration_arg, target_arg, is_removable_arg, value):
        self.agility_to_add = value
        super().__init__(name_arg, duration_arg, target_arg, is_removable_arg)
        
    def add_this_status_modifier_to_target(self, target):
        target.bonus_agility += self.agility_to_add
        return super().add_this_status_modifier_to_target(target)
    
    def remove_this_status_modifier_from_target(self, target):
        target.bonus_agility -= self.agility_to_add
        return super().remove_this_status_modifier_from_target(target)


class PlayerIntelligenceUp(Buff):
    def __init__(self, name_arg, duration_arg, target_arg, is_removable_arg, value):
        self.intelligence_to_add = value
        super().__init__(name_arg, duration_arg, target_arg, is_removable_arg)
        
    def add_this_status_modifier_to_target(self, target):
        target.bonus_intelligence += self.intelligence_to_add
        return super().add_this_status_modifier_to_target(target)
    
    def remove_this_status_modifier_from_target(self, target):
        target.bonus_intelligence -= self.intelligence_to_add
        return super().remove_this_status_modifier_from_target(target)