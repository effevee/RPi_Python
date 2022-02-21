# Raspberry Pi Rotary Encoder Class
#
# Copyright 2011 Ben Buxton. Licenced under the GNU GPL Version 3.
# Contact: bb@cactii.net
#
# Arduino code ported & adapted by : Effevee
#
# A rotary encoder has 3 pins : two for the "bit" outputs, and a common (wiper).
# As the encoder turns, the bit pins change according to a Gray Code sequence as follows: 
#
#   Position    A      B
#   ----------------------
#     Step1     0      0
#      1/4      1      0
#      1/2      1      1
#      3/4      0      1
#     Step2     0      0
#
# From this table, we can see that when moving from one 'click' to
# the next, there are 4 changes in the output code.
#
# - Step 1 -> pos 1/4  : 00 -> 10
# - pos 1/4 -> pos 1/2 : 10 -> 11
# - pos 1/2 -> pos 3/4 : 11 -> 01 
# - pos 3/4 -> Step 2  : 01 -> 00
#
# Detecting the direction is easy - the table simply goes in the other
# direction (read up instead of down).
#
# To decode this, we use a simple state machine. Every time the output
# code changes, it follows state, until finally a full steps worth of
# code is received (in the correct order). At the final 0-0, it returns
# a value indicating a step in one direction or the other.
#
# It's also possible to use 'half-step' mode. This just emits an event
# at both the 0-0 and 1-1 positions. This might be useful for some
# encoders where you want to detect all positions.
#
# If an invalid state happens (for example we go from '0-1' straight
# to '1-0'), the state machine resets to the start until 0-0 and the
# next valid codes occur.
#
# The biggest advantage of using a state machine over other algorithms
# is that this has inherent debounce built in. Other algorithms emit spurious
# output with switch bounce, but this one will simply flip between
# sub-states until the bounce settles, then continue along the state
# machine.
#
# A side effect of debounce is that fast rotations can cause steps to
# be skipped. By not requiring debounce, fast rotations can be accurately
# measured.
# Another advantage is the ability to properly handle bad state, such
# as due to EMI, etc.
# It is also a lot simpler than others - a static state table and less
# than 10 lines of logic.

import sys
import RPi.GPIO as GPIO
import threading

# State table have, for each state (row), the new state
# to set based on the next encoder output. From left to right in
# the table, the encoder outputs are 00, 01, 10, 11, and the value
# in that position is the new state to set.

# 7 valid codes of 3 bits for full state table
# emit 1 event for full sequence
# CW sequence:  00 -> 10 -> 11 -> 01 -> 00
# CCW sequence: 00 -> 01 -> 11 -> 10 -> 00
# bit 1: switch A
# bit 2: switch B
# bit 3: direction 0=CW, 1=CCW
R_START     = 0b000
R_CW_BEGIN  = 0b010
R_CW_NEXT   = 0b011
R_CW_FINAL  = 0b001
R_CCW_START = 0b100
R_CCW_BEGIN = 0b101
R_CCW_NEXT  = 0b111
R_CCW_FINAL = 0b110

# valid full state table
STATE_TAB = (
  # R_START
  (R_START,      R_CCW_BEGIN,  R_CW_BEGIN,  R_START),
  # R_CW_FINAL
  (R_START,      R_CW_FINAL,   R_START,     R_CW_NEXT),
  # R_CW_BEGIN
  (R_START,      R_START,      R_CW_BEGIN,  R_CW_NEXT),
  # R_CW_NEXT
  (R_START,      R_CW_FINAL,   R_CW_BEGIN,  R_CW_NEXT),
  # R_CCW_BEGIN
  (R_START,      R_CCW_BEGIN,  R_START,     R_CCW_NEXT),
  # R_CCW_FINAL
  (R_CCW_START,  R_START,      R_CCW_FINAL, R_CCW_NEXT),
  # R_CCW_NEXT
  (R_START,      R_CCW_BEGIN,  R_CCW_FINAL, R_CCW_NEXT),
)


# The Raspberry Pi GPIOs have internal 10K pull-up resistors
# Rotary encoders need these to be set to GPIO.PUD_UP
# However, KY-040 encoders have their own physical 10K pull-up resistors 
# In such a case set resistor=GPIO.PUD_OFF in the initialisation call
# otherwise there will be two 10K resistors paralleled across each other giving 5K

