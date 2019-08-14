from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring

#header for some xml bullshit
h = '{http://www.battlescribe.net/schema/catalogueSchema}'
s = '{http://www.battlescribe.net/schema/gameSystemSchema}'

def parse(datapath, faction):
    f = open(datapath + faction + '.cat', "r")
    orksxml = f.read()
    f.close()

    orksdict = bf.data(fromstring(orksxml))

    sharedEntries = orksdict[list(orksdict.keys())[0]][h+'sharedSelectionEntries'][h+'selectionEntry']
    sharedProfiles = orksdict[list(orksdict.keys())[0]][h+'sharedProfiles'][h+'profile']
    subFactions = orksdict[list(orksdict.keys())[0]][h+'rules'][h+'rule']

    f = open(datapath + 'Warhammer 40,000 Kill Team.gst', "r")
    commonxml = f.read()
    f.close()

    commonDict = bf.data(fromstring(commonxml))

    specialistProfiles = commonDict[s+'gameSystem'][s+'sharedProfiles'][s+'profile']

    profiles = {'Model':{}, 'Weapon':{}, 'Ability':{}, 'Wargear':{}, 'Sub-faction':{}, 'Psychic Power':{}}

    for entry in sharedEntries:
        if (h+'profiles' in entry.keys()):
            entryName = entry['@name']
            profiledata = entry[h+'profiles'][h+'profile']
            if (isinstance(profiledata, list) == False):
                profiledata = [profiledata]
            for p in profiledata:
                profile = parseProfile(p, h, entryName)
                profiles[profile['typeName']][profile['name']] = profile
        else:
            continue

    for p in sharedProfiles:
        profile = parseProfile(p, h)
        profiles[profile['typeName']][profile['name']] = profile

    for r in subFactions:
        name = r['@name']
        start = name.find('(') + 1
        end = name.find(')')
        name = name[start:end]
        profiles['Sub-faction'][name] = {'name': name, 'Description' : r[h+'description']['$']}

    for c in specialistProfiles:
        profile = parseProfile(c, s)
        profiles[profile['typeName']][profile['name']] = profile

    return profiles

def parseProfile(p, header, entryName=''):
    name = p['@name']
    typeName = p['@typeName']
    if (typeName == 'Model' and entryName):
        name = entryName
    pid = p['@id']
    characteristics = p[header+'characteristics'][header+'characteristic']
    if (isinstance(characteristics, list) == False):
        characteristics = [characteristics]
    stats = {}
    for c in  characteristics:
        try:
            if (isinstance(c['$'], str)):
                stats[c['@name']] = c['$'].replace('\n', '')
            else:
                stats[c['@name']] = str(c['$'])
        except:
            continue
    return ({'name': name, 'typeName': typeName, 'id': pid, 'stats': stats})
