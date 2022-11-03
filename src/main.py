import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from backend import Flipper_Back
from frontend import App
import socket


if __name__ == "__main__":
    #  create a window first
    # define window dimensions width and height
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800
    Flipper_Back.EnterSudo("kali")
    app = App.App(WINDOW_WIDTH, WINDOW_HEIGHT)
    # *get the screen size of your computer
    # *[width and height using the root object as foolows]
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    # Get the window position from the top dynamically
    # as well as position from left or right as follows
    position_top = int(screen_height / 2 - WINDOW_HEIGHT / 2)
    position_right = int(screen_width / 2 - WINDOW_WIDTH / 2)
    # this is the line that will center your window
    app.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{position_right}+{position_top}')
    # lock window to not be resizable
    app.resizable(False, False)
    # initialise the window
    app.mainloop(0)
