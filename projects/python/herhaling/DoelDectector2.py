import random

aantalGoals = 0
aantalPaal = 0
aantalSjots = 100
diktePaal = 10
x_max = 900
y_max = 500

# lus sjots
for sjot in range(aantalSjots):
    # sjot de bal
    x = random.randint(0, x_max)
    y = random.randint(0, y_max)
    # paal ?
    if x>300 and x<=310 and y<=230:     # linkerpaal
        aantalPaal += 1
    elif x>600 and x<=610 and y<=230:   # rechterpaal
        aantalPaal += 1
    elif x>300 and x<=610 and y>220 and y<= 230:   # deklat
        aantalPaal += 1
    # goal ?
    if x>300 and x <600 and y>0 and y <220:
        aantalGoals += 1

# resultaat na 10 shots
print('{} goals en {} op de paal in {} sjots'.format(aantalGoals, aantalPaal, aantalSjots))

