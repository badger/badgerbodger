from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, StringVar
from tkinter.ttk import Frame, Label, Entry, Button
import os
import subprocess

class Scanner(Frame):

    def __init__(self, parent, create_badge):
        super().__init__(parent)
        self.create_badge = create_badge
        self.parent = parent
        self.initUI()

    def initUI(self):

        self.scantext = StringVar()

        self.scantext_entry = Entry(self.parent, textvariable=self.scantext, background='black',borderwidth=0,highlightthickness=0)
        self.scantext_entry.pack(fill='x',)
        self.scantext_entry.focus()
        self.scantext_entry.bind('<Return>', self.handle_create)

    def handle_create(self, event):
        scanned = self.scantext.get()
        self.scantext.set("")
        self.create_badge(scanned)
