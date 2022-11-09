import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from backend import Flipper_Back
from frontend import RadioButtonFrame as RBF
from pathlib import Path
import os
import json
import socket


class App(ctk.CTk, tk.Tk):
    def __init__(self, width, height):
        self.width = height
        self.height = height
        self.padx = 10
        self.pady = 5
        self.main_height = (8 * self.height) / 10
        self.side_width = (self.width/2) - (2 * self.padx)
        self.side_width_inside = self.side_width - (2 * self.padx)
        self.button_width = self.width / (2 * 4)
        self.radio_button_list = []
        super().__init__()
        # define main frames
        self.menu_frame = ctk.CTkFrame(master=self,
                                       width=self.width,
                                       height=self.height / 20,
                                       corner_radius=10)
        self.main_frame = ctk.CTkFrame(master=self,
                                       width=self.width,
                                       height=self.main_height,
                                       corner_radius=10)
        self.frame_export = ctk.CTkFrame(master=self,
                                         width=width,
                                         height=(1 * height) / 10,
                                         corner_radius=10)
        # define left panel frame
        self.frame_left = ctk.CTkFrame(master=self.main_frame,
                                       width=self.side_width,
                                       height=self.main_height,
                                       corner_radius=10)
        # define frames inside left frame
        self.frame_upper_left = ctk.CTkFrame(master=self.frame_left,
                                        width=self.side_width_inside,
                                        height=self.main_height / 6,
                                        corner_radius=10)
        self.frame_bottom_left = ctk.CTkFrame(master=self.frame_left,
                                         width=self.side_width_inside,
                                         height=(5 * self.main_height) / 6,
                                         corner_radius=10)
        # define right panel frame
        self.frame_right = ctk.CTkFrame(master=self.main_frame,
                                        width=self.side_width,
                                        height=self.main_height,
                                        corner_radius=10)
        # define frames inside left frame
        self.frame_upper_right = ctk.CTkFrame(master=self.frame_right,
                                              width=self.side_width_inside,
                                              height=self.main_height / 6,
                                              corner_radius=10)
        self.frame_bottom_right = ctk.CTkFrame(master=self.frame_right,
                                               width=self.side_width_inside,
                                               height=(5 * self.main_height) / 6,
                                               corner_radius=10)
        # style.theme_use("clam")
        # style.configure("Treeview", background="black", fieldbackground="black", foreground="white")
        # self.tree = ttk.Treeview(master=self.frame_bottom_right)
        self.ip = ctk.StringVar()
        self.entry = ctk.CTkEntry(master=self.frame_upper_left,
                                  width= self.side_width_inside - self.button_width - (4 * self.padx),
                                  placeholder_text="IP/DNS",
                                  textvariable=self.ip)
        self.button = ctk.CTkButton(master=self.frame_upper_left,
                                    width=self.button_width,
                                    text="Submit",
                                    command=self.submit)
        self.button_import = ctk.CTkButton(master=self.frame_export,
                                           width=self.button_width,
                                           text="Import",
                                           command=self.import_)
        self.button_export = ctk.CTkButton(master=self.frame_export,
                                           width=self.button_width,
                                           text="Export",
                                           command=self.export)
        self.button_refresh = ctk.CTkButton(master=self.frame_upper_right,
                                            width=self.button_width,
                                            text="Refresh",
                                            command=self.refresh)
        self.button_clear = ctk.CTkButton(master=self.frame_upper_right,
                                          width=self.button_width,
                                          text="Clear all",
                                          command=self.clear_iptables)
        self.button_clear_one = ctk.CTkButton(master=self.frame_upper_right,
                                              width=self.button_width,
                                              text="Clear selection",
                                              command=self.clear_one)

        # * main frames
        self.menu_frame.grid(column=0, row=0, padx=0, pady=5, sticky="n")
        self.main_frame.grid(column=0, row=1, padx=0, pady=5, sticky="n")
        self.frame_export.grid(column=0, row=2, padx=0, pady=5, sticky="s")

        # * left main frame
        self.frame_left.grid(column=0, row=1, padx=self.padx, pady=5)
        self.frame_upper_left.grid(column=0, row=0, padx=self.padx, pady=5)
        self.frame_bottom_left.grid(column=0, row=1, padx=self.padx, pady=5)

        # * right main frame
        self.frame_right.grid(column=1, row=1, padx=self.padx, pady=5, sticky='n')
        self.frame_upper_right.grid(column=0, row=0, padx=self.padx, pady=5, sticky='nsew')
        self.frame_bottom_right.grid(column=0, row=1, padx=self.padx, pady=5, sticky='n')
        # create CTk scrollbar
        # self.scrollbar = ctk.CTkScrollbar(self.frame_bottom_right)
        # self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.button_refresh.grid(column=0, row=0, padx=1 * self.padx, pady=10, sticky='w')
        self.button_clear_one.grid(column=1, row=0, padx=1 * self.padx, pady=10)
        self.button_clear.grid(column=2, row=0, padx=1 * self.padx, pady=10, sticky='e')

        # * entry frame

        self.entry.grid(column=0, row=0, padx=self.padx, pady=10)
        self.button.grid(column=1, row=0, padx=self.padx, pady=10)
        # * bottom inport/export frame

        self.button_import.grid(column=0, row=0, padx=150, pady=30, sticky='w')
        self.button_export.grid(column=1, row=0, padx=150, pady=30, sticky='e')

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