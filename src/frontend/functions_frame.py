import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from backend import Flipper_Back
from pathlib import Path
import os
import json


class FunctionsFrame(ctk.CTkFrame):
    def __init__(self, width, height, button_width, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width=width
        self.height=height
        self.button_width=button_width
        self.padx=43
        self.pady=20

        self.configure(width = self.width,
                       height = self.height,
                       border_width=0,)
        
        self.button_refresh = ctk.CTkButton(master=self,
                                            width=self.button_width,
                                            text="Refresh",
                                            command=self.refresh)
        self.button_clear = ctk.CTkButton(master=self,
                                          width=self.button_width,
                                          text="Clear all",
                                          command=self.clear_iptables)
        self.button_clear_one = ctk.CTkButton(master=self,
                                              width=self.button_width,
                                              text="Clear selection",
                                              command=self.clear_one)

        

        self.button_refresh.grid(column=0, row=0, padx=1 * self.padx, pady=self.pady, sticky='w')
        self.button_clear_one.grid(column=1, row=0, padx=1 * self.padx, pady=self.pady)
        self.button_clear.grid(column=2, row=0, padx=1 * self.padx, pady=self.pady, sticky='e')
    
    def submit(self):
        print(f"IP: {self.entry.get()}")
        Flipper_Back.AddRule("INPUT", "-s", self.entry.get(), "DROP")
        self.clear()
        self.refresh()

    def clear(self):
        self.entry.delete(0, 'end')

    def import_(self):
        Flipper_Back.imortChain('EXPORT.txt')
        self.refresh()
        print("importing")

    def export(self):
        print("exporting")
        Flipper_Back.exportChain("INPUT")
    
    def refresh(self):
        # IP_tables = Flipper_Back.ShowChain("INPUT").split("\n")
        
        IP_tables = Flipper_Back.ShowRules().split("\n")
        IP_list = []
        del IP_tables[0:3]  # delete first three IPtables string
        del IP_tables[-1] # delete empty string at the end
        for item in IP_tables:
            item = item.split(' ')
            del item[0:3]  # delete flags
            del item[1:3]  # delete -j and DROP
            item = item[0][:-3]  # delete netmask /32
            IP_list.append(item)
        print(IP_list)

        self.radio_button_frame = RBF.RadioButtonFrame(self.frame_bottom_right,
                                                       frame_height=self.frame_bottom_right["height"],
                                                       ip_list=[])
        # self.radio_button_frame.configure(fg_color=self.frame_bottom_right.fg_color)
        self.radio_button_frame.grid(row=0, column=0, sticky="nw")

        self.radio_button_frame = RBF.RadioButtonFrame(self.frame_bottom_right,
                                                       frame_height=self.frame_bottom_right["height"],
                                                       ip_list=IP_list)
        # self.radio_button_frame.configure(fg_color=self.frame_bottom_right.fg_color)
        self.radio_button_frame.grid(row=0, column=0, sticky="nw")

        # create CTk scrollbar
        # self.scrollbar = ctk.CTkScrollbar(self)
        # self.scrollbar.grid(row=0, column=1, sticky="ns")

        # connect frame scroll event to CTk scrollbar
        # self.radio_button_frame.configure(yscrollcommand=self.scrollbar.set)
    
    def clear_one(self):
        selected_value = self.radio_button_frame.get_value()
        print(selected_value)
        Flipper_Back.deleteRule("INPUT", selected_value)
        self.refresh()
    def input_dns_json(self):
        path = Path("src/frontend").parent.parent.absolute()

        if os.stat(f'{path}/INPUT_dns.json').st_size != 0:
            with open (f'{path}/INPUT_dns.json', 'w') as f:
                data = json.load(f)
            print(data)
    def clear_iptables(self):
        Flipper_Back.ClearAll()
        self.refresh()
        self.input_dns_json()