import time
import badger2040
import badger_os
import machine
import json
import contribution_graph

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

# Size of QR Code 
QRCODE_SIZE = 112

# Will be replaced with badge.txt
DEFAULT_TEXT = """Universe 2022
Mona
Octocat
@github"""

# Allocate memory to load QR Code image 
QRCODE = bytearray(int(QRCODE_SIZE * QRCODE_SIZE / 8))

CURRENT_PAGE = 0 # 0=Badge; 1=contribution graph

# Load QR Code image
try:
    open("gh_qrcode.bin","rb").readinto(QRCODE)
except OSError:
    try:
        import gh_qrcode
        QRCODE = bytearray(gh_qrcode.data())
        del gh_qrcode
    except ImportError:
        pass


# ------------------------------
#      Drawing functions
# ------------------------------

# Draw the badge, including user text
def draw_badge():

    
    #Draw white background
    display.pen(15)
    display.rectangle(0,0, WIDTH, HEIGHT)
    
    #QR CODE
    display.image(QRCODE, QRCODE_SIZE,QRCODE_SIZE,WIDTH-100,28)
    
    # Draw header background
    display.pen(0)
    display.rectangle(0,0,WIDTH,30)
    
    # Draw header text
    display.pen(15)
    display.font("serif")
    display.thickness(2)
    display.text(title, 70, 16, 0.6)
    
    # Draw GitHub handle text
    display.pen(0)
    display.font("sans")
    display.thickness(2)
    display.text(github_handle, 8, 114, 0.65)
    
    # Draw Line
    display.thickness(2)
    display.line(8, 94, WIDTH-116, 94)
    
    # Draw name
    display.thickness(3)
    display.text(first_name, 8, 50, 0.75)
    display.text(last_name, 8, 74, 0.75)


def draw_page():
# match case not available, using if-else
    if CURRENT_PAGE == 0:
        draw_badge()
    elif CURRENT_PAGE == 1 or CURRENT_PAGE == 2:
        contribution_graph.draw_contribution_graph(display)
    display.update()


def open_launcher():
    # Changing state to set running application as launcher
    state = {"running": "launcher", "page": 1}
    
    # Saving the state file
    try:
        with open("/state/launcher.json", "w") as f:
            f.write(json.dumps(state))
            f.flush()
            
    except OSError:
        # State file does not exist, create it
        import os
        try:
            os.stat("/state")
        except OSError:
            os.mkdir("/state")
            state_save("launcher", state)
    
    # Clear the display and reset device
    display.update_speed(badger2040.UPDATE_TURBO)
    display.clear()
    display.update()
    machine.reset()
    
    
    
# ------------------------------
#        Program setup
# ------------------------------

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

# Open the badge file
try:
    badge = open("badge.txt", "r")
except OSError:
    with open("badge.txt", "w") as f:
        f.write(DEFAULT_TEXT)
        f.flush()
    badge = open("badge.txt", "r")

# Read in the next 3 lines
title = badge.readline()        # "Universe 2022"
first_name = badge.readline().upper()   # "Mona"
last_name = badge.readline().upper()    # "Octocat"
github_handle = badge.readline()# "@github"




# ------------------------------
#       Main program
# ------------------------------

draw_page()

while True:
    
    
    # Buttons UP / DOWN to view previous / next page of contribution graph
    if CURRENT_PAGE == 1 and (display.pressed(badger2040.BUTTON_DOWN) or display.pressed(badger2040.BUTTON_UP)):
        contribution_graph.CONTRIBUTION_GRAPH_PAGE = 1 if contribution_graph.CONTRIBUTION_GRAPH_PAGE == 0 else 0
        draw_page()

    # Button A opens launcher
    elif display.pressed(badger2040.BUTTON_A):
        open_launcher()
    
    # Button B sets current page to Badge
    elif CURRENT_PAGE != 0 and display.pressed(badger2040.BUTTON_B):
        CURRENT_PAGE = 0
        draw_page()
        
    # Button C sets current page to Contribution Graph
    elif CURRENT_PAGE != 1 and display.pressed(badger2040.BUTTON_C):
        CURRENT_PAGE = 1
        contribution_graph.CONTRIBUTION_GRAPH_PAGE = 0
        draw_page()
        
    # if incorrect button pressed, show popup info for 5 seconds
    elif display.pressed(badger2040.BUTTON_A) or display.pressed(badger2040.BUTTON_B) or display.pressed(badger2040.BUTTON_C) or display.pressed(badger2040.BUTTON_UP) or display.pressed(badger2040.BUTTON_DOWN):
        badger_os.warning(display, "a = launcher   b = badge   c = contributions")
        time.sleep(5)
        draw_page()


    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()