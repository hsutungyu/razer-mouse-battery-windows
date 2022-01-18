import time
import logging

import usb.core
import usb.util
from usb.backend import libusb1
from win10toast import ToastNotifier

# declare constants
# 1. product ID
# 0x0072 = Razer Mamba Wireless Receiver (i.e., 2.4GHz)
# 0x0073 = Razer Mamba Wireless (i.e., when plugged in as wired mouse)
# see README.md for instruction to find the device ID for your mouse
WIRELESS_RECEIVER = 0x0072
WIRELESS_WIRED = 0x0073
# 2. transaction_id.id
# 0x3f for Razer Mamba Wireless
# see README.md for instruction to find the correct transaction_id.id for your mouse
TRAN_ID = b"\x3f"


def get_mouse():
    """
    Function that checks whether the mouse is plugged in or not
    :return: [mouse, wireless]: a list that stores (1) a Device object that represents the mouse; and
    (2) a boolean for stating if the mouse is in wireless state (True) or wired state (False)
    """
    # declare backend: libusb1.0
    backend = libusb1.get_backend()
    # find the mouse by PyUSB
    mouse = usb.core.find(idVendor=0x1532, idProduct=WIRELESS_RECEIVER, backend=backend)
    # if the receiver is not found, mouse would be None
    if not mouse:
        # try finding the wired mouse
        mouse = usb.core.find(idVendor=0x1532, idProduct=WIRELESS_WIRED, backend=backend)
        # still not found, then the mouse is not plugged in, raise error
        if not mouse:
            raise RuntimeError(f"The specified mouse (PID:{WIRELESS_RECEIVER} or {WIRELESS_WIRED}) cannot be found.")
        # else we found the wired mouse, set wireless to False for waiting time
        else:
            wireless = False
    # else we found the wireless mouse, set wireless to True for waiting time
    else:
        wireless = True

    return [mouse, wireless]


def battery_msg():
    """
    Function that creates and returns the message to be sent to the device
    :return: meg: the message to be sent to the mouse for getting the battery level
    """
    # adapted from https://github.com/rsmith-nl/scripts/blob/main/set-ornata-chroma-rgb.py
    # the first 8 bytes in order from left to right
    # status + transaction_id.id + remaining packets (\x00\x00) + protocol_type + command_class + command_id + data_size
    msg = b"\x00" + TRAN_ID + b"\x00\x00\x00\x02\x07\x80"
    crc = 0
    for i in msg[2:]:
        crc ^= i
    # the next 80 bytes would be storing the data to be sent, but for getting the battery no data is sent
    msg += bytes(80)
    # the last 2 bytes would be the crc and a zero byte
    msg += bytes([crc, 0])
    return msg


def get_battery():
    """
    Function for getting the battery level of a Razer Mamba Wireless, or other device if adapted
    :return: a string with the battery level as a percentage (0 - 100)
    """
    # find the mouse and the state, see get_mouse() for detail
    [mouse, wireless] = get_mouse()
    # the message to be sent to the mouse, see battery_msg() for detail
    msg = battery_msg()
    logging.info(f"Message sent to the mouse: {list(msg)}")
    # needed by PyUSB
    # if Linux, need to detach kernel driver
    mouse.set_configuration()
    usb.util.claim_interface(mouse, 0)
    # send request (battery), see razer_send_control_msg in razercommon.c in OpenRazer driver for detail
    req = mouse.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x300, data_or_wLength=msg,
                              wIndex=0x00)
    # needed by PyUSB
    usb.util.dispose_resources(mouse)
    # if the mouse is wireless, need to wait before getting response
    if wireless:
        time.sleep(0.3305)
    # receive response
    result = mouse.ctrl_transfer(bmRequestType=0xa1, bRequest=0x01, wValue=0x300, data_or_wLength=90, wIndex=0x00)
    usb.util.dispose_resources(mouse)
    usb.util.release_interface(mouse, 0)
    logging.info(f"Message received from the mouse: {list(result)}")
    # the raw battery level is in 0 - 255, scale it to 100 for human, correct to 2 decimal places
    return f"{result[9] / 255 * 100:.2f}"


if __name__ == "__main__":
    battery = get_battery()
    logging.info(f"Battery level obtained: {battery}")
    toaster = ToastNotifier()
    toaster.show_toast("Mamba Wireless Battery",
                       f"{battery}% Battery Left",
                       icon_path="mamba_wireless.ico",
                       duration=10)
