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
        self.padx=43
        self.pady=20

        self.configure(width = self.width,
                       height = self.height,
                       border_width=0,)
        
        self.grid_propagate(False)


        self.optionmenu = ctk.CTkOptionMenu(master=self,
                                            values=Flipper_Back.chain_names(),
                                            command=self.optionmenu_callback)
        # print(self.optionmenu.bg_color)
        self.configure(fg_color=['#EBEBEC', '#212325'])

        self.optionmenu.pack(pady=self.pady, anchor='n')


    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)

    def get_value(self):
        print(self.optionmenu.get())

        return self.optionmenu.get()