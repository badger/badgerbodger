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

    def __init__(self, parent, on_request_update, on_request_nuke, on_request_mona):
        tk.Frame.__init__(self,parent)
        self.config(width=480, height=800, padx=32, pady=32, background='black')
        self.on_request_update = on_request_update
        self.on_request_nuke = on_request_nuke
        self.on_request_mona = on_request_mona

        self.close_img = ImageTk.PhotoImage(Image.open(os.path.join(script_dir,f'images/close.png')))
        self.close_btn = tk.Button(self, text="", image=self.close_img, command=self.close)
        self.close_btn.pack(anchor='ne')

        self.internet_connection = tk.StringVar(self, "Internet: Checking")

        label_ip = tk.Label(self, text=f'IP Address:  {self.get_ip()}', anchor='w', background='black')
        label_ip.pack(fill="x")

        label_internet = tk.Label(self, textvariable=self.internet_connection, anchor='w', background='black')
        label_internet.pack(fill='x')

        buttons_frame = tk.Frame(self, padx=60, pady=60, background='black')

        btn_nuke = tk.Button(buttons_frame, 
                             text="Nuke Badge", 
                             command=self.nuke,
                             height=3
                             )
        btn_nuke.pack(fill='x', pady=16)

        btn_mona = tk.Button(buttons_frame, 
                             text="Burn Mona Badge", 
                             command=self.mona,
                             height=3
                             )
        btn_mona.pack(fill='x', pady=16)

        btn_update = tk.Button(buttons_frame,
                               text="Update Software",
                               command=self.update,
                               height=3
                                )
        btn_update.pack(fill='x', pady=16)

        btn_reboot = tk.Button(buttons_frame, 
                               text="Reboot",
                               command=self.reboot, 
                               height=3
                               )
        btn_reboot.pack(fill='x', pady=16)

        btn_shutdown = tk.Button(buttons_frame, 
                                 text="Shut Down",
                                 command=self.shutdown,
                                 height=3
                                 )
        btn_shutdown.pack(fill='x', pady=16)

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
            response = requests.get("https://github.com", timeout=5)
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