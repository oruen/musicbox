#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "unT" # Change XYZ to the UID of your NFC/RFID Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
import requests
import time
import sys

tag_type = 0
last_seen_tag = None
tags = [(4, 169, 119, 18, 43, 94, 128),
        (4, 156, 235, 18, 43, 94, 128),
        (4, 174, 214, 18, 43, 94, 128),
        (4, 174, 182, 18, 43, 94, 128),
        (4, 129, 80, 18, 43, 94, 128)]
songs = {0: "shapka.mp3",
         1: "vorona.mp3",
         2: "vinni-puh.mp3",
         3: "buratino.mp3",
         4: "utyata.mp3"}

def play_song(song_id):
    global songs
    url = "http://localhost:6680/mopidy/rpc"
    if song_id in songs:
        filename = songs[song_id]
        print(requests.post(url, json={"jsonrpc": "2.0", "id": 1, "method": "core.playback.stop"}).text)
        print(requests.post(url, json={"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.clear"}).text)
        print(requests.post(url, json={"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.add", "params": {"uri": "file:///var/lib/mopidy/media/" + filename}}).text)
        print(requests.post(url, json={"jsonrpc": "2.0", "id": 1, "method": "core.playback.play"}).text)

# Callback function for state changed callback
def cb_state_changed(state, idle, nr):
    try:
        if state == nr.STATE_REQUEST_TAG_ID_READY:
            ret = nr.get_tag_id()
            global last_seen_tag
            global tags
            if ret != last_seen_tag:
                print("Found tag of type " + str(ret.tag_type) + " " + str(ret) + " with ID [" +
                      " ".join(map(str, map(hex, ret.tid[:ret.tid_length]))) + "]")
                if ret.tid in tags:
                    ind = tags.index(ret.tid)
                    print("Tag number " + str(ind))
                    play_song(ind)
                else:
                    print("Unknown tag")
            last_seen_tag = ret

        # Cycle through all types
        if idle:
            global tag_type
            tag_type = (tag_type + 1) % 3
            nr.request_tag_id(tag_type)
    except:
        sys.exit("Error occured")

if __name__ == "__main__":
    try:
        time.sleep(10)
        ipcon = IPConnection() # Create IP connection
        nr = BrickletNFCRFID(UID, ipcon) # Create device object

        ipcon.connect(HOST, PORT) # Connect to brickd
        # Don't use device before ipcon is connected

        # Register state changed callback to function cb_state_changed
        nr.register_callback(nr.CALLBACK_STATE_CHANGED,
                             lambda x, y: cb_state_changed(x, y, nr))

        # Start scan loop
        nr.request_tag_id(nr.TAG_TYPE_MIFARE_CLASSIC)

        #raw_input("Press key to exit\n") # Use input() in Python 3
        while True:
            time.sleep(1)
    except:
        system.exit("Error")
        # hello
    #ipcon.disconnect()
