#!/bin/bash

# get first argument
if [ -z "$1" ]
then
    file="handles.txt"
else
    file=$1
fi

# get handles from file
cat $file | while read handle 
do
  echo "Press boot and reset button"
  afplay /System/Library/Sounds/Funk.aiff  
  # Wait for device to appear
  while [ ! -d /Volumes/RPI-RP2 ]; do sleep 1; done  
  sleep 1
  echo "Nuke device"
  cp uf2-images/flash_nuke.uf2 /Volumes/RPI-RP2
  sleep 1
  killall NotificationCenter

  # Wait for device to appear
  while [ ! -d /Volumes/RPI-RP2 ]; do sleep 1; done  
  sleep 1
  echo "Flash device with Badger image"
  cp uf2-images/github-badger2040-mona-micropython.uf2 /Volumes/RPI-RP2
  sleep 15
  killall NotificationCenter

  ./bodge.sh $handle
  echo "Done!"
done