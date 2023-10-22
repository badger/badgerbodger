# Badger Bodger Scanner

For GitHub Universe 2023, we built out a device that can scan a badge and generate
the appropriate files to them copy over onto the connected badger flashed with
a default image fresh from the Pimoroni factory in Sheffield.

## Hardware
- Raspberry Pi 4 Model B – 4GB RAM
- 64GB MicroSD Card
- Hyperpixel 4.0 Touchscreen Display [UK](https://shop.pimoroni.com/products/hyperpixel-4?variant=12569485443155)
- [3D printed case](https://www.printables.com/model/121395-case-for-hyperpixel-40-with-raspberrypi-4)
- 2D Barcode Scanner
- USB-A to USB-C cable
- USB-C Power Supply (multi-region)

## Initial Setup
The Hyperpixel 4.0 display comes with all the hardware you need to build the unit in combination with the 3D printed case. 

- Install the GPIO pin expansion header onto the Raspberry Pi
- Screw in the PCB standoffs to the back of the Hyperpixel 4.0
- Insert the Raspberry Pi into the 3D printed case (note, a bit of jiggling is required as it's snug fit)
- Connect the Hyperpixel 4.0 to the Raspberry Pi using the GPIO pins and push down gently
- Screw in the Hyperpixel 4.0 and Raspberry Pi to the 3D printed case using the screws provided

## Preparing the SD Card
Note that Raspbian Bookworm was released during the construction of the badge scanners, however it looked like it contained lots of changes to the desktop environment and how python operates that I haven't tested with it yet or got working.  Therefore, when using Raspberry Pi Imager to flash the SD card, I used the "Raspberry PI OS (Legacy)" opetion which is located under the "Raspberry Pi OS (other)" section.

In advanced options (the little gear icon), the following options were selected:
- Set hostname to "scannerXX" where XX is the number of the scanner
- Enable SSH using password authentication
- Set the user to `badger` and password to the one stored in the password manager
- Configure Wireless LAN to connect to the appropriate network
- Set the locale to `US/Pacific` and keyboard layout to `US`

Once Raspbian is flashed to the SD card, re-insert it into the computer and edit the `firstrun.sh` script to include the following
just before the last 3 lines of the script (i.e. just before) `rm -f /boot/firstrun.sh`

```
# Create the install.sh script to clone a git repo, then run firstrun.sh in it
mkdir -p /home/badger/.config/autostart
cat << EOF > /home/badger/install.sh
#!/bin/bash
sleep 30
git clone --branch prod https://github.com/badger2040/badgerbodger.git /home/badger/badgerbodger
chmod +x /home/badger/badgerbodger/firstrun.sh
/bin/bash /home/badger/badgerbodger/firstrun.sh
rm /home/badger/.config/autostart/install.desktop
# rm /home/badger/install.sh
exit 0
EOF

# Run the install.sh script on boot
cat << EOF > /home/badger/.config/autostart/install.desktop
[Desktop Entry]
Name=Install
Exec=/bin/bash /home/badger/install.sh
EOF
chown -R badger:badger /home/badger

```

Then finally edit the config.txt file and add the following to the bottom of the file:
```
# Hyperpixel 4.0
dtoverlay=vc4-kms-dpi-hyperpixel4
dtparam=rotate=180
```
