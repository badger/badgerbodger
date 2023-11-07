import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import socket
import requests
import subprocess
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

class SettingsMenu(tk.Frame):

    def __init__(self, parent, on_request_update, on_request_nuke, on_request_mona, badge_connected):
        tk.Frame.__init__(self,parent)
        self.config(width=480, height=800, padx=24, pady=24, background='black')
        self.on_request_update = on_request_update
        self.on_request_nuke = on_request_nuke
        self.on_request_mona = on_request_mona

        self.close_img = ImageTk.PhotoImage(Image.open(os.path.join(script_dir,f'images/close.png')))
        self.close_btn = tk.Button(self, text="", 
                                   image=self.close_img, 
                                   command=self.close,
                                   highlightthickness=0,
                                   bd=0,
                                   padx=0,pady=0,height=46,width=46)
        self.close_btn.place(x=376,y=0)

        self.internet_connection = tk.StringVar(self, "Internet: Checking")

        label_ip = tk.Label(self, text=f'IP Address:  {self.get_ip()}', anchor='w', background='black', foreground='white',  font=('TkDefaultFont', 18) )
        label_ip.pack(fill="x")

        label_internet = tk.Label(self, textvariable=self.internet_connection, anchor='w', background='black', foreground='white',  font=('TkDefaultFont', 18))
        label_internet.pack(fill='x')

        badge_label_text = "Badge: Disconnected"
        if badge_connected:
            badge_label_text = "Badge: Connected"

        label_badge = tk.Label(self, text=badge_label_text, anchor='w', background='black', foreground='white',  font=('TkDefaultFont', 18))
        label_badge.pack(fill='x')


        label_commit_id = tk.Label(self, text=f'Version: {self.get_commit_id()}', anchor='w', background='black', foreground='white', font=('TkDefaultFont',18))
        label_commit_id.pack(fill='x')

        self.close_btn.lift()

        buttons_frame = tk.Frame(self, padx=60, pady=24, background='black')
        
        if(badge_connected):
            button_state = 'normal'
        else:
            button_state = 'disabled'
        
        btn_update = tk.Button(buttons_frame,
                               text="Update Software",
                               command=self.update,
                               height=3,
                               font=('TkDefaultFont', 18)
                                )
        btn_update.pack(fill='x', pady=8)

        btn_mona = tk.Button(buttons_frame, 
                             text="Burn Mona Badge", 
                             command=self.mona,
                             height=3,
                             state=button_state,
                             font=('TkDefaultFont', 18)
                             )
        btn_mona.pack(fill='x', pady=8)

        btn_nuke = tk.Button(buttons_frame, 
                             text="Nuke Badge", 
                             command=self.nuke,
                             height=3,
                             state=button_state,
                             font=('TkDefaultFont', 18)
                             )
        btn_nuke.pack(fill='x', pady=8)

        btn_reboot = tk.Button(buttons_frame, 
                               text="Reboot",
                               command=self.reboot, 
                               height=3,
                               font=('TkDefaultFont', 18)
                               )
        btn_reboot.pack(fill='x', pady=8)

        btn_shutdown = tk.Button(buttons_frame, 
                                 text="Shut Down",
                                 command=self.shutdown,
                                 height=3,
                                 font=('TkDefaultFont', 18)
                                 )
        btn_shutdown.pack(fill='x', pady=8)

        buttons_frame.pack(fill='both')

        self.check_internet_connection()

    
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    
    def check_internet_connection(self):
        try:
            response = requests.get("https://api.github.com/status", timeout=5)
            self.internet_connection.set("Internet: Connected")

        except requests.ConnectionError:
            self.internet_connection.set("Internet: Disconnected")

    def shutdown(self):
        subprocess.run(['poweroff'])
    
    def reboot(self):
        subprocess.run(['reboot'])

    def nuke(self):
        self.place_forget()
        self.on_request_nuke()

    def mona(self):
        self.place_forget()
        self.on_request_mona()

    def update(self):
        self.place_forget()
        self.on_request_update()

    def close(self):
        self.destroy()

    def get_commit_id(self):
      commit_id = subprocess.run(['git','rev-parse','--short', 'HEAD'], capture_output=True, text=True)
      branch_name = subprocess.run(['git','branch','--show-current'], capture_output=True, text=True)
      return f'{commit_id.stdout.strip()} ({branch_name.stdout.strip()})'