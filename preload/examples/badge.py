import badger2040
import jpegdec

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

LEFT_PADDING = 5
NAME_HEIGHT = 50
LASTNAME_HEIGHT = 30
DETAILS_HEIGHT = 20
TEXT_WIDTH = WIDTH - LEFT_PADDING
LINE_SPACING = 2
DETAILS_TEXT_SIZE = 0.5 

BADGE_PATH = "/badges/badge.txt"
BADGE_BACKGROUND = "/badges/back.jpg"


# Will be replaced with badge.txt
# "Universe 2023", first_name, lastname_name, company, title, pronouns to the file on separate lines.
DEFAULT_TEXT = """Universe 2023
Mona Lisa
Octocat
GitHub
Company Mascot
she/her
@mona
"""

# ------------------------------
#      Utility functions
# ------------------------------


# Reduce the size of a string until it fits within a given width
def truncatestring(text, text_size, width):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            text += ""
            return text


# ------------------------------
#      Drawing functions
# ------------------------------

# Draw the badge, including user text
def draw_badge():
    display.set_pen(15)
    display.clear()
    
    # Draw the background
    try:
        jpeg.open_file(BADGE_BACKGROUND)
        jpeg.decode(0, 0)
    except OSError:
        print("Badge background error")

    # Draw the firstname, scaling it based on the available width
    display.set_pen(0)
    display.set_font("sans")
    display.set_thickness(3)
    name_size = 1.0  # A sensible starting scale
    while True:
        name_length = display.measure_text(first_name, name_size)
        if name_length >= TEXT_WIDTH and name_size >= 0.1:
            name_size -= 0.01
        else:
            display.text(first_name, LEFT_PADDING, 20, TEXT_WIDTH, name_size)
            break

    # Draw the lastname, scaling it based on the available width
    display.set_pen(0)
    display.set_font("sans")
    display.set_thickness(2)
    lastname_size = 0.7  # A sensible starting scale
    while True:
        lastname_length = display.measure_text(last_name, lastname_size)
        if lastname_length >= TEXT_WIDTH and lastname_size >= 0.1:
            lastname_size -= 0.01
        else:
            display.text(last_name, LEFT_PADDING, NAME_HEIGHT + LINE_SPACING, TEXT_WIDTH, lastname_size)
            break

    # Draw the title and pronouns, aligned to the bottom & truncated to fit on one line
    display.set_pen(0)
    display.set_font("sans")

    display.text(title, LEFT_PADDING, HEIGHT - (DETAILS_HEIGHT * 2) - LINE_SPACING, TEXT_WIDTH, DETAILS_TEXT_SIZE)
    display.text(pronouns, LEFT_PADDING, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_TEXT_SIZE)
    
    display.update()


# ------------------------------
#        Program setup
# ------------------------------

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)
display.set_thickness(2)

jpeg = jpegdec.JPEG(display.display)

# Open the badge file
try:
    badge = open(BADGE_PATH, "r")
except OSError:
    with open(BADGE_PATH, "w") as f:
        f.write(DEFAULT_TEXT)
        f.flush()
    badge = open(BADGE_PATH, "r")

# Read in the next 6 lines
# "Universe 2023", first_name, lastname_name, company, title, pronouns, handle from the file on separate lines.
DEFAULT_TEXT = """Universe 2023
Mona Lisa
Octocat
GitHub
Company Mascot
she/her
@mona
"""
try:
    event = badge.readline()         # "Universe 2023"
    first_name = badge.readline()    # "Mona Lisa"
    last_name = badge.readline()     # "Octocat"
    company = badge.readline()       # "GitHub"
    title = badge.readline()         # "Company Mascot"
    pronouns = badge.readline()      # "she/her"
    # handle = badge.readline()        # "@mona"
    
    
    # Truncate Title and pronouns to fit
    title = truncatestring(title, DETAILS_TEXT_SIZE, 110)
    pronouns = truncatestring(pronouns, DETAILS_TEXT_SIZE, 110)
    
finally:
    badge.close()

# ------------------------------
#       Main program
# ------------------------------

draw_badge()

while True:
    # Sometimes a button press or hold will keep the system
    # powered *through* HALT, so latch the power back on.
    display.keepalive()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()

