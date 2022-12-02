This is a simple interface for sideloading files via ADB.

To get started create or rename the config.toml.example to config.toml.
Next update the file location for ADB ([Can be downloaded here](https://forum.xda-developers.com/t/tool-minimal-adb-and-fastboot-2-9-18.2317790/)).

Under the _Files_ header on the left of the equals symbol is the name of the button you would like.
On the right of the equals sign is the locaction of the file you are sending.

For example:

[FileLocation]
"My first button" = "C:/WipeDevice.zip"

Once your device is ready to accept input from ADB press the button in your terminal.


_Tested on windows 11_
