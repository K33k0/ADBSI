import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import toml

config = toml.load("config.toml")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('ADBSI by Kieran Wynne')
        self.geometry('295x300')
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # devices
        self.devices_button = ttk.Button(self, text="List Devices", command=self.list_devices)
        self._set_grid(self.devices_button, 0,0)

        # reboot
        self.reboot_button = ttk.Button(self, text="Reboot recovery", command=self.list_devices)
        self._set_grid(self.reboot_button, 1,0)

        # user buttons
        self.user_buttons = [ttk.Button(self, text=name, command=lambda m=name:self.adb_pass_through(m)) for name in config["FileLocation"].keys()]
        for i, button in enumerate(self.user_buttons):
            starting_row = 2
            self._set_grid(button, starting_row+i, column=0)

        self.device_list = tk.Listbox(self)
        self._set_grid(self.device_list, 0,1,3,5,5,5)

    def adb_pass_through(self,button_name):
        showinfo(title='Information', message=f'Hello from {button_name}')

    def list_devices(self):
        devices = ['a','b','c','d','e']
        for i, d in enumerate(devices):
            self.device_list.insert(i+1, d)
        pass

    def _set_grid(self,elem, row, column, columnspan=None, rowspan=None, pad_y=None, pad_x=None):
        elem.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, pady=pad_y, padx=pad_x)
        elem.grid_rowconfigure(1, weight=1)
        elem.grid_columnconfigure(1, weight=0)

if __name__ == "__main__":
    app = App()
    app.mainloop()
