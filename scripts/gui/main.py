import tkinter as tk
from tkinter import ttk
from state_page import StatePage

import subprocess
from scanner import Scanner


# GUI for badge programmer

class BadgeProgrammerUI(tk.Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.state_list = ["initializing","disconnected","ready","uploading","nuking","complete","error"]
        self.current_state = "initializing"
        self.state_pages = map(self.getStatePage, self.state_list)
        self.badger_detected = False
        self.state_frame = tk.Frame(self.master)
        self.state_frame.pack(fill=tk.BOTH, expand=True)
        self.setState("disconnected")
        self.badgeDetectionLoop()
        

    # Get pages for different states of the program
    def getStatePage(state): 
        return StatePage(state=state)

    def showPage(self, state):
            for widget in self.state_frame.winfo_children():
                widget.destroy()

            if state == "ready":
                frame = tk.Frame(self,height=10)
                scanner = Scanner(frame)
                scanner.pack()
                frame.place(x=0,y=0)
            state_page = StatePage(self.state_frame, state)
            state_page.pack(fill=tk.BOTH, expand=True)
          
            self.master.update()

    def setState(self, state):
        if(state == self.current_state): return
        self.current_state = state
        self.showPage(state=self.current_state)


    # Check if badge is connected 
    def badgeDetectionLoop(self):
        detection = subprocess.run(['mpremote', 'ls'])
        badger_detected = detection.returncode == 0
        if badger_detected:
            self.setState("ready")
        else: 
            self.setState("disconnected")
        self.after(1000, self.badgeDetectionLoop)

    
def main():
    window = tk.Tk()
    window.geometry("480x800")
    window.configure(bg='black')
    window.resizable(width=False,height=False)    
    BadgeProgrammerUI()
    window.mainloop()

if __name__ == '__main__':
    main()
