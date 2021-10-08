import pyautogui
import json
import pytesseract
import time
from PIL import Image, ImageGrab
from pytesseract import Output
import requests

cfg = ""

try:
    cfg = json.load(open('cfg.json'))
except:
    print("no cfg file")


def getQueue():
    Img = ImageGrab.grab()
    Img = Img.convert('L')

    # 设定阈值
    threshold = 200
    table = []
    for i in range(256):
        if i < threshold:
            table.append(1)
        else:
            table.append(0)
    # 图片二值化
    Img = Img.point(table, '1')
    # 最后保存二值化图片
    Img.save("queue.png")

    d = pytesseract.image_to_data(Img, output_type=Output.DICT)
    n_boxes = len(d['level'])
    queuelist = []
    for i in range(n_boxes):
        if "you:" == str(d['text'][i]):
            queuelist.append(str(d['text'][i+1]))
    print(queuelist)
    return queuelist

def sendMessage(server, ql):
    r = requests.post(server, json={"number": cfg["number"],"queuelist": ql})
    print(r.json())

if __name__ == "__main__":
    while True:
        ql = getQueue()
        sendMessage(cfg["server"], ql)
        time.sleep(10)