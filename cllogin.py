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
import winsound

#pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\tesseract.exe'

#investName = "immutable-x"
investName = "braintrust"

secretjson = json.load(open('secret.json'))
Email = ""

location = None
oldImg = None
newImg = None
imgDiff = 5
# 必要素材
freshPic = 'detectpic/fresh.png'
saleOption1 = 'coinlist.co/' + investName + '-option-1/new'
saleOption2 = 'coinlist.co/' + investName + '-option-2/new'
queuelink = 'https://sales.coinlist.co/' + investName + '#sale-options'
continuewithPic = 'detectpic/continuewith.png'
continuePic = 'detectpic/continue.png'
japanPic = 'detectpic/japan.png'
japan2Pic = 'detectpic/japan2.png'
selectcountryPic = 'detectpic/selectcountry.png'
manycountryPic = 'detectpic/manycountry.png'
confirmresidencePic = 'detectpic/confirmresidence.png'
registration_completePic = 'detectpic/registration_complete.png'
dashboardPic = 'detectpic/dashboard.png'
loginpagePic = 'detectpic/loginpage.png'
loginPic = 'detectpic/login.png'
authcodePic = 'detectpic/authcode.png'

q1 = 'detectpic/' + investName + 'quiz/q1.png'
q2 = 'detectpic/' + investName + 'quiz/q2.png'
q3 = 'detectpic/' + investName + 'quiz/q3.png'
q4 = 'detectpic/' + investName + 'quiz/q4.png'
q5 = 'detectpic/' + investName + 'quiz/q5.png'
q6 = 'detectpic/' + investName + 'quiz/q6.png'
q7 = 'detectpic/' + investName + 'quiz/q7.png'
q8 = 'detectpic/' + investName + 'quiz/q8.png'
q9 = 'detectpic/' + investName + 'quiz/q9.png'


def locatePic(pic):
    while True:
        location = pyautogui.locateOnScreen(pic, confidence=0.9, grayscale=True)
        if location:
            info = "Find " + pic
            print(info)
            point = pyautogui.center(location)
            pyautogui.moveTo(point.x, point.y)
            time.sleep(0.3)
            break
        else:
            info = "Not Find " + pic
            print(info)
            time.sleep(2)

def autoLogin():
    # 输入网站
    while True:
        location = pyautogui.locateOnScreen(freshPic, confidence=0.9, grayscale=True)
        if location:
            print(location)
            print("Find fresh, goto coinlist")
            point = pyautogui.center(location)
            print(point)
            pyautogui.moveTo(point.x *2, point.y, 2)
            pyautogui.click()
            pyautogui.click()
            pyautogui.write('coinlist.co/login', interval=0.01)
            pyautogui.press('enter')
            pyautogui.press('enter')
            time.sleep(4)
            pyautogui.moveTo(point.x, point.y *4)
            pyautogui.click()
            break
        else:
            print("Not find fresh icon")
            time.sleep(2)

    locatePic(loginpagePic)

    # 获取邮箱
    while True:
        find = 0
        pyautogui.click()
        Img = ImageGrab.grab()
        Img = Img.convert('L')
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
        time.sleep(2)

    locatePic(loginPic)
    pyautogui.click()
    time.sleep(3)

    locatePic(authcodePic)
    pyautogui.click()
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
    
    locatePic(loginPic)
    pyautogui.click()
    time.sleep(3)
    
    locatePic(dashboardPic)

def enterQueue(queuelink):
    while True:
        location = pyautogui.locateOnScreen(freshPic, confidence=0.9, grayscale=True)
        if location:
            print(location)
            print("Find fresh, goto sale page")
            point = pyautogui.center(location)
            #pyautogui.moveTo(point.x/2 *2, point.y/2)
            pyautogui.click(point.x *2, point.y)
            pyautogui.press('delete')
            pyautogui.write(queuelink, interval=0.01)
            pyautogui.press('enter')
            pyautogui.press('enter')
            time.sleep(3)
            pyautogui.press('pagedown')
            break
        else:
            print("Not find fresh icon")
            time.sleep(2)


def register(saleOption):
    while True:
        location = pyautogui.locateOnScreen(freshPic, confidence=0.9, grayscale=True)
        if location:
            print(location)
            print("Find fresh, goto sale page")
            point = pyautogui.center(location)
            #pyautogui.moveTo(point.x/2 *2, point.y/2)
            pyautogui.click(point.x *2, point.y)
            pyautogui.press('delete')
            pyautogui.write(saleOption, interval=0.01)
            pyautogui.press('enter')
            pyautogui.press('enter')
            time.sleep(0.2)
            break
        else:
            print("Not find fresh icon")
            time.sleep(2)

    time.sleep(3)
    while True:
        location = pyautogui.locateOnScreen(continuewithPic, confidence=0.9, grayscale=True)
        if location:
            print(location)
            print("Find continuewith xxx")
            point = pyautogui.center(location)
            #pyautogui.moveTo(point.x/2 *2, point.y/2)
            pyautogui.click(point.x, point.y)
            pyautogui.press('enter')
            time.sleep(0.2)
            break
        else:
            print("Not find continuewith xxx")
            time.sleep(2)

    time.sleep(3)
    locatePic(selectcountryPic)
    pyautogui.click()
    time.sleep(1)
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
        location = pyautogui.locateOnScreen(japan2Pic, confidence=0.9, grayscale=True)
        if location:
            print("japan ok")
            break
        else:
            print("japan fail")
            time.sleep(2)
    locatePic(continuePic)
    pyautogui.click()

def quiz(qx):
    while True:
        location = pyautogui.locateOnScreen(qx, confidence=0.98, grayscale=True)
        if location:
            info = "Find " + qx
            print(info)
            point = pyautogui.center(location)
            pyautogui.moveTo(point.x, point.y)
            pyautogui.click()
            time.sleep(0.4)
            break
        else:
            info = "Not Find " + qx
            print(info)
            time.sleep(2)

def doQuiz():
    time.sleep(3)
    quiz(q1)
    quiz(q2)
    pyautogui.press("pagedown")
    time.sleep(1)
    quiz(q3)
    quiz(q4)
    quiz(q5)
    quiz(q6)
    pyautogui.press("pagedown")
    time.sleep(1)
    quiz(q7)
    quiz(q8)
    quiz(q9)
    locatePic(continuePic)
    pyautogui.click()
    time.sleep(2)
    locatePic(registration_completePic)




if __name__ == "__main__":
    autoLogin()
    #register(saleOption1)
    #doQuiz()
    #register(saleOption2)
    #doQuiz()
    winsound.MessageBeep(1)
    
