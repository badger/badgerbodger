import time
import math

from pimoroni_i2c import PimoroniI2C

PINS_STEMMA = {"sda": 4, "scl": 5}

i2c = PimoroniI2C(**PINS_STEMMA)

print('Scan i2c bus...')
devices = i2c.scan()
 
if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))
 
  for device in devices:  
    print("Decimal address: ",device," | Hex address: ",hex(device))
