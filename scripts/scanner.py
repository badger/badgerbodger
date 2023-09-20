import tkinter as tk
from tkinter import ttk

# Create the app's main window
window = tk.Tk()
window.title("Scanner")

window_width = 500
window_height = 700

# get the screen dimension
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

window.resizable(False, False)
window.attributes('-topmost', 1)\

def handle_exit():
    window.destroy()

def handle_create(event):
    scanned = scantext.get()
    scantext.set("")
    print (scanned)

scantext = tk.StringVar()

scantext_entry = ttk.Entry(textvariable=scantext)
scantext_entry.pack(fill='x', expand=True, pady=10)
scantext_entry.focus()

create_button = ttk.Button(text="Create Badge", command=handle_create)
create_button.pack(fill='x', expand=True, pady=10)

exit_button = ttk.Button(text="  -----  Exit   -----  ", command=handle_exit)
exit_button.pack(fill='x', expand=True, pady=10)

window.bind('<Return>', handle_create)

# Start the event loop
window.mainloop()
