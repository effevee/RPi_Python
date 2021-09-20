import os

DEBUG = True

try:
    # maak databestand aan met groepen van user pi
    os.system("groups > /home/pi/RPi_Python/projects/python/data/piG.dat")
    
    # lees het databestand
    piGroups = ""
    with open('/home/pi/RPi_Python/projects/python/data/piG.dat', 'r') as f:    # eenmaal with wordt verlaten wordt het bestand gesloten
        piGroups = f.read()
    if DEBUG: print(piGroups)
    
    # splits de string op spaties om een lijst te vormen
    piList = piGroups.split(" ")
    piList[-1] = piList[-1][:-1]     # \n van laatste element verwijderen
    if DEBUG: print(piList)
    
    # lengte van de lijst
    print('lengte van de lijst: {}'.format(len(piList)))
    
    # kortste woord en positie
    kortste = min(piList, key=len)
    print("het kortste woord {} staat op positie {}".format(kortste, piList.index(kortste)))
    
    # langste woord en positie
    langste = max(piList, key=len)
    print("het langste woord {} staat op positie {}".format(langste, piList.index(langste)))
    
    # verwijder kortste en langste woord uit de lijst
    piList.remove(kortste)
    piList.remove(langste)
    if DEBUG: print(piList)
    
    # lijst omzetten naar string met spaties
    piGroupsChanged = " ".join(piList)
    if DEBUG: print(piGroupsChanged)
    
    # schrijf de aangepaste string naar een nieuw bestand
    with open('/home/pi/RPi_Python/projects/python/data/piGChanged.dat', 'w') as f:
        f.write(piGroupsChanged + '\n')
    
except Exception as E:
    print('probleem met uitvoeren commando of lezen bestand')
    if DEBUG:
        print(E)