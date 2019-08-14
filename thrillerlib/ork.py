class Ork:
    def __init__(self, model):
        self.model = model
        self.name = self.model['name']
        self.stats = self.model['stats']
        self.weapons = []
        self.wargear = []
        self.abilities = []
        self.subFaction = None
        self.specialist = None

    def addWeapon(self, weapon):
        self.weapons.append(weapon)

    def addWargear(self, wargear):
        self.wargear.append(wargear)

    def addAbility(self, ability):
        self.abilities.append(ability)

    def setSpecialist(self, specialist):
        self.specialist = specialist

    def setSubFaction(self, subFaction):
        self.subFaction = subFaction
