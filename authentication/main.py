# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time


# If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
import serial
import adafruit_fingerprint

from .firebase import change_register_status,change_login_status,change_login_sensor_id
uart = serial.Serial("COM8", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi and hardware UART:
# import serial
# uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

##################################################


def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True


# pylint: disable=too-many-branches
def get_fingerprint_detail():
    if finger.read_templates() != adafruit_fingerprint.OK:

        print("Finger Print sensor Error")
        change_login_status("Finger Print sensor Error")
    """Get a finger print image, template it, and see if it matches!
    This time, print out each error instead of just returning on failure"""
    print("Getting image...", end="")
    i = finger.get_image()
    if i == adafruit_fingerprint.OK:
        print("Image taken")
        change_login_status("Image taken")
    else:
        if i == adafruit_fingerprint.NOFINGER:
            print("No finger detected")
            change_login_status("No finger detected")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
            change_login_status("Imaging error")
        else:
            print("Other error")
            change_login_status("Other error")
        return False,0

    print("Templating...", end="")
    change_login_status("Templating...")
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        print("Templated")
        change_login_status("Templated")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
            change_login_status("Image too messy")

        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
            change_login_status("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
            change_login_status("Image invalid")
        else:
            print("Other error")
            change_login_status("Other error")
        return False,0

    print("Searching...", end="")    
    change_login_status("Searching...")    

    i = finger.finger_fast_search()
    # pylint: disable=no-else-return
    # This block needs to be refactored when it can be tested.
    if i == adafruit_fingerprint.OK:
        print("Found fingerprint!")
        change_login_status("Found fingerprint!")
        change_login_sensor_id(finger.finger_id)
        return True,finger.finger_id
    else:
        if i == adafruit_fingerprint.NOTFOUND:
            print("No match found")
            change_login_status("No match found")
        else:
            print("Other error")            
            change_login_status("Other error")            

        return False,0


# pylint: disable=too-many-statements
def enroll_finger(location):

    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="")
            change_register_status("Place finger on sensor...")

        else:
            print("Place same finger again...", end="")
            change_register_status("Place same finger again...")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                change_register_status("Image taken..")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                change_register_status("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
                change_register_status("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
                change_register_status("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
                change_register_status("Image invalid")
            else:
                print("Other error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            change_register_status("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="")
    change_register_status("Creating model...")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
        change_register_status("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
            change_register_status("Prints did not match")
        else:
            print("Other error")
        return False

    print("Storing model #%d..." % location, end="")
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
        change_register_status("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True


##################################################


def get_num():
    """Use input() to get a valid number from 1 to 127. Retry till success!"""
    i = 0
    while (i > 127) or (i < 1):
        try:
            i = int(input("Enter ID # from 1-127: "))
        except ValueError:
            pass
    return i


# while True:
#     print("----------------")
#     if finger.read_templates() != adafruit_fingerprint.OK:
#         raise RuntimeError("Failed to read templates")
#     print("Fingerprint templates:", finger.templates)
#     print("e) enroll print")
#     print("f) find print")
#     print("d) delete print")
#     print("----------------")
#     c = input("> ")

#     if c == "e":
#         enroll_finger(get_num())
#     if c == "f":
#         if get_fingerprint():
#             print("Detected #", finger.finger_id, "with confidence", finger.confidence)
#         else:
#             print("Finger not found")
#     if c == "d":
#         if finger.delete_model(get_num()) == adafruit_fingerprint.OK:
#             print("Deleted!")
#         else:
#             print("Failed to delete")