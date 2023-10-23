import tkinter as tk
from tkinter import ttk
from state_page import StatePage
from state_page import script_dir
from PIL import Image, ImageTk

import subprocess
from scanner import Scanner
from settings import SettingsMenu
import os
import time
import sys

# GUI for badge programmer

class BadgeProgrammerUI(tk.Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.state_list = ["initializing","disconnected","ready","uploading","nuking","complete","error", "rebooting"]
        self.current_state = "initializing"
        self.state_pages = map(self.get_state_page, self.state_list)
        self.badger_detected = False
        self.state_frame = tk.Frame(self.master)
        self.scanner_frame = tk.Frame(self.master, height=10)
        
        self.state_frame.pack(fill=tk.BOTH, expand=True)

        # self.check_for_update()

        self.set_state("disconnected")
        self.detection_loop_on = True
        self.scanner = Scanner(self.scanner_frame, create_badge=self.create_badge)
        self.scanner.pack()
        
        self.settings_shown = False
        self.settings_img = ImageTk.PhotoImage(Image.open(os.path.join(script_dir,f'images/github-mark-white.png')))
        self.settings_btn = tk.Button(self.master, text="", image=self.settings_img, borderwidth=0, highlightthickness=0, padx=0, pady=0, bd=0, command=self.toggle_settings)
        self.settings_btn.place(x=416,y=16)

        

        self.badge_detection_loop()

    
    #Show settings page
    def toggle_settings(self):
        if self.settings_shown:
            self.settings_frame.destroy()
            self.settings_shown = False
        else:
           # self.settings_btn.place_forget()
            self.settings_frame = SettingsMenu(self.master)
            self.settings_frame.place(x=0,y=0, width=480,height=800)
            self.settings_btn.lift()
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


    # Check if badge is connected 
    def badge_detection_loop(self):
        if self.current_state == 'rebooting':
            return
        
        detection = subprocess.run(['mpremote', 'ls'])
        badger_detected = detection.returncode == 0

        if not badger_detected:
            self.set_state("disconnected")

        elif badger_detected and self.current_state != 'complete':
            self.set_state("ready")
            
        if self.detection_loop_on:
            self.update()
            self.after(1000, self.badge_detection_loop)
       
        
    def create_badge(self, scanned):
        self.detection_loop_on = False
        self.set_state("uploading")
        print(scanned)
        # Barcode gives data in the format
        # 1687465756044001tUzB^Martin^Woodward^GitHub^VP, DevRel^He/him^@martinwoodward^
        # Where pronouns and handle are optional but still delimited.
        scan_data = scanned.split('^')
        reg_id = scan_data[0]
        first_name = scan_data[1]
        last_name = scan_data[2]
        company = scan_data[3]
        handle = scan_data[6]

        # By default convert to uppercase to match printed badges
        # A hacker can always change the case later if they want
        title = scan_data[4].upper()
        pronouns = scan_data[5].upper()

        # Depending on keyboard mapping, the @ symbol as the first character 
        # of the handle may have been entered as "
        # If so, replace it with @
        if handle[0] == '"':
            handle = "@" + handle[1:]

        # get root directory of the project
        root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))

        # Create a file called generated/badges/badge.txt for writing.
        # Write "Universe 2023", first_name, lastname_name, company, title, pronouns, handle to the file on separate lines.
        badge_filename = os.path.join(root_path,"generated/badges/badge.txt")
        os.makedirs(os.path.dirname(badge_filename), exist_ok=True)
        with open(badge_filename, "w") as badge_file:
            badge_file.write(
                f"Universe 2023\n{first_name}\n{last_name}\n{company}\n{title}\n{pronouns}\n{handle}\n")
            badge_file.close()

        # Copy all the data to the badge
        print("Transferring")
        _transfer_folder(os.path.join(root_path,"preload"))
        _transfer_folder(os.path.join(root_path,"generated"))

        # Reboot the badge
        self.set_state("rebooting")
        print(_call_mpremote(['reset']))
        print("Resetting")
        # Wait 6 seconds for reboot
        time.sleep(6)
        self.detection_loop_on = True
        self.set_state("complete")
        self.badge_detection_loop()
    
    def check_for_update(self):
        self.set_state("update_checking")

        # Checking if update is available
        update_availability = subprocess.check_output(['sh','update_check.sh'])
        print(update_availability.decode().strip())

        # If available, show updating state & perform git pull
        if update_availability.decode().strip() == "update_available":
            self.set_state("updating")
            update_process = subprocess.run(['git','pull'], capture_output=True, text=True)

            # If git pull successful, restart the application
            if update_process.returncode == 0:
                os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
            else:
                print(update_process.stdout) #Pull failed
            

        


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
    # Debug - print mpremote calls.
    #print(proc.stdout)
    #print(proc.stderr)
    return proc.returncode == 0


    
def main():
    window = tk.Tk()
    window.geometry("480x800")
    window.configure(bg='black')
    #window.attributes('-fullscreen', True)
    window.resizable(width=False,height=False)
    window.bind("<Escape>",lambda event:window.attributes('-fullscreen', False))    
    BadgeProgrammerUI()
    window.mainloop()

def end_fullscreen(self, event=None):
    self.tk.attributes("-fullscreen", False)

if __name__ == '__main__':
    main()