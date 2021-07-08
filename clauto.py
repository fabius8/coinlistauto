import pyautogui
import re
import pyotp
import json
import pytesseract
import time
from PIL import Image, ImageGrab
from pytesseract import Output
import imagehash

secretjson = json.load(open('secret.json'))
Email = ""

oldImg = None
newImg = None
imgDiff = 10
# 必要素材
freshPic = 'detectpic/fresh.png'
loginPic = 'detectpic/login.png'

print(pyautogui.size()) 

def IsForward(oldImg, newImg):
    oldhash = imagehash.average_hash(oldImg)
    newhash = imagehash.average_hash(newImg)
    print("oldhash:", oldhash)
    print("newhash:", newhash)
    print("Image Diff:", abs(newhash - oldhash))
    if abs(newhash - oldhash) > imgDiff:
        return True
    else:
        return False

# 输入网站
while True:
    location = pyautogui.locateOnScreen(freshPic, confidence=0.9, grayscale=True)
    if location:
        print(location)
        print("Find fresh, goto coinlist")
        point = pyautogui.center(location)
        pyautogui.moveTo(point.x/2 *2, point.y/2, 1)
        pyautogui.click(point.x/2 *2, point.y/2)
        oldImg = ImageGrab.grab()
        pyautogui.write('coinlist.co/login', interval=0.01)
        oldImg.save("old.png")
        pyautogui.press('enter')
        pyautogui.click(point.x/2, point.y/2 *2)
        break
    else:
        print("Not find fresh icon")
        time.sleep(1)

while True:
    # 对比图片页面是否前进
    newImg = ImageGrab.grab()
    newImg.save("new.png")
    if IsForward(oldImg, newImg) is False:
        time.sleep(1)
    else:
        break

# 获取邮箱
while True:
    find = 0
    # 光标在邮箱前面，截图前需移除
    pyautogui.press("tab")
    Img = ImageGrab.grab()
    Img = Img.convert('L')

    # 设定阈值
    threshold = 230
    table = []
    for i in range(256):
        if i < threshold:
            table.append(1)
        else:
            table.append(0)
    # 图片二值化
    Img = Img.point(table, '1')
    # 最后保存二值化图片
    Img.save("Email.png")

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
    Img.save("auth.png")
    d = pytesseract.image_to_data(Img, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        if "AUTH" in d['text'][i]:
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
            for i in secretjson:
                if i["Username"] == Email:
                    find = 1
                    totp = pyotp.TOTP(i["Secret"])
                    print(Email, pyotp.TOTP(i["Secret"])) 
                    pyautogui.write(totp.now())
                    pyautogui.click(x/2 + w/2, y/2 + h/2 * 10)
                    break
            break
    if find == 1:
        break
    print("Not find authentication")
