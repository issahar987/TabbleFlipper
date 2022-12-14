import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from backend import Flipper_Back, general
from pathlib import Path
import os
import json

class RadioButtonFrame(ctk.CTkFrame):
    def __init__(self, *args, frame_height, ip_list=[], chain, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.ip_list = ip_list[0:12]
        self.configure(height=frame_height, width=400)
        self.dns_dict = {}
        self.configure(fg_color=['#EBEBEC', '#212325'])  # sets widget color to black
        self.path = Path("src/frontend").parent.parent.absolute()
        self.filename = f'{self.path}/INPUT_dns.json'
        self.chain = chain
        self.index = 0

        general.check_dns_json(self.filename)
        if os.stat(self.filename).st_size != 0:
            with open (self.filename, 'r') as f:
                data = json.load(f)
            print(data)

            for item in data:
                if data[item] not in self.dns_dict:
                    self.dns_dict[data[item]] = [item]
                else:
                    self.dns_dict[data[item]].append(item)
        
        print(f'this is dns dict {self.dns_dict}')

        print(f'This is ip_list: {self.ip_list}')

        self.radio_button_var = ctk.StringVar(value="")
        for count, item in enumerate(self.ip_list, start=1):
            self.index += len(self.dns_dict[item])
            self.radio_button = ctk.CTkRadioButton(self, text=f"{item}", value=f"{self.index} {item}", variable=self.radio_button_var)
            self.radio_button.grid(row=count, column=0, padx=10, pady=10, sticky="nw")
    def get_value(self):
        """ returns selected value as a string, returns an empty string if nothing selected """
        return self.radio_button_var.get()
    

    def get_dns_dict(self):
        return self.dns_dict
    
    def get_chain(self):
        return self.chain

    def set_value(self, selection):
        """ selects the corresponding radio button, selects nothing if no corresponding radio button """
        self.radio_button_var.set(selection)