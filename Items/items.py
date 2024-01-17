import Items.items_effects as ie


class ItemClass():
    def __init__(self, item_name_arg:str, item_description_text_arg, item_buy_cost_arg:int):
        self.item_name = item_name_arg
        self.item_description_text = item_description_text_arg
        self.item_buy_cost = item_buy_cost_arg
    
    def print_item_shop_preview_info(self, item_index_in_list:int):
        print(f"{item_index_in_list}. {self.item_name} COST: {self.item_buy_cost}")
    
    def print_item_inventory_preview_info(self, item_index_in_list:int):
        print(f"{item_index_in_list}. {self.item_name}")
    
    def print_item_details(self):
        print(f"ITEM NAME: {self.item_name}")
        print(f"DESCRIPTION:\n {self.item_description_text}")

    def check_if_item_is_in_player_inventory(self, player_arg):
        is_item_in_inventory = False 
        for item in player_arg.inventory:
            if id(self) == id(item):
                is_item_in_inventory = True
        return is_item_in_inventory
    
    def add_item_to_player_inventory(self, player_arg):
        player_arg.inventory.append(self)
        print(f"{self.item_name} added to inventory")
        return
    
    def buy_this_item(self, player_arg):
        if player_arg.coins >= self.item_buy_cost:
            self.add_item_to_player_inventory(player_arg)
            print(f"\n{self.item_name} acquired for {self.item_buy_cost} coins")
            player_arg.coins -= self.item_buy_cost
        else:
            print("NOT ENOUGH COINS")


class ArmorClass(ItemClass):
    def __init__(self, item_name_arg: str, item_description_text_arg, item_buy_cost_arg: int, defense_provided:int):
        self.defense_points = defense_provided
        super().__init__(item_name_arg, item_description_text_arg, item_buy_cost_arg)
    
    def print_item_details(self):
        print("")
        print(f"ARMOR NAME: {self.item_name}")
        print(f"DEFENSE POINTS: {self.defense_points}")
        print(f"DESCRIPTION:\n {self.item_description_text}")
        print("")
    
    def equip_item(self, player_arg):
        try:
            player_arg.armor_slot = self
            print(f"\n{self.item_name} equipped in the armor slot\n")
        except IndexError:
            print("INDEX ERROR")


class WeaponClass(ItemClass):
    def __init__(self, item_name_arg: str, item_description_text_arg, item_buy_cost_arg: int,
                  attack_points_arg:int, stamina_cost_for_use_arg:float):
        self.weapon_attack_points = attack_points_arg
        self.stamina_cost = stamina_cost_for_use_arg
        super().__init__(item_name_arg, item_description_text_arg, item_buy_cost_arg)
    
    def print_item_details(self):
        print("")
        print(f"WEAPON NAME: {self.item_name}")
        print(f"ATTACK POINTS: {self.weapon_attack_points}")
        print(f"STAMINA COST: {self.stamina_cost}")
        print(f"DESCRIPTION:\n {self.item_description_text}")
        print("")
    
    def equip_item(self):
        pass
    

class MeleeWeaponClass(WeaponClass):
    def __init__(self, item_name_arg: str, item_description_text_arg, item_buy_cost_arg: int,
                  attack_points_arg: int, stamina_cost_for_use_arg: float):
        super().__init__(item_name_arg, item_description_text_arg, item_buy_cost_arg, attack_points_arg, stamina_cost_for_use_arg)

    def equip_item(self, player_arg):
        try:
            player_arg.melee_weapon_slot = self
            print(f"\n{self.item_name} equipped in the melee weapon slot\n")
            return
        except IndexError:
            print("INDEX ERROR")


class RangedWeaponClass(WeaponClass):
    def __init__(self, item_name_arg: str, item_description_text_arg, item_buy_cost_arg: int,
                  attack_points_arg: int, stamina_cost_for_use_arg: float):
        super().__init__(item_name_arg, item_description_text_arg, item_buy_cost_arg, attack_points_arg, stamina_cost_for_use_arg)

    def equip_item(self, player_arg):
        try:
            player_arg.ranged_weapon_slot = self
            print(f"\n{self.item_name} equipped in the ranged weapons slot\n")
        except IndexError:
            print("INDEX ERROR")


class ShieldClass(ItemClass):
    def __init__(self, item_name_arg: str, item_description_text_arg, item_buy_cost_arg: int, block_value_arg:int):
        self.block_points = block_value_arg
        super().__init__(item_name_arg, item_description_text_arg, item_buy_cost_arg)
    
    def print_item_details(self):
        print("")
        print(f"ARMOR NAME: {self.item_name}")
        print(f"BLOCK POINTS: {self.block_points}")
        print(f"DESCRIPTION:\n {self.item_description_text}")
        print("")


class ConsumableClass(ItemClass):
    def __init__(self, item_name_arg: str, item_description_text_arg, item_buy_cost_arg: int,
                 item_use_effect_arg):
        self.item_effect = item_use_effect_arg
        self.amount = 0
        super().__init__(item_name_arg, item_description_text_arg, item_buy_cost_arg)
    
    def print_item_inventory_preview_info(self, item_index_in_list:int):
        print(f"{item_index_in_list}. {self.item_name}(x{self.amount})")
    
    def increase_this_item_amount(self, increase_amount:int=1):
        self.amount += increase_amount
        return self.amount
    
    def decrease_this_item_amount(self, decrease_amount:int=1):
        self.amount -= decrease_amount
        return self.amount
    
    def add_item_to_player_inventory(self, player_arg, amount_to_add:int=1):
        is_item_in_inventory = self.check_if_item_is_in_player_inventory(player_arg)
        if is_item_in_inventory == False:
            player_arg.inventory.append(self)
            print(f"{self.item_name} added to inventory")
            print(f"{self.item_name} +{amount_to_add}")
            self.increase_this_item_amount(amount_to_add)
        else:
            self.increase_this_item_amount(amount_to_add)
            print(f"{self.item_name} +{amount_to_add}")
        return
    
    def select_amount_to_buy(self, player_arg):
        while True:
            try:
                max_units = int(player_arg.coins / self.item_buy_cost)
                print(f"How many units do you want to buy? MAX:{max_units}")
                units_to_buy = int(input("> "))
                print(units_to_buy)
                return units_to_buy
            except ValueError:
                print("Type a number")
                continue
    
    def buy_this_item(self, player_arg):
        units_to_buy = self.select_amount_to_buy(player_arg)
        order_cost = units_to_buy * self.item_buy_cost
        if player_arg.coins >= order_cost:
            self.add_item_to_player_inventory(player_arg, units_to_buy)
            print(f"\n{self.item_name}(x{units_to_buy}) acquired for {order_cost} coins")
            player_arg.coins -= order_cost
        else:
            print("NOT ENOUGH COINS")
    
    def remove_item_from_player_inventory(self, player_arg):
        if self.amount > 1:
            self.decrease_this_item_amount()
        elif self.amount <= 1:
            self.amount = 0
            player_arg.inventory.remove(self)
        return

    def use_item(self, player_arg):
        self.item_effect(player_arg)
        self.remove_item_from_player_inventory(player_arg)
        print(f"{self.item_name} used")
        return