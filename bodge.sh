#!/bin/bash
# Get first argument
if [ -z "$1" ]
then
    echo "No GitHub handle supplied, re-run as 'bodge.sh <github_handle>'"
    exit 1
fi

echo "Preloading Badger with custom data for $1"

# Generate content 
rm -rf generated
mkdir -p generated

python3 scripts/getdata.py --handle $1

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
