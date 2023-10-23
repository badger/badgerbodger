# Badger Bodger
At GitHub events, the Badger 2040 is pre-loaded with data to personalise it to the individual with data taken from their attendee registration barcode. This repo contains the scripts for the badge customization code.  At the event this runs on a Raspberry Pi with a 2D barcode scanner attached, however it can also run on laptop (tested on macOS).  It is assumed that the Badger 2040 is running a stock Badger OS image as flashed from the[Pimoroni](https://pimoroni.com/) Factory in Sheffield. The scripts were tested against [this Badger OS image](https://github.com/pimoroni/badger2040/releases/tag/v0.0.4).

## Badger Modifications
On top of the stock Badger OS image, the following changes are made:
- A GitHub event branded [badge.py](preload/examples/badge.py) that displays the attendee name with a background image and corresponding badge.txt file containing the personalised data
- The [Book of Mona](preload/books/mona.txt), and updated [ebook.py](preload/examples/ebook.py) that points to it
- Some [pre-loaded QR Codes](preload/qrcodes/)
- Some [pre-loaded images](preload/images/)

## Running on a laptop
Install the latest version of python 3 via homebrew
```
brew install python
```

Install Python prerequisites
```
pip3 install -r scripts/requirements.txt
```

Run the GUI
```
python3 scripts/gui/main.py
```

## Badger Bodger Device
The Badger Bodger itself is a Raspberry Pi with a small display and a 2D barcode scanner attached.

### Scanner Hardware
- Raspberry Pi 4 Model B – 4GB RAM
- 64GB MicroSD Card
- Hyperpixel 4.0 Touchscreen Display [UK](https://shop.pimoroni.com/products/hyperpixel-4?variant=12569485443155)
- [3D printed case](https://www.printables.com/model/121395-case-for-hyperpixel-40-with-raspberrypi-4)
- 2D Barcode Scanner [US](https://amzn.to/3ScbSAK) [UK](https://amzn.to/3Q9JGMd)
- USB-A to USB-C cable
- USB-C Power Supply (multi-region)

### Hardware Construction
The Hyperpixel 4.0 display comes with all the hardware you need to build the unit in combination with the 3D printed case. 

- Install the GPIO pin expansion header onto the Raspberry Pi
- Screw in the PCB standoffs to the back of the Hyperpixel 4.0
- Insert the Raspberry Pi into the 3D printed case (note, a bit of jiggling is required as it's snug fit)
- Connect the Hyperpixel 4.0 to the Raspberry Pi using the GPIO pins and push down gently
- Screw in the Hyperpixel 4.0 and Raspberry Pi to the 3D printed case using the screws provided

### Preparing the SD Card
Note that Raspbian Bookworm was released during the construction of the badge scanners, however it looked like it contained lots of changes to the desktop environment and how python operates that we haven't tested with it yet.  Therefore, when using Raspberry Pi Imager to flash the SD card, used the "Raspberry PI OS (Legacy)" opetion which is located under the "Raspberry Pi OS (other)" section.

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

Then eject the SD card from your laptop, insert it into the Raspberry Pi and boot.  Provided the Raspberry Pi has internet connectivity, within a few minutes the desktop will be displayed and then a few minutes after than the badge scanner GUI will be displayed.
