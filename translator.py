import tkinter as tk    # required to make application
import os               # os.path allows to construct a cross-platform path

####### Establishing paths

script_dir = os.path.dirname(os.path.abspath(__file__))             # gets absolute path of this file, then gets direcory
icon_path = os.path.join(script_dir, "resources", "icon.ico")       # Icon in the same folder

####### Creating application

root = tk.Tk()          # Tk() is the constructor for the top-level window
root.iconbitmap(icon_path)



root.mainloop()         # the event loop is required to keep the window open, otherwise it would instanteneouslyclose