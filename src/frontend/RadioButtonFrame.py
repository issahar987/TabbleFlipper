import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from backend import Flipper_Back
import socket

class RadioButtonFrame(ctk.CTkFrame):
    def __init__(self, *args, frame_height, ip_list=[], **kwargs):
        super().__init__(*args, **kwargs)
        
        self.ip_list = ip_list[0:12]
        self.configure(height = frame_height, width=200)

        self.radio_button_var = ctk.StringVar(value="")
        for count, item in enumerate(self.ip_list, start=1):
            self.radio_button_1 = ctk.CTkRadioButton(self, text=f"{item}", value=f"{count}", variable=self.radio_button_var)
            self.radio_button_1.grid(row=count, column=0, padx=10, pady=10, sticky="nw")
    def get_value(self):
        """ returns selected value as a string, returns an empty string if nothing selected """
        return self.radio_button_var.get()

    def set_value(self, selection):
        """ selects the corresponding radio button, selects nothing if no corresponding radio button """
        self.radio_button_var.set(selection)