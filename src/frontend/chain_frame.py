import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from backend import Flipper_Back
from pathlib import Path
import os
import json


class ChainFrame(ctk.CTkFrame):
    def __init__(self, width, height, button_width, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width=width
        self.height=height

        self.configure(width = self.width,
                       height = self.height,
                       border_width=0,)
        
        self.grid_propagate(False)