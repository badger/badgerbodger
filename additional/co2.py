# Detect the mouth breathers with a CO2 sensing Qw/ST compatible breakout
# https://shop.pimoroni.com/products/scd41-co2-sensor-breakout

import time

import badger2040
import pimoroni_i2c
import breakout_scd41

PINS_STEMMA = {"sda": 4, "scl": 5}

i2c = pimoroni_i2c.PimoroniI2C(**PINS_STEMMA)

breakout_scd41.init(i2c)
breakout_scd41.start()

badger = badger2040.Badger2040()

badger.font("sans") # Set font
badger.thickness(2) # Set line thickness

# Write text to screem
badger.text("CO2", 20, 20)
badger.text("Temp", 20, 60)
badger.text("Hum", 20, 100)
badger.update()


while True:
    if breakout_scd41.ready():
        co2, temperature, humidity = breakout_scd41.measure()
        # Clear text
        badger.pen(15)
        badger.rectangle(120,0, badger2040.WIDTH-120, badger2040.HEIGHT)
        # Write text to screem
        badger.pen(0)
        badger.text("{:.0f}".format(co2), 120, 20)
        badger.text("{:.0f}".format(temperature), 120, 60)
        badger.text("{:.0f}%".format(humidity), 120, 100)
        print(co2, temperature, humidity)
        # Update the screen
        
        badger.update_speed(badger2040.UPDATE_FAST)
        badger.update()

        time.sleep(300.0)
        
