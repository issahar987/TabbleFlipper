import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from backend import Flipper_Back, general
from frontend import RadioButtonFrame as RBF
from pathlib import Path
import os
import json
import socket



class FunctionsFrame(ctk.CTkFrame):
    def __init__(self, width, height, button_width, ip_list_frame, chain_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width=width
        self.height=height
        self.button_width=button_width
        self.padx=43
        self.pady=20
        self.ip_list_frame=ip_list_frame
        self.chain_frame=chain_frame
        self.chain=self.chain_frame.get_value()

        self.configure(width = self.width,
                       height = self.height,
                       border_width=0,)
        # self.configure(fg_color=['#EBEBEC', '#212325'])  # sets widget color to black
        self.grid_propagate(False)

        print(ip_list_frame)
        
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
    
    def refresh(self):
        # IP_tables = Flipper_Back.ShowChain("INPUT").split("\n")
        self.chain=self.chain_frame.get_value()
        IP_list = general.ip_to_dns(self.chain)

        self.radio_button_frame = RBF.RadioButtonFrame(self.ip_list_frame,
                                                       frame_height=self.ip_list_frame["height"],
                                                       ip_list=[],
                                                       chain=self.chain)
        # self.radio_button_frame.configure(fg_color=self.frame_bottom_right.fg_color)
        self.radio_button_frame.grid(row=0, column=0, padx=4 * self.padx, sticky="nw")

        self.radio_button_frame = RBF.RadioButtonFrame(self.ip_list_frame,
                                                       frame_height=self.ip_list_frame["height"],
                                                       ip_list=IP_list,
                                                       chain=self.chain)
        # self.radio_button_frame.configure(fg_color=self.frame_bottom_right.fg_color)
        self.radio_button_frame.grid(row=0, column=0, padx=4 * self.padx, sticky="nw")

        # create CTk scrollbar
        # self.scrollbar = ctk.CTkScrollbar(self)
        # self.scrollbar.grid(row=0, column=1, sticky="ns")

        # connect frame scroll event to CTk scrollbar
        # self.radio_button_frame.configure(yscrollcommand=self.scrollbar.set)
    

    def clear_one(self):
        selected_value = self.radio_button_frame.get_value()
        splitted_selected_value = selected_value.split()  # * index | dns
        dns_dict = self.radio_button_frame.get_dns_dict()
        self.chain = self.radio_button_frame.get_chain()

        index = int(splitted_selected_value[0])
        dns_dict_selection = dns_dict[splitted_selected_value[1]]
        len_dns_dict_selection = len(dns_dict_selection)

        print(f'This is index {index} in clear_one')
        for i in range(0, len_dns_dict_selection):
            Flipper_Back.deleteRule(self.chain, str(index - i))

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