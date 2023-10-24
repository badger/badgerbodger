#!/bin/bash

# Run from the root of the project
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# Set up paths so that mpremote will work
mkdir -p /home/badger/.local/bin
echo "export PATH=\$PATH:~/.local/bin" >> /home/badger/.bashrc
export PATH=$PATH:~/.local/bin

# Install python dependencies
pip3 install --upgrade pip
pip3 install -r scripts/requirements.txt

# Set screensaver to not run
export DISPLAY=:0;xset s noblank; xset s off; xset -dpms
# Set screensaver to not run on boot
mkdir -p /home/badger/.config/lxsession/LXDE-pi
cat << EOF > /home/badger/.config/lxsession/LXDE-pi/autostart
@xpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@xset -dpms
@xset s off
EOF

# Set scanner to run on boot
mkdir -p /home/badger/.config/autostart
cat << EOF > /home/badger/.config/autostart/scanner.desktop
[Desktop Entry]
Name=Scanner
Exec=/usr/bin/python3 /home/badger/badgerbodger/scripts/gui/main.py
EOF

# Disable USB autorun dialog
mkdir -p /home/badger/.config/pcmanfm/LXDE-pi
cat << EOF > /home/badger/.config/pcmanfm/LXDE-pi/pcmanfm.conf
[config]
bm_open_method=0

[volume]
mount_on_startup=1
mount_removable=1
autorun=0
EOF

# First run of scanner
/usr/bin/python3 /home/badger/badgerbodger/scripts/gui/main.py

