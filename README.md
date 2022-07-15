# Mamba Wireless Battery Indicator

## Introduction

![Notification Screenshot](.github/noti_screenshot.jpg?raw=true)<br>
This is a script for **Windows** written in Python 3.10 that gets the battery level of a Razer Mamba Wireless and shows a tray notification.<br>
Combining with the Task Scheduler, the notification can be regularly shown with self-defined interval (the default is a notification every 15 minutes).

## Instruction

1. Clone this repository
2. Go to the [website](https://libusb.info/) of `libusb` to download the Latest Windows Binaries
3. In the `.7z` file downloaded, extract `\VS2019\MS64\dll\libusb-1.0.dll` to `C:\Windows\System32` and `\VS2019\MS32\dll\libusb-1.0.dll` to `C:\Windows\SysWOW64`
4. If you can run PowerShell script on your system, run `. .\mamba.ps1` in a PowerShell inside the directory
5. Input a time interval in minutes, or press Enter for the default of 15 minutes when prompted
  * The script installs the needed Python packages and sets up the scheduled tasks with a 15-minute time interval

### If you cannot/do not want to run the PowerShell script

1. Run the PowerShell script, then run `python -m pip install -r requirements.txt` inside the directory
2. Go to `Task Scheduler` by searching in the start menu
3. In the `Actions` menu on the right hand side, click `Create Task...`
4. Enter a name and a description as you like
5. Go to `Actions` and click `New...`
6. Enter the details in the dialog box that appears:

| **Field**                 | **To Enter**                      | **Example**                             |
|---------------------------|-----------------------------------|-----------------------------------------|
| Program/script:           | `\path\to\pythonw.exe`            | C:\Python310\pythonw.exe                |
| Add arguments (optional): | `mamba.pyw`                       | `mamba.pyw`                             |
| Start in (optional):      | the path that you put `mamba.pyw` | the directory that you cloned this repo |

7. Go to `Triggers` and click `New...`
8. Enter the details in the dialog box that appears:

| **Field**          | **To Enter**                                            | **Example**                                  |
|--------------------|---------------------------------------------------------|----------------------------------------------|
| Repeat task every: | enable; the notification would appear every `x` minutes | 15 minutes = 1 notification every 15 minutes |
| for a duration of: | Indefinitely                                            |                                              |

9. Click `OK`, done! Now the notification would appear every 15 minutes (or the time interval that you choose)

## Credit

This script is written by looking into [OpenRazer](https://github.com/openrazer/openrazer), a GNU/Linux driver for controlling razer devices.<br>
Also, I have referenced the [blog post](https://rsmith.home.xs4all.nl/hardware/setting-the-razer-ornata-chroma-color-from-userspace.html) and the [script](https://github.com/rsmith-nl/scripts/blob/main/set-ornata-chroma-rgb.py) by Roland Smith in the process of writing this script.

## How to adapt the Python script for your Razer device

**Warning: This process may brick your device (although my mouse did not). TRY AT YOUR OWN RISK!**<br>
To adapt the script for your Razer mouse, follow the steps below: 
1. Get the PIDs of your mouse in both the wireless and wired mode
> Go to Device Manager -> Find your mouse -> Right click -> Properties -> Details -> Hardware Ids -> Repeat in the other state
  * e.g., in wireless state, the entries of Hardware Ids contain `VID_1532&PID_0072`, then 0x0072 is the PID of my mouse in the wireless state
  * In wired state, the entries contain `VID_1532&PID_0073`, then 0x0073 is the PID of my mouse in the wired state
2. `git clone https://github.com/openrazer/openrazer.git`
3. Look at `openrazer/driver/razermouse_driver.c` in the cloned repository
4. Search for `battery` in the `.c` file to find the function `razer_attr_read_charge_level`
5. If the name of your mouse appears inside the switch statement, write down the `transaction_id.id`
  * e.g., I see `USB_DEVICE_ID_RAZER_MAMBA_WIRELESS_RECEIVER` inside the switch statement, so the `transaction_id.id` for my mouse is `0x3f`
  * If you do not see your mouse name inside, then the `transaction_id.id` is `0xff`
6. Open `mamba.pyw` and change the values of `WIRELESS_RECEIVER`, `WIRELESS_WIRED` and `TRAN_ID` according to your findings above
7. Done!

## Troubleshooting

If the script is not working, you could try the following steps:
- Turn off Focus Assist in the action center, accessed by the dialog button on the bottom right corner of the taskbar
- Try a different USB port
- Uninstall any WinUSB driver (upper filter) that you have installed
- Try closing Razer Synapse
- Try uninstalling the driver of your mouse in Device Manager, and then replug the USB receiver
- If the mouse is not responsive after executing the script, replug usb receiver should solve the problem

## License

GNU General Public License v2.0