class RotaryEncoder:
    state = R_START
    pinA = None
    pinB = None
    CLOCKWISE=1
    ANTICLOCKWISE=2
    BUTTONDOWN=3
    BUTTONUP=4

    def __init__(self, pinA, pinB, button, callback, pullup=GPIO.PUD_UP):
        t = threading.Thread(target=self._run, args=(pinA, pinB, button, callback, pullup,))
        t.daemon = True
        t.start()

    def _run(self, pinA, pinB, button, callback, pullup):
        self.pinA = pinA
        self.pinB = pinB
        self.button = button
        self.callback = callback
        self.pullup = pullup

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        try:
            # The following lines enable the internal pull-up resistors
            if pinA > 0 and pinB > 0:
                # internal pull-up resistors on pins
                gpio = self.pinA
                GPIO.setup(self.pinA, GPIO.IN, pull_up_down=self.pullup)
                GPIO.setup(self.pinB, GPIO.IN, pull_up_down=self.pullup)
                # add event detection on pin changes
                gpio = self.pinB
                GPIO.add_event_detect(self.pinA, GPIO.BOTH, callback=self.rotary_event)
                GPIO.add_event_detect(self.pinB, GPIO.BOTH, callback=self.rotary_event)

            if button > 0:
                # internal pull-up resistor on button
                gpio = self.button
                GPIO.setup(self.button, GPIO.IN, pull_up_down=self.pullup)
                # add event detection on button changes
                GPIO.add_event_detect(self.button, GPIO.FALLING, callback=self.button_event, bouncetime=150)

        except Exception as e:
            print("Rotary Encoder initialise error GPIO %s %s" % (gpio,str(e)))
            sys.exit(1)

    # Call back routine for switch events
    def rotary_event(self, switch):
        # Grab state of input pins.
        pinstate = (GPIO.input(self.pinB) << 1) | GPIO.input(self.pinA)
        # Determine new state from the pins and state table.
        self.state = STATE_TAB[self.state & 0xf][pinstate]
        # Return emit bits, ie the generated event.
        result = self.state & 0x30
        if result:
            event = self.CLOCKWISE if result == 32 else self.ANTICLOCKWISE
            self.callback(event)
            return result

    # Call back routine for button events
    def button_event(self, button):
        # Ignore Button Up events   
        if not GPIO.input(button): 
            event = self.BUTTONDOWN 
            self.callback(event)
        return

    # Get a button state - returns 1 or 0
    def getButtonState(self, button):
        return  GPIO.input(button)

    def buttonPressed(self,button):
        state = self.getButtonState(button) 
        if state == 1:
            pressed = False
        else:
            pressed = True
        return pressed

# End of class


# ### Test routine ###
# 
# Names = ['NO_EVENT', 'CLOCKWISE', 'ANTICLOCKWISE', 'BUTTON DOWN', 'BUTTON UP']
# 
# # Volume event - test only - No event generation
# def volume_event(event):
#     name = ''
#     try:
#         name = Names[event]
#     except:
#         name = 'ERROR'
# 
#     print("Volume event ", event, name)
#     return
# 
# # Tuner event - test only - No event generation
# def tuner_event(event):
#     name = ''
#     try:
#         name = Names[event]
#     except:
#         name = 'ERROR'
# 
#     print("Tuner event ", event, name)
#     return
# 
# if __name__ == "__main__":
# 
#     from config_class import Configuration
#     config = Configuration()
# 
#     print("Test rotary encoder Class")
# 
#     # Get configuration
#     left_switch = config.getSwitchGpio("left_switch")
#     right_switch = config.getSwitchGpio("right_switch")
#     mute_switch = config.getSwitchGpio("mute_switch")
#     down_switch = config.getSwitchGpio("down_switch")
#     up_switch = config.getSwitchGpio("up_switch")
#     menu_switch = config.getSwitchGpio("menu_switch")
# 
#     print("Left switch GPIO", left_switch)
#     print("Right switch GPIO", right_switch)
#     print("Up switch GPIO", up_switch)
#     print("Down switch GPIO", down_switch)
#     print("Mute switch GPIO", mute_switch)
#     print("Menu switch GPIO", menu_switch)
#     
#     volumeknob = RotaryEncoder(left_switch,right_switch,mute_switch, volume_event)
#     tunerknob = RotaryEncoder(down_switch,up_switch,menu_switch, tuner_event)
# 
#     try:
#         while True:
#             time.sleep(0.05)
# 
#     except KeyboardInterrupt:
#         print(" Stopped")
#         sys.exit(0)
# 
# 
# # End of script
# # set tabstop=4 shiftwidth=4 expandtab
# # retab
