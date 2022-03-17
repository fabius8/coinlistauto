import signal
import zmq
import json
from pynput import keyboard
from pynput import mouse
from pynput.mouse import Button
from pynput.keyboard import Key
import pyperclip

keyboard = keyboard.Controller()
mouse = mouse.Controller()

signal.signal(signal.SIGINT, signal.SIG_DFL)

serveIp = "43.154.1.243"
tcpURL = 'tcp://' + serveIp + ':5555'
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(tcpURL)
socket.setsockopt(zmq.SUBSCRIBE, b'controller')

while True:
    message = socket.recv_string()
    print(message)
    #print(f'{message}'[10:])
    action = json.loads(f'{message}'[10:])
    #print(type(action),action)
    if action["type"] == "key":
        print("Press Key: ", action["key"])
        if len(action["key"]) == 1:
            keyboard.tap(action["key"])
        elif action["key"] == "Key.f2":
            pyperclip.copy(action["text"])
        else:
            keyboard.tap(getattr(Key, action["key"][4:]))

    elif action["type"] == "mouse":
        if action['button'] == "Button.left":
            #print("left", action['x'], action['y'])
            mouse.position = (action['x'], action['y']) 
            mouse.click(Button.left)
        else:
            #print("right", action['x'], action['y'])
            mouse.position = (action['x'], action['y']) 
            mouse.click(Button.right)

