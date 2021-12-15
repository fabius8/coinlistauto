from pynput import keyboard
from pynput.keyboard import Key
from pynput import mouse
import signal
import time
import zmq
import json
import pyperclip

KEYLIST = [
    "Key.enter",
    "Key.backspace",
    "Key.tab",
    "Key.space",
    "Key.delete",
    "Key.esc",
    "Key.up",
    "Key.down",
    "Key.right",
    "Key.left",
    "Key.ctrl_l",
    "Key.ctrl_r",
    "Key.shift",
    "Key.shift_r",
    "Key.caps_lock"
]


signal.signal(signal.SIGINT, signal.SIG_DFL)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:5555')

def on_press(key):
    try:
        message = "controller" + json.dumps({'type': 'key', 'key': format(key.char)})
        print("char:", message)
        socket.send_string(message)

    except AttributeError:
        print("combo:", format(key))
        if format(key) in KEYLIST:
            message = "controller" + json.dumps({'type': 'key', 'key': format(key)})
            print(message)
            socket.send_string(message)
        if format(key) == "Key.f2":
            string = pyperclip.paste()
            message = "controller" + json.dumps({'type': 'key', 'key': format(key), 'text': string})
            print(message)
            socket.send_string(message)


def on_click(x, y, button, pressed):
    #print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
    if not pressed:
       message = "controller" + json.dumps({'type': 'mouse', 'x':x, 'y':y, 'button': format(button)})
       print(message)
       socket.send_string(message)

# ...or, in a non-blocking fashion:
mouse.Listener(on_click=on_click).start()


with keyboard.Listener(on_press=on_press) as k:
    k.join()

