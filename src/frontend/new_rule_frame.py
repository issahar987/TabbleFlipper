import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from backend import Flipper_Back
from pathlib import Path
import os
import json


class NewRuleFrame(ctk.CTkFrame):
    def __init__(self, width, height, button_width, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width=width
        self.height=height
        self.button_width=button_width
        self.padx=43
        self.pady=20

        self.configure(width = self.width,
                       height = self.height)
        self.grid_propagate(False)
        
        self.button_import = ctk.CTkButton(master=self,
                                           width=self.button_width,
                                           text="Import",
                                           command=self.import_)
        self.button_export = ctk.CTkButton(master=self,
                                           width=self.button_width,
                                           text="Export",
                                           command=self.export)
        self.button_new_rule = ctk.CTkButton(master=self,
                                             width=self.button_width,
                                             text="New rule",
                                             command=self.new_rule)

        

        self.button_import.grid(column=0, row=0, padx=1 * self.padx, pady=self.pady, sticky='w')
        self.button_new_rule.grid(column=1, row=0, padx=1.5 * self.padx, pady=self.pady, sticky='n')
        self.button_export.grid(column=2, row=0, padx=1 * self.padx, pady=self.pady, sticky='e')

    def new_rule(self):
        print("new_rule")

    def import_(self):
        Flipper_Back.imortChain('EXPORT.txt')
        print("importing")

    def export(self):
        print("exporting")
        Flipper_Back.exportChain("INPUT")