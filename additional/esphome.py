# Example that connects to an esphome coprocessor
# The D1 Mini is connected over the stemma port

import badger2040
import time
import pngdec
from machine import Pin

BUTTON_A = "buttonA"
BUTTON_B = "buttonB"
state = {BUTTON_A: 0, BUTTON_B: 0}

display = badger2040.Badger2040()
display.led(128)
display.clear()

display.set_update_speed(badger2040.UPDATE_FAST)
png = pngdec.PNG(display.display)

changed = True

def wait_for_user_to_release_buttons():
    while display.pressed_any():
        time.sleep(0.01)

def draw_badge():
    display.clear()
    
    if state[BUTTON_A] == 1:
        BADGE_IMAGE = "bulb-on.png"
    else:
        BADGE_IMAGE = "bulb-off.png"
    
    try:
        png.open_file(BADGE_IMAGE)
        png.decode(0, 0)
    except OSError:
        print("Badge background error")
    
    display.update()
    
        
# Update the pins on the switch
def update_pins(a, b):
  wait_for_user_to_release_buttons()
    
  buttonA = Pin(4, Pin.OUT)
  buttonB = Pin(5, Pin.OUT)

  buttonA.value(a)
  buttonB.value(b)
  

# Main loop
# Note this implementation is super power innefficient
# as it's for on-stage use.

while True:
    display.keepalive()

    if display.pressed(badger2040.BUTTON_A):
        if state[BUTTON_A] == 1:
            state[BUTTON_A] = 0
        else:
            state[BUTTON_A] = 1
        changed = True

    if display.pressed(badger2040.BUTTON_B):
        if state[BUTTON_B] == 1:
            state[BUTTON_B] = 0
        else:
            state[BUTTON_B] = 1
        changed = True

    if changed:
        update_pins(state[BUTTON_A],state[BUTTON_B])
        draw_badge()
        changed = False

