#!/bin/bash

mpremote bootloader
sleep 5
cp uf2-images/pimoroni-*.uf2 /media/*/RPI-RP2
