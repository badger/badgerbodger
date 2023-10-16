from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, StringVar
from tkinter.ttk import Frame, Label, Entry, Button
import os
import subprocess

# Mostly reused scripts/scanner.py, pending modifications

class Scanner(Frame):

    def __init__(self, parent, create_badge):
        super().__init__(parent)
        self.create_badge = create_badge

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
        
