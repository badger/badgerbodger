#!/bin/bash

while true;
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
  sleep 14
  killall NotificationCenter

  echo "Wait for LED to be on then enter the GitHub handle:"
  afplay /System/Library/Sounds/Ping.aiff
  
  # get handle from keyboard
  read handle

  ./bodge.sh $handle
  echo "Done!"
  echo "Plug in a new badge to continue"
done
