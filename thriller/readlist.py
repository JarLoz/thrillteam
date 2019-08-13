def readlist():
    f = open("orklist.txt", "r")
    lines = f.readlines()
    f.close()

    lines = [x.strip() for x in lines]
    orks = []
    ork = {}
    for line in lines:
        if (line == '-'):
            orks.append(ork)
            ork = {}
            continue
        split = line.split(':')
        key = split[0]
        value = split[1].strip()
        if (key == 'Model'):
            ork[key] = value
        else:
            if (key not in ork.keys()):
                ork[key] = []
            ork[key].append(value)
    orks.append(ork)

    return orks
