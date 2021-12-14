from pynput import keyboard
from pynput.keyboard import Key
from pynput import mouse
import signal
import time
import zmq
import json

signal.signal(signal.SIGINT, signal.SIG_DFL)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:5555')

def on_press(key):
    try:
        #print('alphanumeric key {0} pressed'.format(key.char))
        #print(type(key), '{0} released'.format(key.char))
        message = "controller" + json.dumps({'type': True, 'key': format(key.char)})
        print(message)
        socket.send_string(message)

    except AttributeError:
        print(format(key))
        if format(key) == "Key.backspace" or format(key) == "Key.enter":
            #print('special key {0} pressed'.format(key))
            #print(type(key), '{0} released'.format(key))
            message = "controller" + json.dumps({'type': True, 'key': format(key)})
            print(message)
            socket.send_string(message)


def on_click(x, y, button, pressed):
    #print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
    if not pressed:
       message = "controller" + json.dumps({'type': False, 'x':x, 'y':y})
       print(message)
       socket.send_string(message)

# ...or, in a non-blocking fashion:
mouse.Listener(on_click=on_click).start()


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()


