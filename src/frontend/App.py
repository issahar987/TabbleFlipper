import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from backend import Flipper_Back
from frontend import RadioButtonFrame as RBF
from frontend import chain_frame
from frontend import functions_frame
from frontend import ip_list_frame
from frontend import new_rule_frame
from frontend import enter_sudo
from pathlib import Path
import os
import json
import socket


class App(ctk.CTk, tk.Tk):
    def __init__(self, width, height):
        super().__init__()
        self.width = (80 * width)/100
        self.height = height
        self.pady = 10
        self.padx = 60
        self.button_width = 50

        self.chain_frame = chain_frame.ChainFrame(master=self,
                                                  width=self.width,
                                                  height=(
                                                      10 * self.height) / 100,
                                                  button_width=self.button_width)

        self.ip_list_frame = ip_list_frame.IpListFrame(master=self,
                                                       width=self.width,
                                                       height=(
                                                           65 * self.height) / 100,
                                                       button_width=self.button_width)
        self.configure(fg_color=['#EBEBEC', '#212325'])  # sets widget color to black
        self.functions_frame = functions_frame.FunctionsFrame(master=self,
                                                              width=self.width,
                                                              height=(
                                                                  10 * self.height) / 100,
                                                              button_width=self.button_width,
                                                              ip_list_frame=self.ip_list_frame,
                                                              chain_frame=self.chain_frame)
        self.new_rule_frame = new_rule_frame.NewRuleFrame(master=self,
                                                          width=self.width,
                                                          height=(
                                                              10 * self.height) / 100,
                                                          button_width=self.button_width)

        self.chain_frame.grid(
            column=0, row=0, padx=self.padx, pady=0, sticky="n")
        self.functions_frame.grid(
            column=0, row=1, padx=self.padx, pady=0, sticky="n")
        self.ip_list_frame.grid(
            column=0, row=2, padx=self.padx, pady=self.pady, sticky="n")
        self.new_rule_frame.grid(
            column=0, row=3, padx=self.padx, pady=self.pady, sticky="s")
