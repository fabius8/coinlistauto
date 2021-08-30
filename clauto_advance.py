import pyautogui
import re
import pyotp
import json
import pytesseract
import time
from PIL import Image, ImageGrab
from pytesseract import Output
import imagehash
from fuzzy_match import match
from fuzzy_match import algorithims

secretjson = json.load(open('secret.json'))
Email = ""

location = None
oldImg = None
newImg = None
imgDiff = 5
# 必要素材
freshPic = 'detectpic/fresh.png'
#loginPic = 'detectpic/login.png'
saleOption1 = 'coinlist.co/immutable-x-option-1/new'
saleOption2 = 'coinlist.co/immutable-x-option-2/new'
continuewithPic = 'detectpic/continuewith.png'
continuePic = 'detectpic/continue.png'
japanPic = 'detectpic/japan.png'
selectcountryPic = 'detectpic/selectcountry.png'
manycountryPic = 'detectpic/manycountry.png'
confirmresidencePic = 'detectpic/confirmresidence.png'

q1 = 'detectpic/imxquiz/q1.png'
q2 = 'detectpic/imxquiz/q2.png'
q3 = 'detectpic/imxquiz/q3.png'
q4 = 'detectpic/imxquiz/q4.png'
q5 = 'detectpic/imxquiz/q5.png'
q6 = 'detectpic/imxquiz/q6.png'
q7 = 'detectpic/imxquiz/q7.png'
q8 = 'detectpic/imxquiz/q8.png'
q9 = 'detectpic/imxquiz/q9.png'

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


def autoLogin():
    # 输入网站
    while True:
        location = pyautogui.locateOnScreen(freshPic, confidence=0.9, grayscale=True)
        if location:
            print(location)
            print("Find fresh, goto coinlist")
            point = pyautogui.center(location)
            #pyautogui.moveTo(point.x/2 *2, point.y/2)
            pyautogui.click(point.x/2 *2, point.y/2)
            oldImg = ImageGrab.grab()
            pyautogui.write('coinlist.co/login', interval=0.01)
            oldImg.save("old.png")
            pyautogui.press('enter')
            pyautogui.press('enter')
            time.sleep(4)
            pyautogui.moveTo(point.x, point.y *4)
            pyautogui.click()
            break
        else:
            print("Not find fresh icon")
            time.sleep(2)

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
        pyautogui.click()
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
        Img.save("Email.png")

        d = pytesseract.image_to_data(Img, output_type=Output.DICT)
        n_boxes = len(d['level'])
        for i in range(n_boxes):
            if re.search(r'..*@..*\..*', str(d['text'][i])):
                find = 1
                print("Find Email")
                Email = d['text'][i]
                print(Email)
                # (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                # print((x, y, w, h))
                # pyautogui.moveTo(x/2, y/2 + h * 8, 1)
                # pyautogui.click(x/2, y/2 + h * 8)
                break
        if find == 1:
            break
        print("Not find Email")
        time.sleep(1)

    # 点击邮箱下面LOGIN按钮
    while True:
        find = 0
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
        Img.save("Login.png")

        d = pytesseract.image_to_data(Img, output_type=Output.DICT)
        n_boxes = len(d['level'])
        for i in range(n_boxes):
            if re.search(r'Remember', str(d['text'][i])):
                find = 1
                print("Find Remember")
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                print((x, y, w, h))
                pyautogui.moveTo(x/2, y/2 + h*3)
                pyautogui.click(x/2, y/2 + h*3)
                time.sleep(3)
                break
        if find == 1:
            break
        print("Not find Remember")
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
                find = 1
                print(d['text'][i])
                print("Find authentication")
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                pyautogui.moveTo(x/2 + w, y/2 + h/2 * 4)
                pyautogui.click(x/2 + w, y/2 + h/2 * 4)
                pyautogui.press("backspace")
                pyautogui.press("backspace")
                pyautogui.press("backspace")
                pyautogui.press("backspace")
                pyautogui.press("backspace")
                pyautogui.press("backspace")
                eamillist = {}
                sorted_eamillist = {}
                for i in secretjson:
                    diff = algorithims.trigram(Email, i["Username"])
                    eamillist[i["Username"]] = diff
                sorted_eamillist = sorted(eamillist.items(), key=lambda x: x[1], reverse=True)
                for i in secretjson:
                    if i["Username"] == sorted_eamillist[0][0]:
                        totp = pyotp.TOTP(i["Secret"])
                        print(Email, i["Username"], totp.now())
                        pyautogui.write(totp.now())
                        break
                pyautogui.click(x/2 + w, y/2 + h/2 * 10)   
                break
        if find == 1:
            break
        print("Not find authentication")
        time.sleep(1)

