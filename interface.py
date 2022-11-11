import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import toml
import threading
from subprocess import check_output
from main import device_list, reboot_device_to_recovery, run_user_sideload

config = toml.load("config.toml")


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('ADBSI by Kieran Wynne')
        self.geometry('295x300')
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)


        # reboot
        self.reboot_button = ttk.Button(self, text="Reboot recovery", command=self.reboot_recovery)
        self._set_grid(self.reboot_button, 0,0)

        # user buttons
        self.user_buttons = [ttk.Button(self, text=name, command=lambda m=name:self.adb_pass_through(m)) for name in config["FileLocation"].keys()]
        for i, button in enumerate(self.user_buttons):
            starting_row = 1
            self._set_grid(button, starting_row+i, column=0)

        self.devices = tk.Variable(value=['an','issue','occurred'])
        self.device_list_box = tk.Listbox(self, listvariable=self.devices, activestyle='none', state=tk.DISABLED)
        self._set_grid(self.device_list_box, 0,1,3,5,5,5)

    def adb_pass_through(self,button_name):
        devices = list(self.devices.get())
        if len(devices) == 0:
            return
        command = config["FileLocation"][button_name]
        for i in run_user_sideload(config["adbLocation"], list(self.devices.get()), command):
            print(i)
        return

    def list_devices(self):
        latest_devices = device_list(config["adbLocation"])
        self.devices.set(value=tuple(latest_devices))
        self.after(500, self.list_devices)

    def reboot_recovery(self):
        devices = list(self.devices.get())
        reboot_device_to_recovery(config["adbLocation"], devices)



    def _set_grid(self,elem, row, column, columnspan=None, rowspan=None, pad_y=None, pad_x=None):
        elem.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, pady=pad_y, padx=pad_x)
        elem.grid_rowconfigure(1, weight=1)
        elem.grid_columnconfigure(1, weight=0)

if __name__ == "__main__":
    app = App()
    app.after(10,app.list_devices)
    app.mainloop()
