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
        return
    
    def remove_this_status_modifier_from_target(self, target):
        target.status.remove(self)
        return


class Buff(StatusModifier):
    def __init__(self, name_arg, duration_arg, target_arg, is_removable_arg):
        super().__init__(name_arg, duration_arg, target_arg, is_removable_arg)
    

class Debuff(StatusModifier):
    def __init__(self, name_arg, duration_arg, is_removable_arg):
        super().__init__(name_arg, duration_arg, is_removable_arg)


class StrengthUp(Buff):
    def __init__(self, name_arg, duration_arg, target_arg, is_removable_arg, value):
        self.strength_modifier = value
        super().__init__(name_arg, duration_arg, target_arg, is_removable_arg)
    
    def add_this_status_modifier_to_target(self, target):
        target.bonus_strength += self.strength_modifier
        return super().add_this_status_modifier_to_target(target)
    
    def remove_this_status_modifier_from_target(self, target):
        target.bonus_strength -= self.strength_modifier
        return super().remove_this_status_modifier_from_target(target)


class DefenseUp(Buff):
    def __init__(self, name_arg, duration_arg, target_arg, is_removable_arg, value):
        self.defense_modifier = value
        super().__init__(name_arg, duration_arg, target_arg, is_removable_arg)
    
    def add_this_status_modifier_to_target(self, target):
        target.bonus_defense_points += self.defense_modifier
        return super().add_this_status_modifier_to_target(target)
    
    def remove_this_status_modifier_from_target(self, target):
        target.bonus_defense_points -= self.defense_modifier
        return super().remove_this_status_modifier_from_target(target)


class MagicDefenseUp(Buff):
    def __init__(self, name_arg, duration_arg, target_arg, is_removable_arg, value):
        self.magic_defense_modifier = value
        super().__init__(name_arg, duration_arg, target_arg, is_removable_arg)
    
    def add_this_status_modifier_to_target(self, target):
        target.bonus_magic_defense_points += self.magic_defense_modifier
        return super().add_this_status_modifier_to_target(target)
    
    def remove_this_status_modifier_from_target(self, target):
        target.bonus_magic_defense_points -= self.magic_defense_modifier
        return super().remove_this_status_modifier_from_target(target)