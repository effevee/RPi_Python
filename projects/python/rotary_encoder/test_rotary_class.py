import sys
import time
from rotary_class import RotaryEncoder

# Define GPIO inputs
PIN_A = 17  
PIN_B = 18
BUTTON = 27

# This is the event callback routine to handle events
def switch_event(event):
    if event == RotaryEncoder.CLOCKWISE:
        print("Clockwise")
    elif event == RotaryEncoder.ANTICLOCKWISE:
        print("Anticlockwise")
    elif event == RotaryEncoder.BUTTONDOWN:
        print("Button down")
    elif event == RotaryEncoder.BUTTONUP:
        print("Button up")
    return

# Define the switch
rswitch = RotaryEncoder(PIN_A, PIN_B, BUTTON, switch_event)

print("Pin A "+ str(PIN_A))
print("Pin B "+ str(PIN_B))
print("BUTTON "+ str(BUTTON))

# Listen
while True:
	time.sleep(0.5)

