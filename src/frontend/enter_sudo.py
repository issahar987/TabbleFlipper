import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from backend import Flipper_Back as FB
import socket


class App_enter_sudo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.frame_Main = ctk.CTkFrame(master=self,
                                       corner_radius=10)
        self.pswd = ctk.StringVar()
        self.entry_pswd = ctk.CTkEntry(master=self.frame_Main,
                                       show="*",
                                       placeholder_text="IP/DNS",
                                       textvariable=self.pswd)
        self.enter_sudo_button = ctk.CTkButton(master=self.frame_Main,
                                               text="enter sudo pswd",
                                               command=self.enter_pswd)
        self.frame_Main.grid(column=0, row=0, padx=5, pady=5)
        self.entry_pswd.grid(column=0, row=0, padx=5, pady=5)
        self.enter_sudo_button.grid(column=1, row=0, padx=5, pady=5)

    def enter_pswd(self):
        FB.EnterSudo(self.entry_pswd.get())
        self.destroy()
