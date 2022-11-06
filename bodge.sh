#!/bin/bash
# Generate content 
rm -rf generated
mkdir -p generated

# Get first argument
if [ -z "$1" ]
then
    echo "No GitHub handle supplied, skipping data collection."
    cp images/info_link.bin generated/gh_qrcode.bin
else
    echo "Preloading Badger with custom data for $1"
    python3 scripts/getdata.py --handle $1
fi

# Convert any png images in the /images folder
echo "Converting images"
mkdir -p generated/images

for f in images/*.png; do
    echo "Converting $f"
    python3 scripts/convert.py --binary --resize --out_dir generated/images $f
done

# Copy the content of the /generated folder to the root of the attached device.
echo "Copying generated content"
ampy --port /dev/cu.usbmodem* put generated /

# Copy the content of the /preload folder to the root of the attached device.
echo "Copying preload content"
ampy --port /dev/cu.usbmodem* put preload /

# Reboot the board
ampy --port /dev/cu.usbmodem* reset --hard

