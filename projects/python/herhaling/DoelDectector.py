import random
import time

aantalGoals = 0
aantalSjots = 10
x_max = 900
y_max = 500

# lus sjots
for sjot in range(aantalSjots):
    # toon sjot nr
    print(sjot+1, end=' ')
    # sjot de bal
    x = random.randint(0, x_max)
    y = random.randint(0, y_max)
    # goal ?
    if x>300 and x<600 and y<220:
        aantalGoals += 1
    # even wachten
    time.sleep(0.5)

# resultaat na 10 shots
print()
print('{} goals in {} sjots'.format(aantalGoals, aantalSjots))
