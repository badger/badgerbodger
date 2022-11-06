# Blinky badger fun!
# To learn more see https://learn.pimoroni.com/article/getting-started-with-badger-2040

import badger2040
import time

badger = badger2040.Badger2040()

while True:
    badger.led(255)
    time.sleep(1)
    badger.led(0)
    time.sleep(1)