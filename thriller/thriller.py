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
    
    template.fontPointsize(50)
    drawableName = DrawableText(38, 84, name)
    template.draw(drawableName)
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
    main()
