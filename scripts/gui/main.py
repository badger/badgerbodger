import tkinter as tk
from tkinter import ttk
from state_page import StatePage

import subprocess
from scanner import Scanner
import os

# GUI for badge programmer

class BadgeProgrammerUI(tk.Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.state_list = ["initializing","disconnected","ready","uploading","nuking","complete","error"]
        self.current_state = "initializing"
        self.state_pages = map(self.get_state_page, self.state_list)
        self.badger_detected = False
        self.state_frame = tk.Frame(self.master)
        self.scanner_frame = tk.Frame(self, height=10)
        
        self.state_frame.pack(fill=tk.BOTH, expand=True)
        self.set_state("disconnected")
        self.badge_detection_interval = 1000
        self.badge_detection_loop()

    # Get pages for different states of the program
    def get_state_page(state): 
        return StatePage(state=state)

    def show_page(self, state):
            for widget in self.state_frame.winfo_children():
                widget.destroy()

            if state == "ready":
                Scanner(self.scanner_frame, create_badge=self.create_badge).pack()

            state_page = StatePage(self.state_frame, state)
            state_page.pack(fill=tk.BOTH, expand=True)
          
            self.master.update()

    def set_state(self, state):
        if(state == self.current_state): return
        self.current_state = state
        self.show_page(state=self.current_state)


    # Check if badge is connected 
    def badge_detection_loop(self):
        detection = subprocess.run(['mpremote', 'ls'])
        badger_detected = detection.returncode == 0

        if badger_detected:
            if self.badge_complete_check():
                self.set_state("complete")
            else:
                self.set_state("ready")
        
        else: 
            self.set_state("disconnected")
            self.badge_detection_interval = 1000

        self.after(self.badge_detection_interval, self.badge_detection_loop)

    def badge_complete_check(self):
        # Checking locally the contents of the last generated badge
        last_badge_path = 'generated/badges/badge.txt'
        if(os.path.exists(last_badge_path)):
                with open(last_badge_path) as f:
                    last_badge_contents = f.read()

                    # Checking remote badge.txt
                    remote_badge = subprocess.run(['mpremote','cat','badges/badge.txt'], capture_output=True, text=True)
                    if remote_badge.returncode == 0 and last_badge_contents == remote_badge.stdout:
                        # Same badge
                        return True
                    
        #Not the same badge
        return False
        

    def create_badge(self, scanned):
        self.set_state("uploading")
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
        self.set_state("complete")
        self.badge_detection_interval = 5000
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


    
def main():
    window = tk.Tk()
    window.geometry("480x800")
    window.configure(bg='black')
    window.resizable(width=False,height=False)    
    BadgeProgrammerUI()
    window.mainloop()

if __name__ == '__main__':
    main()
