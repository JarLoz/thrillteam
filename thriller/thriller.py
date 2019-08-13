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
    # Name 
    template.fontPointsize(50)
    drawableName = DrawableText(38, 84, name)
    template.draw(drawableName)

    # Stats

    template.fontPointsize(45)

    drawableM = DrawableText(52, 185, ork.stats()['M'])
    drawableWS = DrawableText(135, 185, ork.stats()['WS'])
    drawableBS = DrawableText(230, 185, ork.stats()['BS'])
    drawableS = DrawableText(330, 185, ork.stats()['S'])
    drawableT = DrawableText(416, 185, ork.stats()['T'])
    drawableA = DrawableText(485, 185, ork.stats()['A'])
    drawableLd = DrawableText(566, 185, ork.stats()['Ld'])
    drawableSv = DrawableText(665, 185, ork.stats()['Sv'])

    template.draw(drawableM)
    template.draw(drawableWS)
    template.draw(drawableBS)
    template.draw(drawableS)
    template.draw(drawableT)
    template.draw(drawableA)
    template.draw(drawableLd)
    template.draw(drawableSv)

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
