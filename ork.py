class Ork:
    def __init__(self, model):
        self.model = model
        self.weapons = []
        self.wargear = []
        self.abilities = []

    def addWeapon(self, weapon):
        self.weapons.append(weapon)

    def addWargear(self, wargear):
        self.wargear.append(wargear)

    def addAbility(self, ability):
        self.abilities.append(ability)

    def name(self):
        return self.model['name']

    def stats(self):
        return self.model['stats']
