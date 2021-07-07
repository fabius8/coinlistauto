import pyautogui
import re
from PIL import Image, ImageGrab
import pytesseract
import time
from pytesseract import Output
import pyotp
import cv2

Email = ""
secret1 = "SHB6V3HFFZ35DZ5KZRCFRWDE"

print(pyautogui.size())

# 输入网站
while True:
    location = pyautogui.locateOnScreen(
        'fresh.png', 
        confidence=0.9, 
        grayscale=True)
    if location:
        print(location)
        print("Find fresh, goto coinlist")
        point = pyautogui.center(location)
        pyautogui.moveTo(point.x/2 *2, point.y/2, 1)
        pyautogui.click(point.x/2 *2, point.y/2)
        pyautogui.write('coinlist.co', interval=0.01)
        pyautogui.press('enter')
        break
    else:
        print("Not find fresh icon")
        time.sleep(1)

time.sleep(1)

# 点击登陆
while True:
    find = 0
    Img = ImageGrab.grab()
    Img = Img.convert('L')
    d = pytesseract.image_to_data(Img, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        if "Log" in d['text'][i]:
            print("Find Login icon")
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            pyautogui.moveTo(x/2+1, y/2+1, 1)
            pyautogui.click(x/2+1, y/2+1)
            find = 1
            break
    if find == 1:
        break
    print("Not find Login icon")
    time.sleep(1)

# 获取邮箱
while True:
    find = 0
    Img = ImageGrab.grab()
    Img = Img.convert('L')
    d = pytesseract.image_to_data(Img, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        if re.search(r'..*@..*\..*', str(d['text'][i])):
            find = 1
            print("Find Email")
            Email = d['text'][i]
            print(Email)
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            print((x, y, w, h))
            pyautogui.moveTo(x/2, y/2 + h * 8, 1)
            pyautogui.click(x/2, y/2 + h * 8)
            break
    if find == 1:
        break
    print("Not find Email")
    time.sleep(1)

# 输入auth code
while True:
    find = 0
    Img = ImageGrab.grab()
    Img = Img.convert('L')
    d = pytesseract.image_to_data(Img, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        if "AUTH" in d['text'][i]:
            find = 1
            print(d['text'][i])
            print("Find authentication")
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            pyautogui.moveTo(x/2 + w/2, y/2 + h/2 * 4, 1)
            pyautogui.click(x/2 + w/2, y/2 + h/2 * 4)
            pyautogui.press("backspace")
            pyautogui.press("backspace")
            pyautogui.press("backspace")
            pyautogui.press("backspace")
            pyautogui.press("backspace")
            pyautogui.press("backspace")
            totp = pyotp.TOTP(secret1)
            print(Email, pyotp.TOTP(secret1))       
            pyautogui.write(totp.now())
            pyautogui.click(x/2 + w/2, y/2 + h/2 * 10)
            break
    if find == 1:
        break
    print("Not find authentication")

