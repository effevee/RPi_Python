### strings
school="CVO"
print("lengte van de string CVO:",len(school))  # len() is een functie
# maak variabele groet
groet="Welkom bij"
# maak zin: Welkom bij het CVO
zin=groet+" het "+school
print(zin)
# vervang CVO door cvo in zin
zin=zin.replace('CVO', 'cvo')   # .replace() is een method
print(zin)

### lijsten
rugzak=["zeep","tandpasta","water","appel","banaan","mondmasker"]
# aantal elementen in lijst
print("aantal elementen in de rugzak:",len(rugzak))
# print element 'banaan' uit lijst rugzak
print(rugzak[4])          # index vooraan beginnen
print(rugzak[-2])         # index achteraan beginnen
# maak een minirugzak en stop daarin : tandpasta, water en appel
miniRugzak=rugzak[1:4]    # beginindex = 1ste element / eindindex = laatste element + 1
print(miniRugzak)
# stop wodka tussen zeep en tandpasta
rugzak.insert(1, "wodka")
print(rugzak)
# eet de banaan op
rugzak.remove("banaan")
print(rugzak)
# haal de index op van water
print("water staat op index {}".format(rugzak.index("water")))
# nieuwe lijst
onevenRugzak = []
# vul de nieuwe lijst op met de oneven items van rugzak
for i in range(len(rugzak)):
    if i%2 != 0:
        onevenRugzak.append(rugzak[i])
print("inhoud oneven rugzak:", onevenRugzak)

# module voor random getallen
import random
# maak een lijstRand van 20 random getallen tussen 0 en 100
lijstRand = []
for i in range(20):
    lijstRand.append(random.randint(0,100))
print("lijst met 20 random getallen tussen 0 en 100:",lijstRand)
# kortere manier
lijstRand2 = [random.randint(0,100) for i in range(20)]
print("lijst met 20 random getallen tussen 0 en 100:",lijstRand2)
# maak een functie even_minus_oneven die de som van de even getallen aftrekt van de som van de oneven getallen
# de functie retourneert het resultaat en als parameter verwacht de functie een lijst
def even_minus_oneven(getallenRij):
    som_even = 0
    som_oneven = 0
    for getal in getallenRij:
        if getal%2 == 0:
            som_even += getal
        else:
            som_oneven += getal
    return (som_even - som_oneven)
print("functie even_minus_oneven van de lijstRand geeft als resultaat:", even_minus_oneven(lijstRand))
