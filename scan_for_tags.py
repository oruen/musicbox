#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "unT" # Change XYZ to the UID of your NFC/RFID Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
import requests
import time

tag_type = 0
last_seen_tag = None
tag_black = (4, 201, 175, 146, 158, 51, 128)
tag_red = (4, 130, 161, 146, 158, 51, 128)
songs = {1: "shapka.mp3",
         2: "vorona.mp3",
         3: "vinni-puh.mp3",
         4: "buratino.mp3",
         5: "utyata.mp3"}

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
    if state == nr.STATE_REQUEST_TAG_ID_READY:
        ret = nr.get_tag_id()
        global last_seen_tag
        global tag_a
        if ret != last_seen_tag:
            #print("Found tag of type " + str(ret.tag_type) + " " + str(ret) + " with ID [" +
            #      " ".join(map(str, map(hex, ret.tid[:ret.tid_length]))) + "]")
            if tag_black == ret.tid:
                print("Tag Black")
                play_song(1)
            elif tag_red == ret.tid:
                print("Tag Red")
                play_song(2)
            else:
                print("Unknown tag")
        last_seen_tag = ret

    # Cycle through all types
    if idle:
        global tag_type
        tag_type = (tag_type + 1) % 3
        nr.request_tag_id(tag_type)

if __name__ == "__main__":
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
        # hello
    #ipcon.disconnect()
