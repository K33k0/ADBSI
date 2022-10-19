import pytermgui as ptg
from pytermgui import tim
import sys
import subprocess
from subprocess import check_output
import os
from pytermgui.enums import HorizontalAlignment, VerticalAlignment
import toml

def kill_app(*args):
    sys.exit()

def run(stage):
    status = None
    # If there no devices attached stop.
    if len(get_all_devices()) == 0:
        return
    # Loop through each device running the selected file
    for s in get_all_devices():
        # Loop through each file in the config and sideload the file that matches the button pressed
        for name, file in config['FileLocation'].items():
            if name == stage.label:
                status = subprocess.Popen(
                    [config['adbLocation'],'-s',s,'sideload',file],
                    stdout=subprocess.PIPE,
                    universal_newlines=True,
                    stderr=subprocess.STDOUT
                    )
    
# Loop through the terminal output from the adb command
    while True:
        try:
            nextline = status.stdout.readline()
        except Exception:
            print('Failed at readline')
            raise
        # if line of output is empty or adb is running then kill it
        if nextline == '' and status.poll() is not None:
            status.kill()
            break
        # parse out the number numbers from within the adb output. Turning it into a value out of 100
        if '(' in nextline:
            current_status = float(nextline[nextline.find("(")+1:nextline.find(")")][1:-1])
            status_text.value = f"{int(current_status)}/100"
            
    exitcode = status.returncode
    if exitcode == 0:
        status_text.value = (f"{stage.label} Complete")

def reboot_recovery(button):
    devices = get_all_devices()
    if len(devices) == 0:
        status_text.value = "No Devices Found"
        return

    for s in devices:
        status_text.value = "Rebooting to recovery"
        status = subprocess.Popen([config['adbLocation'],'-s',s,'reboot','recovery'],stdout=subprocess.PIPE,universal_newlines=True,stderr=subprocess.STDOUT)
        while True:
            nextline = status.stdout.readline()
            if nextline == '' and status.poll() is not None:
                break
        status.communicate()[0]
        status_text.value = "Completed reboot recovery"

def get_all_devices(button=None):
    serial_numbers = []
    status = check_output([config['adbLocation'],'devices']).decode('utf-8').split('\n')[1:]
    for l in status:
        if 'device' in l or 'sideload' in l:
            serial_numbers.append(l[:14])
    if button:
        status_text.value = f"{len(serial_numbers)} connected"
    else:
        return serial_numbers
 

config = toml.load('config.toml')
with ptg.WindowManager() as manager:
    exit_button = ptg.Button("Exit", kill_app)
    # Create a list of buttons
    my_buttons = [ptg.Button(name, run) for name in config['FileLocation'].keys()]
    get_devices_button = ptg.Button("Get Serial Numbers",get_all_devices)
    recover_button = ptg.Button("Reboot recovery", reboot_recovery)
    status_text = ptg.Label()
    status_container = ptg.Container(status_text)
    window = ptg.Window(
        "[wm-title]ADB Sideloader",
        ptg.Label("[210 dim]By Kieran Wynne"),
        *my_buttons,
        get_devices_button,
        recover_button,
        exit_button,
        status_container
    )
    manager.add(window)
    manager.run()