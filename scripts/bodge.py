
"""
Script to load the badge with the a generate badge.txt file. 

The data can be manually enterered in the scan_data array or 
scanned from the QR code on the badge.  unidecode is called
for the strings to get the latin characters that the badges
knows how to display (very lmited support for non-latin characters)

The badge file is then transferred to a device and the device is reset. 
"""
import subprocess
import os
import sys
from unidecode import unidecode

# Set the data to be loaded
scan_data = [
    "RegistrationId", 
    "Mona", # First name
    "Lisa", # Last name
    "GitHub", # Company
    "Octocat", # Job Title
    "she/her", # Pronouns 
    "@mona", # GitHub username 
    ]

# Scanned test from the QR Code on the badge
# This will override the scan_data above if it is set
scanned = ""

script_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

def main():
    
    if not _call_mpremote(['ls']):
        print("device not found, try resetting the badge and try again")
        sys.exit(1)

    print('- - - Loading badge - - -')

    first_name = unidecode(scan_data[1])
    last_name = unidecode(scan_data[2])
    company = unidecode(scan_data[3])
    handle = unidecode(scan_data[6])

    # By default convert to uppercase to match printed badges
    title = unidecode(scan_data[4].upper())
    pronouns = unidecode(scan_data[5].upper())

    # Depending on keyboard mapping, the @ symbol as the first character 
    if handle[0] == '"':
        handle = "@" + unidecode(handle[1:])
    elif handle[0] != "@":
        handle = "@" + unidecode(handle)

    print('Copy preload content')
    _transfer_folder(os.path.join(root_path,"preload"))

    # Create a file called generated/badges/badge.txt for writing.
    # Write "Universe 2023", first_name, lastname_name, company, title, pronouns, handle to the file on separate lines.
    badge_filename = os.path.join(root_path,"generated/badges/badge.txt")
    os.makedirs(os.path.dirname(badge_filename), exist_ok=True)
    with open(badge_filename, "w") as badge_file:
        print(f'Writing {badge_filename}')
        print(
            f"Universe 2023\n{first_name}\n{last_name}\n{company}\n{title}\n{pronouns}\n{handle}\n")
        badge_file.write(
            f"Universe 2023\n{first_name}\n{last_name}\n{company}\n{title}\n{pronouns}\n{handle}\n")
        badge_file.close()

    print('Copy generated content')
    _transfer_folder(os.path.join(root_path,"generated"))

    # Reboot the badge
    print("Resetting")
    _call_mpremote(['reset'])
    print("Done")

def _transfer_folder(root):
    # Iterate over the files in a given folder
    for subdir, dirs, files in os.walk(root):
        for file in files:
            localpath = os.path.join(subdir, file)
            remotepath = ":" + os.path.join(subdir, file).removeprefix(root)
            _call_mpremote(['cp', localpath, remotepath])

def _call_mpremote(args):
    args.insert(0, 'mpremote')
    proc = subprocess.run(args, capture_output=False, text=True)
    return proc.returncode == 0

# Basic latin set & the Spanish keyboard input of set with US keyboard layout
# This is because a Spanish keyboard reading the UTF-8 encoded QR code will
# do a slightly better job of passing through non-accented versions of the characters
# than a US keyboard reading the UTF-8 encoded QR code which will just ignore them.
latin  = " !\"$%&'()*+,-./0123456789<=>?ABCDEFGHIJKLMNOPQRSTUVWXYZ^_`abcdefghijklmnopqrstuvwxyzc@"
spanish = " !@$%^-*(}],/.&0123456789<)>_ABCDEFGHIJKLMNOPQRSTUVWXYZ{?[abcdefghijklmnopqrstuvwxyz#²"

def _decode_scanned_data(scanned):
    # if the scanned text ends in "{" then it's been scanned with a barcode scanner 
    # set to Spanish (which works better for accented characters) so we need to decode it.

    # Otherwise we can just return the scanned
    if scanned[-1] != "{":
        return scanned

    # Loop through the scanned and replace each character with the corresponding character in the latin set
    decoded = ""
    for c in scanned:
        if c in spanish:
            decoded += latin[spanish.index(c)]

    return decoded

# If the scanned data is not null or is not empty, use that instead of the scan_data
if scanned and scanned.strip():
    scan_data = _decode_scanned_data(scanned).split("^")

if __name__ == '__main__':
    main()