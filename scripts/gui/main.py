import tkinter as tk
from tkinter import ttk
from state_page import StatePage
from PIL import Image, ImageTk

import subprocess
from scanner import Scanner
from settings import SettingsMenu
import os
import time
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Basic latin set & the Spanish keyboard input of set with US keyboard layout
# This is because a Spanish keyboard reading the UTF-8 encoded QR code will
# do a slightly better job of passing through non-accented versions of the characters
# than a US keyboard reading the UTF-8 encoded QR code which will just ignore them.
latin  = " !\"$%&'()*+,-./0123456789<=:?ABCDEFGHIJKLMNOPQRSTUVWXYZ^_`abcdefghijklmnopqrstuvwxyzc@@"
spanish = " !@$%^-*(}],/.&0123456789<)>_ABCDEFGHIJKLMNOPQRSTUVWXYZ{?[abcdefghijklmnopqrstuvwxyz#²€"

# GUI for badge programmer

class BadgeProgrammerUI(tk.Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.current_state = "wait"
        self.badger_detected = False
        self.state_frame = tk.Frame(self.master)
        self.scanner_frame = tk.Frame(self.master, height=10)
        
        self.state_frame.pack(fill=tk.BOTH, expand=True)

        # self.check_for_update()

        self.set_state("disconnected")
        self.scanner = Scanner(self.scanner_frame, create_badge=self.create_badge)
        self.scanner.pack()
        
        self.settings_img = ImageTk.PhotoImage(Image.open(os.path.join(script_dir,f'images/settings.png')))
        
        # Set the button to be smaller than the image to get rid of the 
        # white border around the image.
        self.settings_btn = tk.Button(self.master, text="", 
                                      image=self.settings_img,
                                      command=self.toggle_settings,
                                      highlightthickness=0,
                                      bd=0,
                                      padx=0,pady=0,height=46,width=46)
        self.settings_btn.place(x=400,y=24)

        self.badge_detection_loop()
    
    #Show settings page
    def toggle_settings(self):
            self.settings_frame = SettingsMenu(self.master, 
                                               on_request_update=self.manual_update,
                                               on_request_nuke=self.nuke_badge,
                                               on_request_mona=self.mona_badge,
                                               badge_connected=self.badge_detected
                                               )
            self.settings_frame.place(x=0,y=0, width=480,height=800)
            self.settings_shown = True

    # Get pages for different states of the program
    def get_state_page(state): 
        return StatePage(state=state)

    def show_page(self, state):
            for widget in self.state_frame.winfo_children():
                widget.destroy()

            if state == "ready":
                self.scanner_frame.pack()
            else:
                self.scanner_frame.pack_forget()

            state_page = StatePage(self.state_frame, state)
            state_page.pack(fill=tk.BOTH, expand=True)
          
            self.master.update()

    def set_state(self, state):
        if(state == self.current_state): return
        self.current_state = state
        self.show_page(state=self.current_state)

    def badge_detection_loop(self):
            """
            Continuously checks for the presence of a badge using the 'mpremote ls' command.
            If a badge is detected, sets the state to 'ready'.
            If a badge is not detected, sets the state to 'disconnected'.
            """
            if self.current_state == 'rebooting':
                return
            
            detection = subprocess.run(['mpremote', 'ls'],capture_output=True, text=True)
            self.badge_detected = detection.returncode == 0

            if not self.badge_detected:
                self.set_state("disconnected")

            elif self.badge_detected and self.current_state != 'complete':
                self.set_state("ready")
                    
            self.badge_loop_scheduler =  self.after(1000, self.badge_detection_loop)
        
    def create_badge(self, scanned):
        self.after_cancel(self.badge_loop_scheduler)
        self.set_state("uploading")


        # Copy all the data to the badge
        print("Transferring")
        _transfer_folder(os.path.join(root_path,"preload"))

        print(scanned)
        scanned = _decode_scanned_data(scanned)
        # Barcode gives data in the format
        # 1687465756044001tUzB^Martin^Woodward^GitHub^VP, DevRel^He/him^@martinwoodward^
        # Where pronouns and handle are optional but still delimited.
        print(scanned)
        scan_data = scanned.split('^')
        print (len(scan_data))
        if len(scan_data) >= 7:
            # Got the scan data back in the format we expect
            reg_id = scan_data[0]
            first_name = scan_data[1]
            last_name = scan_data[2]
            company = scan_data[3]
            title = scan_data[4]
            pronouns = scan_data[5]
            handle = scan_data[6]

            # Depending on keyboard mapping, the @ symbol as the first character 
            # of the handle may have been entered as "
            # If so, replace it with @
            if handle and handle[0] == '"':
                handle = "@" + handle[1:]
            elif handle and handle[0] != "@":
                handle = "@" + handle

            # Create a file called generated/badges/badge.txt for writing.
            # Write "Universe 2024", first_name, lastname_name, company, title, pronouns, handle to the file on separate lines.
            badge_filename = os.path.join(root_path,"generated/badges/badge.txt")
            os.makedirs(os.path.dirname(badge_filename), exist_ok=True)
            with open(badge_filename, "w") as badge_file:
                badge_file.write(
                    f"Universe 2024\n{first_name}\n{last_name}\n{company}\n{title}\n{pronouns}\n{handle}\n")
                badge_file.close()

            _transfer_folder(os.path.join(root_path,"generated"))

        # Reboot the badge
        self.set_state("rebooting")
        print(_call_mpremote(['reset']))
        print("Resetting")
        # Wait 5 seconds for reboot
        time.sleep(5)
        self.set_state("complete")
        self.badge_detection_loop()
    
    def check_for_update(self, show_confirmation = False):
        self.set_state("update_checking")

        # Checking if update is available
        update_availability = subprocess.check_output(['sh',os.path.join(root_path,'update_check.sh')],cwd=root_path)
        print(update_availability.decode().strip())

        # If available, show updating state & perform git pull
        if update_availability.decode().strip() == "update_available":
            self.set_state("updating")
            update_process = subprocess.run(['git','pull','origin','--ff-only'],
                                             capture_output=True,
                                             text=True,
                                             cwd=root_path)

            # If git pull successful, restart the application
            if update_process.returncode == 0:
                os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
            else:
                # Pull failed, show output
                print(update_process.stdout) 
                print(update_process.stderr) 

        elif show_confirmation:
            print("Up to date")
            self.after_cancel(self.badge_loop_scheduler)
            self.set_state("up_to_date")
            self.after(3000, self.badge_detection_loop)

    def manual_update(self):
         self.check_for_update(show_confirmation=True)
    
    def nuke_badge(self):
        self.after_cancel(self.badge_loop_scheduler)
        self.set_state("wait")
        subprocess.run(['bash', os.path.join(root_path,'nuke.sh')])
        self.badge_detection_loop()

    def mona_badge(self):
        self.after_cancel(self.badge_loop_scheduler)
        
        self.set_state("uploading")

        _transfer_folder(os.path.join(root_path,"preload"))
        # Reboot the badge
        self.set_state("rebooting")
        print(_call_mpremote(['reset']))
        print("Resetting")
        # Wait 5 seconds for reboot
        time.sleep(5)
        self.set_state("complete")

        self.badge_detection_loop()

def _transfer_folder(root):
    # Iterate over the files in a given folder
    for subdir, dirs, files in os.walk(root):
        # create the directories on the badge if they do not exist
        for dir in dirs:
            _call_mpremote(['mkdir', dir])
        for file in files:
            localpath = os.path.join(subdir, file)
            remotepath = ":" + os.path.join(subdir, file).removeprefix(root)
            _call_mpremote(['cp', localpath, remotepath])

def _call_mpremote(args):
    args.insert(0, 'mpremote')
    # print(args)
    proc = subprocess.run(args, capture_output=True, text=True)
    return proc.returncode == 0

def _decode_scanned_data(scanned):
    # Check if the scanned text contains more than 3 { characters. 
    # If so, then it's been scanned with a barcode scanner set to Spanish
    # (which works better for accented characters) so we need to decode it.
    if scanned.count("{") < 3:
        return scanned

    # Loop through the scanned and replace each character with the corresponding character in the latin set
    decoded = ""
    for c in scanned:
        if c in spanish:
            decoded += latin[spanish.index(c)]

    return decoded

def main():
    window = tk.Tk()
    window.geometry("480x800")
    window.configure(bg='black')
    window.title("Scanner")

    # Check what OS we are running on and if it is not a Mac 
    # then set the window to fullscreen
    if sys.platform != 'darwin':
        window.attributes('-fullscreen', True)
        window.resizable(width=False,height=False)

    # Bind escape key to exit fullscreen
    window.bind("<Escape>",lambda event:window.attributes('-fullscreen', False))   

    BadgeProgrammerUI()
    window.mainloop()

def end_fullscreen(self, event=None):
    self.tk.attributes("-fullscreen", False)

if __name__ == '__main__':
    main()
