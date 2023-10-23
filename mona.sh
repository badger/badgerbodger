#!/bin/bash

mpremote bootloader
sleep 5
cp uf2-images/github-*.uf2 /media/*/RPI-RP2
