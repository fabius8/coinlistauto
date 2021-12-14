import signal
import zmq
import json
import pyautogui
from pynput import keyboard
from pynput import mouse
from pynput.keyboard import Key, Controller

keyboard = Controller()

signal.signal(signal.SIGINT, signal.SIG_DFL)

serverIp = "43.133.11.104"
tcpUrl = "tcp://" + serverIp + ":5555"
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(tcpUrl)
socket.setsockopt(zmq.SUBSCRIBE, b'controller')

while True:
    message = socket.recv_string()
    print(message)
    #print(f'{message}'[10:])
    action = json.loads(f'{message}'[10:])
    print(type(action),action)
    if action["type"]:
        print("Press Key: ", action["key"])
        if len(action["key"]) == 1:
            keyboard.tap(action["key"])
        else:
            keyboard.tap(getattr(Key, action["key"][4:]))
    else:
        pyautogui.moveTo(action["x"], action["y"])
        pyautogui.click()
        #mouse.move(action['x'], action['y'])
        # Press and release
        #mouse.press(Button.left)
        #mouse.release(Button.left)
