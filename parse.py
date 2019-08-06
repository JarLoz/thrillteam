from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring

#header for some xml bullshit
h = '{http://www.battlescribe.net/schema/catalogueSchema}'
def main():
    f = open("../wh40k-killteam/Orks.cat", "r")
    orksxml = f.read()
    f.close()

    orksdict = bf.data(fromstring(orksxml))

    sharedEntries = orksdict[list(orksdict.keys())[0]][h+'sharedSelectionEntries'][h+'selectionEntry']
    sharedProfiles = orksdict[list(orksdict.keys())[0]][h+'sharedProfiles'][h+'profile']

    return parseSharedEntries(sharedEntries, sharedProfiles)

def parseSharedEntries(sharedEntries, sharedProfiles):
    profiles = {'Model':{}, 'Weapon':{}, 'Ability':{}, 'Wargear':{}}

    for entry in sharedEntries:
        if (h+'profiles' in entry.keys()):
            profiledata = entry[h+'profiles'][h+'profile']
            if (isinstance(profiledata, list) == False):
                profiledata = [profiledata]
            for p in profiledata:
                profile = parseProfile(p)
                profiles[profile['typeName']][profile['name']] = profile
        else:
            continue

    for p in sharedProfiles:
        profile = parseProfile(p)
        profiles[profile['typeName']][profile['name']] = profile

    return profiles

def parseProfile(p):
    name = p['@name']
    typeName = p['@typeName']
    pid = p['@id']
    characteristics = p[h+'characteristics'][h+'characteristic']
    if (isinstance(characteristics, list) == False):
        characteristics = [characteristics]
    stats = {}
    for c in  characteristics:
        try:
            stats[c['@name']] = c['$'].replace('\n', '')
        except:
            continue
    return ({'name': name, 'typeName': typeName, 'id': pid, 'stats': stats})

if (__name__ == "__main__"):
    main()
