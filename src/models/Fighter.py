class Fighter:

    def __init__(self,name, strength, accuracy, stamina, reach, takedown_defense):
        self.name = name 
        self.strength = strength
        self.accuracy = accuracy
        self.max_stamina = stamina
        self.reach = reach
        self.takedown_defense = takedown_defense
        self.current_stamina = stamina
        self.damage = 0

    def apply_damage (self, dmg):
        self.damage = dmg
        self.current_stamina = max(0, self.current_stamina - dmg * 0.1)

    def is_knocked_out (self):
        return self.current_stamina <= 0
