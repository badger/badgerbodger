#!/bin/bash

# Run from the root of the project
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

echo "$parent_path"

mpremote bootloader
sleep 5
cp uf2-images/pimoroni-*.uf2 /media/badger/RP2350
