from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, StringVar
from tkinter.ttk import Frame, Label, Entry, Button
import os
import subprocess

# Mostly reused scripts/scanner.py, pending modifications

class Scanner(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):

        self.scantext = StringVar()

        scantext_entry = Entry(textvariable=self.scantext)
        scantext_entry.pack(fill='x',)
        scantext_entry.focus()
        scantext_entry.bind('<Return>', self.handle_create)

    def handle_create(self, event):
        scanned = self.scantext.get()
        self.scantext.set("")
        self.create_badge(scanned)

    def handle_exit(self):
        self.quit()

    def create_badge(self, scanned):
        print(scanned)
        scan_data = scanned.split('^')
        reg_id = scan_data[0]
        first_name = scan_data[1]
        last_name = scan_data[2]
        company = scan_data[3]
        # By default convert to uppercase to match printed badges
        title = scan_data[4].upper()
        # A hacker can always change the case late if they want
        pronouns = scan_data[5].upper()

        # Create a file called generated/badges/badge.txt for writing.
        # Write "Universe 2023", first_name, lastname_name, company, title, pronouns to the file on separate lines.
        badge_filename = "generated/badges/badge.txt"
        os.makedirs(os.path.dirname(badge_filename), exist_ok=True)
        with open(badge_filename, "w") as badge_file:
            badge_file.write(
                f"Universe 2023\n{first_name}\n{last_name}\n{company}\n{title}\n{pronouns}")
            badge_file.close()

        # Copy all the data to the badge
        _transfer_folder("preload")
        _transfer_folder("generated")

        # Reboot the badge
        _call_mpremote(['reset'])


def _transfer_folder(root):
    # Iterate over the files in a given folder
    for subdir, dirs, files in os.walk(root):
        for file in files:
            localpath = os.path.join(subdir, file)
            remotepath = ":" + os.path.join(subdir, file).removeprefix(root)
            _call_mpremote(['cp', localpath, remotepath])


def _call_mpremote(args):
    args.insert(0, 'mpremote')
    proc = subprocess.run(args, capture_output=True, text=True)
    print(proc.stdout)
    print(proc.stderr)
