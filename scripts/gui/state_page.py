import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import os.path


script_dir = os.path.dirname(os.path.abspath(__file__))

class StatePage(tk.Frame):
    def __init__(self, parent, state):
        tk.Frame.__init__(self, parent)
        imgTk = ImageTk.PhotoImage(Image.open(os.path.join(script_dir,f'images/{state}.png')).resize((480,800)))
        imgLabel = tk.Label(self,image=imgTk,borderwidth=0,highlightthickness=0)
        imgLabel.image = imgTk
        imgLabel.place(x=0,y=0)
