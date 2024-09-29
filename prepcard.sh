#!/bin/bash
# This script prepares the SD Card to use the Hyperpixel display
# and installs the badgerbodger software onto the Raspberry Pi on first boot.

# Remove the last 3 lines from /Volumes/bootfs/firstrun.sh
lines=$(wc -l /Volumes/bootfs/firstrun.sh | awk '{print $1}')
head -n $((lines-3)) /Volumes/bootfs/firstrun.sh > /Volumes/bootfs/firstrun.tmp

# Add setup code to /Volumes/bootfs/firstrun.sh
cat << 'ENDINSERT' >> /Volumes/bootfs/firstrun.tmp
# Create the install.sh script to clone a git repo, then run firstrun.sh in it
mkdir -p /home/badger/.config/autostart
cat << EOF > /home/badger/install.sh
#!/bin/bash
sleep 30
git clone --branch prod https://github.com/badger/badgerbodger.git /home/badger/badgerbodger
chmod +x /home/badger/badgerbodger/firstrun.sh
/bin/bash /home/badger/badgerbodger/firstrun.sh
rm /home/badger/.config/autostart/install.desktop
# rm /home/badger/install.sh
exit 0
EOF

# Run the install.sh script on boot
cat << EOF > /home/badger/.config/autostart/install.desktop
[Desktop Entry]
Name=Install
Exec=/bin/bash /home/badger/install.sh
EOF
chown -R badger:badger /home/badger

rm -f /boot/firstrun.sh
sed -i 's| systemd.run.*||g' /boot/cmdline.txt
exit 0
ENDINSERT

# Swap the temp firstun with our modified one.
rm /Volumes/bootfs/firstrun.sh
mv /Volumes/bootfs/firstrun.tmp /Volumes/bootfs/firstrun.sh

# Add the Hyperpixel overlay to /Volumes/bootfs/config.txt
cat << 'ENDINSERT' >> /Volumes/bootfs/config.txt

# Hyperpixel 4.0
dtoverlay=vc4-kms-dpi-hyperpixel4

ENDINSERT

# Unmount the bootfs volume
diskutil unmount /Volumes/bootfs

