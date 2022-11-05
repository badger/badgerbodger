#!/bin/bash
echo "Preloading Badger with custom data"

# Generate content 
mkdir -p generated

# Convert any png images in the /images folder
echo "Converting images"

for f in images/*.png; do
    echo "Converting $f"
    python3 scripts/convert.py --binary --resize --out_dir generated/images $f
done

# Copy the content of the /generated folder to the root of the attached device.
echo "Copying generated content"
ampy --port /dev/cu.usbmodem1401 put generated /

# Copy the content of the /preload folder to the root of the attached device.
echo "Copying preload content"
ampy --port /dev/cu.usbmodem1401 put preload /

# Reboot the board
ampy --port /dev/cu.usbmodem1401 reset --hard
