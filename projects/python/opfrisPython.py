school="CVO"
print("lengte van de string CVO:",len(school))  # len() is een functie

groet="Welkom bij"

zin=groet+" het "+school
print(zin)

zin=zin.replace('CVO', 'cvo')   # .replace() is een method
print(zin)

rugzak=["zeep","tandpasta","water","appel","banaan","mondmasker"]
print("aantal elementen in de rugzak:",len(rugzak))
print(rugzak[4])     # index vooraan beginnen
print(rugzak[-2])    # index achteraan beginnen

miniRugzak=rugzak[1:4]    # beginindex = 1ste element / eindindex = laatste element + 1
print(miniRugzak)