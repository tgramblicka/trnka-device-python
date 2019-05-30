# !/usr/bin/env python3

import evdev
import requests

backend_ip = "192.168.1.5"


def send_request_to_backend(keycode):
    url = 'http://' + backend_ip + ':8080/trnka-backend/rest/device/key-press/' + keycode
    response = requests.get(url)
    print(response)


try:
    device = evdev.InputDevice('/dev/input/by-path/platform-3f804000.i2c-event')
except FileNotFoundError:
    device = evdev.InputDevice('/dev/input/by-path/platform-20804000.i2c-event')
print(device)

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY and event.value == 1:
        print("Listening on device: ", evdev.categorize(event))
        try:
            print("before key event")
            keyevent = evdev.categorize(event)
            send_request_to_backend(keyevent.keycode)
            print("request sent")
        except Exception as e:
            print(str(e))
