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