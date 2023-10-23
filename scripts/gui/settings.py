import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import socket
import requests
import subprocess

class SettingsMenu(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        self.config(width=480, height=800, padx=32, pady=32)

        self.internet_connection = tk.StringVar(self, "Internet: Checking")

        label_ip = tk.Label(self, text=f'IP Address:  {self.get_ip()}', anchor='w')
        label_ip.pack(fill="x")

        label_internet = tk.Label(self, textvariable=self.internet_connection, anchor='w')
        label_internet.pack(fill='x')

        buttons_frame = tk.Frame(self, padx=60, pady=60)

        btn_nuke = tk.Button(buttons_frame, 
                             text="Nuke Badge", 
                             command=lambda nuke: subprocess.run(['sh','nuke.sh'])
                             )
        btn_nuke.pack()

        btn_update = tk.Button(buttons_frame,
                               text="Update Software",
                               command=lambda nuke: subprocess.run(['sh','update_check.sh'])
                                )
        btn_update.pack()

        btn_reboot = tk.Button(buttons_frame, 
                               text="Reboot",
                               command=lambda nuke: subprocess.run(['reboot'])
                               )
        btn_reboot.pack()

        btn_shutdown = tk.Button(buttons_frame, 
                                 text="Shut Down",
                                 command=lambda nuke: subprocess.run(['poweroff'])
                                 )
        btn_shutdown.pack()

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

    def btnPress():
        print("Hello")