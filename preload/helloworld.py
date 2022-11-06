# To learn more see https://learn.pimoroni.com/article/getting-started-with-badger-2040

import badger2040
badger = badger2040.Badger2040()

badger.pen(0)       # Set pen color from black (0) to white (15)
badger.font("sans") # Set font
badger.thickness(2) # Set line thickness

# Write text to screem
badger.text("Let's build", 20, 40)
badger.text("from here", 20, 80)

# Update the screen
badger.update()
