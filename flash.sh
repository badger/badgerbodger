#!/bin/bash

while true
do
  # Wait for keypress
  echo "Press key after Badge in Flash mode to nuke"
  read -n 1 -s

  cp uf2-images/flash_nuke.uf2 /Volumes/RPI-RP2

  echo "Wait for 2 flashes then press to flash"
  read -n 1 -s
  cp uf2-images/github-badger2040-mona-micropython.uf2 /Volumes/RPI-RP2

  echo "Wait for LED on then enter the GitHub handle:"
  read handle
  ./bodge.sh $handle

  echo "Done!"
done


