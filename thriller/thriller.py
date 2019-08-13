from thriller.parse import parse
from thriller.readlist import readlist
from thriller.ork import Ork
from pgmagick import Image, DrawableText

def main():
    orks = createOrks()
    for o in orks:
        createCard(o)

def createCard(ork):
    template = Image('cardtemplate.png')
    name = ork.name()
    abilities = {}
    # Name 
    template.fontPointsize(50)
    drawableName = DrawableText(38, 84, name)
    template.draw(drawableName)

    # Stats

    template.fontPointsize(45)

    template.draw(DrawableText(52, 185, ork.stats()['M']))
    template.draw(DrawableText(135, 185, ork.stats()['WS']))
    template.draw(DrawableText(230, 185, ork.stats()['BS']))
    template.draw(DrawableText(330, 185, ork.stats()['S']))
    template.draw(DrawableText(416, 185, ork.stats()['T']))
    template.draw(DrawableText(485, 185, ork.stats()['A']))
    template.draw(DrawableText(566, 185, ork.stats()['Ld']))
    template.draw(DrawableText(665, 185, ork.stats()['Sv']))

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
        template.draw(DrawableText(43, weaponY, weaponName))
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

    template.write(name+'.png')


def createOrks():
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
    main
