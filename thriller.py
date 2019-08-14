from thrillerlib.parse import parse
from thrillerlib.readlist import readlist
from thrillerlib.ork import Ork
from pgmagick import Image, DrawableText
from textwrap import wrap
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("faction", help="Name of the faction in the army list")
    parser.add_argument("list", help="Filename of the army list")
    parser.add_argument("data", help="Path to folder containing the battlescribe data files")
    args = parser.parse_args()
    orks = createOrks(args.faction, args.list, args.data)
    for o in orks:
        createCard(o)

def createOrks(faction, listfilename, data):
    orkdata = parse(data, faction)
    orklist = readlist(listfilename)

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
        if ('Specialist' in o.keys()):
            for specialist in o['Specialist']:
                ork.setSpecialist(specialist)
        if ('Sub-faction' in o.keys()):
            for sub in o['Sub-faction']:
                ork.setSubFaction(orkdata['Sub-faction'][sub])

        orks.append(ork)

    return orks

def createCard(ork):
    template = Image('templates/cardtemplate.png')
    name = ork.name
    abilities = {}
    # Name 
    template.fontPointsize(50)
    nameString = name
    if (ork.specialist != None):
        nameString += ", " + ork.specialist
    template.draw(DrawableText(38, 84, nameString))

    # Stats

    template.fontPointsize(45)

    template.draw(DrawableText(52, 185, ork.stats['M']))
    template.draw(DrawableText(135, 185, ork.stats['WS']))
    template.draw(DrawableText(230, 185, ork.stats['BS']))
    template.draw(DrawableText(330, 185, ork.stats['S']))
    template.draw(DrawableText(416, 185, ork.stats['T']))
    template.draw(DrawableText(485, 185, ork.stats['A']))
    template.draw(DrawableText(566, 185, ork.stats['W']))
    template.draw(DrawableText(662, 185, ork.stats['Ld']))
    template.draw(DrawableText(783, 185, ork.stats['Sv']))

    # Weapons

    template.fontPointsize(30)

    weaponOffset = 40
    weaponY = 277
    for weapon in ork.weapons:
        weaponName = weapon['name']
        if (weaponName.startswith('Kombi-weapon with')):
            start = weaponName.find('(') + 1
            end = weaponName.find(')')
            weaponName = weaponName[start:end]

        weaponNameStrings = wrap(weaponName, 14)
        for i in range(min(len(weaponNameStrings), 2)):
            template.draw(DrawableText(43, weaponY, weaponNameStrings[i]))
            if (i+1 < len(weaponNameStrings)):
                weaponY += 35
        template.draw(DrawableText(295, weaponY, weapon['stats']['Range']))
        template.draw(DrawableText(445, weaponY, weapon['stats']['Type']))
        if (weapon['stats']['S'] == 'User'):
            template.draw(DrawableText(656, weaponY, 'U'))
        else:
            template.draw(DrawableText(656, weaponY, weapon['stats']['S']))
        template.draw(DrawableText(713, weaponY, weapon['stats']['AP']))
        template.draw(DrawableText(777, weaponY, weapon['stats']['D']))

        if (weapon['stats']['Abilities'] != '_'):
            abilities[weaponName] = weapon['stats']['Abilities']
            template.draw(DrawableText(846, weaponY, 'Yes'))
        weaponY += weaponOffset

    # Wargear

    wargearNames = []

    for wargear in ork.wargear:
        wargearName = wargear['name']
        wargearNames.append(wargearName)
        if (wargear['stats']['Ability'] != '_'):
            abilities[wargearName] = wargear['stats']['Ability']

    wargearString = "Wargear: " + ", ".join(wargearNames)
    wargearStrings = wrap(wargearString, 50)

    # Only two lines for wargear.
    wargearY = 522
    wargearOffset = 35
    for i in range(min(len(wargearStrings), 2)):
        template.draw(DrawableText(39, wargearY, wargearStrings[i]))
        wargearY += wargearOffset

    # Abilities

    abilityNames = []

    if (ork.subFaction != None):
        abilityName = ork.subFaction['name']
        abilityNames.append(abilityName)
        abilities[abilityName] = ork.subFaction['Description']

    for ability in ork.abilities:
        abilityName = ability['name']
        abilityNames.append(abilityName)
        abilities[abilityName] = ability['stats']['Description']


    abilityString = "Abilities: " + ", ".join(abilityNames)
    abilityStrings = wrap(abilityString, 50)

    # Only four lines for abilities.
    abilityY = 595
    abilityOffset = 35
    for i in range(min(len(abilityStrings), 4)):
        template.draw(DrawableText(39, abilityY, abilityStrings[i]))
        abilityY += abilityOffset

    template.write(name+'.png')

    template = Image('templates/cardtemplate-back.png')
    template.fontPointsize(30)

    # Backside of the card
    abilityY = 117
    abilityOffset = 35

    # Abilities, also from weapons
    for abilityName in abilities.keys():
        abilityStrings = wrap(abilityName + ": " + abilities[abilityName], 60)
        for string in abilityStrings:
            template.draw(DrawableText(39, abilityY, string))
            abilityY += abilityOffset
        abilityY += 10
    template.write(name +  '-back.png')

if (__name__ == "__main__"):
    main()
