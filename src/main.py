import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import Flipper_Back
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
        # self.radio_button_1 = ctk.CTkRadioButton(self, text="Option 1", value="Option 1", variable=self.radio_button_var)
        # self.radio_button_1.grid(row=1, column=0, padx=10, pady=10)
        # self.radio_button_2 = ctk.CTkRadioButton(self, text="Option 2", value="Option 2", variable=self.radio_button_var)
        # self.radio_button_2.grid(row=2, column=0, padx=10, pady=10)
        # self.radio_button_3 = ctk.CTkRadioButton(self, text="Option 3", value="Option 3", variable=self.radio_button_var)
        # self.radio_button_3.grid(row=3, column=0, padx=10, pady=(10, 20))
    def get_value(self):
        """ returns selected value as a string, returns an empty string if nothing selected """
        return self.radio_button_var.get()

    def set_value(self, selection):
        """ selects the corresponding radio button, selects nothing if no corresponding radio button """
        self.radio_button_var.set(selection)

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
        style = ttk.Style()
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

        self.radio_button_frame_1 = RadioButtonFrame(self.frame_bottom_right, frame_height=self.frame_bottom_right["height"],ip_list=IP_list)
        self.radio_button_frame_1.grid(row=0, column=0, sticky="nw")

        # create CTk scrollbar
        # self.scrollbar = ctk.CTkScrollbar(self)
        # self.scrollbar.grid(row=0, column=1, sticky="ns")

        # connect frame scroll event to CTk scrollbar
        # self.radio_button_frame_1.configure(yscrollcommand=self.scrollbar.set)
    
    def clear_one(self):
        selected_value = int(self.radio_button_frame_1.get_value())
        print(selected_value)
        Flipper_Back.deleteRule('INPUT', selected_value)
        self.refresh()
    def clear_iptables(self):
        Flipper_Back.ClearAll()
        self.refresh()
        # for widgets in frame.winfo_children():
        #     widgets.destroy()


if __name__ == "__main__":
    #  create a window first
    # define window dimensions width and height
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800
    Flipper_Back.EnterSudo("kali")
    app = App(WINDOW_WIDTH, WINDOW_HEIGHT)
    # *get the screen size of your computer
    # *[width and height using the root object as foolows]
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    # Get the window position from the top dynamically
    # as well as position from left or right as follows
    position_top = int(screen_height / 2 - WINDOW_HEIGHT / 2)
    position_right = int(screen_width / 2 - WINDOW_WIDTH / 2)
    # this is the line that will center your window
    app.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{position_right}+{position_top}')
    # lock window to not be resizable
    app.resizable(False, False)
    # initialise the window
    app.mainloop(0)
