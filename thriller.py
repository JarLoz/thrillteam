from parse import parse
from readlist import readlist
from ork import Ork

def main():
    orkdata = parse()
    orklist = readlist()

    orks = []
    for o in orklist:
        model = orkdata['Model'][o['Model']]
        ork = Ork(model)

        if ('Weapon' in o.keys()):
            for weapon in o['Weapon']:
                ork.addWeapon(orkdata['Weapon'][weapon])
        if ('Ability' in o.keys()):
            for ability in o['Ability']:
                ork.addAbility(orkdata['Ability'][ability])
        if ('Wargear' in o.keys()):
            for wargear in o['Wargear']:
                ork.addWargear(orkdata['Wargear'][wargear])

        orks.append(ork)

    return orks
if (__name__ == "__main__"):
    main()
