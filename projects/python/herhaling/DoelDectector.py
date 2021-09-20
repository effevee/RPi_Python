import random

aantalGoals = 0
aantalSjots = 10
x_max = 900
y_max = 500

# lus sjots
for sjot in range(aantalSjots):
    # sjot de bal
    x = random.randint(0, x_max)
    y = random.randint(0, y_max)
    # goal ?
    if x>300 and x <600 and y>0 and y <220:
        aantalGoals += 1

# resultaat na 10 shots
print('{} goals in {} sjots'.format(aantalGoals, aantalSjots))