def locatePic(pic):
    while True:
        location = pyautogui.locateOnScreen(pic, confidence=0.9, grayscale=True)
        if location:
            info = "Find " + pic
            print(info)
            point = pyautogui.center(location)
            pyautogui.moveTo(point.x/2, point.y/2)
            time.sleep(1)
            break
        else:
            info = "Not Find " + pic
            print(info)
            time.sleep(2)

def register(saleOption):
    time.sleep(2)
    while True:
        location = pyautogui.locateOnScreen(freshPic, confidence=0.9, grayscale=True)
        if location:
            print(location)
            print("Find fresh, goto sale page")
            point = pyautogui.center(location)
            #pyautogui.moveTo(point.x/2 *2, point.y/2)
            pyautogui.click(point.x/2 *2, point.y/2)
            pyautogui.press('delete')
            oldImg = ImageGrab.grab()
            pyautogui.write(saleOption, interval=0.01)
            oldImg.save("old.png")
            pyautogui.press('enter')
            pyautogui.press('enter')
            time.sleep(4)
            break
        else:
            print("Not find fresh icon")
            time.sleep(2)

    while True:
        location = pyautogui.locateOnScreen(continuewithPic, confidence=0.9, grayscale=True)
        if location:
            print(location)
            print("Find continuewith xxx")
            point = pyautogui.center(location)
            #pyautogui.moveTo(point.x/2 *2, point.y/2)
            pyautogui.click(point.x/2, point.y/2)
            pyautogui.press('enter')
            time.sleep(4)
            break
        else:
            print("Not find continuewith xxx")
            time.sleep(2)

    locatePic(selectcountryPic)
    pyautogui.click()
    locatePic(manycountryPic)
    pyautogui.press("pagedown")
    pyautogui.press("pagedown")
    pyautogui.press("pagedown")
    pyautogui.press("pagedown")
    pyautogui.press("pagedown")
    pyautogui.press("pagedown")
    locatePic(japanPic)
    pyautogui.click()
    locatePic(confirmresidencePic)
    pyautogui.click()
    # again check japan
    while True:
        location = pyautogui.locateOnScreen(japanPic, confidence=0.9, grayscale=True)
        if location:
            print("japan ok")
            break
        else:
            print("japan fail")
            time.sleep(1)
    locatePic(continuePic)
    pyautogui.click()

def quiz(qx):
    while True:
        location = pyautogui.locateOnScreen(qx, confidence=0.98, grayscale=True)
        if location:
            info = "Find " + qx
            print(info)
            point = pyautogui.center(location)
            pyautogui.moveTo(point.x/2, point.y/2)
            pyautogui.click()
            time.sleep(1)
            break
        else:
            info = "Not Find " + qx
            print(info)
            time.sleep(2)

def doQuiz():
    quiz(q1)
    quiz(q2)
    pyautogui.press("pagedown")
    quiz(q3)
    quiz(q4)
    quiz(q5)
    quiz(q6)
    pyautogui.press("pagedown")
    quiz(q7)
    quiz(q8)
    quiz(q9)
    while True:
        location = pyautogui.locateOnScreen(continuePic, confidence=0.9, grayscale=True)
        if location:
            print(location)
            print("Find continue")
            point = pyautogui.center(location)
            #pyautogui.moveTo(point.x/2 *2, point.y/2)
            pyautogui.click(point.x/2, point.y/2)
            break
        else:
            print("Not find continue")
            time.sleep(2)




if __name__ == "__main__":
    autoLogin()
    register(saleOption1)
    doQuiz()
    register(saleOption2)
    doQuiz()