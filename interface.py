import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import toml
import threading
from subprocess import check_output
from main import device_list, reboot_device_to_recovery, run_user_sideload, read_subprocess_output

config = toml.load("config.toml")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.process = None

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

        self.status_bar = ttk.Progressbar(self, orient='horizontal', length=200, mode='determinate')
        self._set_grid(self.status_bar, row=self.grid_size()[0]+1, column=0, columnspan=self.grid_size()[0], rowspan=1)

        self.status_box_value = tk.StringVar(value='')
        self.status_label = ttk.Label(self, textvariable=self.status_box_value, justify=tk.CENTER, wraplength=200)
        self._set_grid(self.status_label, row=self.grid_size()[0]+2, column=0, columnspan=self.grid_size()[0], rowspan=1)

    def adb_pass_through(self,button_name):
        devices = list(self.devices.get())
        if len(devices) == 0:
            return
        self.status_bar['maximum'] = 100
        command = config["FileLocation"][button_name]
        self.process = run_user_sideload(config["adbLocation"], list(self.devices.get()), command)
        self.after(100, self.update_status)

    def update_status(self):
        file_sideloading = list(config['FileLocation'].keys())[list(config['FileLocation'].values()).index(self.process.args[4])]

        if self.process.poll() is not None:
            self.status_box_value.set(f'Completed {file_sideloading}')
            self.status_bar['value'] = 100
            return True
        else:
            output = read_subprocess_output(self.process)
            self.status_bar['value'] = output
            self.after(100, self.update_status)

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
