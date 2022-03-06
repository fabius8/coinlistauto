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

investName = "axelar"
secretjson = json.load(open('secret.json'))
Email = ""


# 必要素材
googleico = "detectpic/googleico.png"
freshPic = 'detectpic/fresh.png'
saleOption1 = 'sales.coinlist.co/' + investName + '-token-sale/new'
#saleOption2 = 'coinlist.co/' + investName + '-option-2/new'

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
#q10 = 'detectpic/' + investName + 'quiz/q10.png'

def locatePic(pic, confidence):
    while True:
        if pyautogui.position().x == 0 and pyautogui.position().y == 0:
            print("no screen")
            time.sleep(3)
            continue
        location = pyautogui.locateOnScreen(pic, confidence=confidence, grayscale=True)
        if location:
            print("Find", pic)
            point = pyautogui.center(location)
            pyautogui.moveTo(point.x, point.y)
            time.sleep(0.3)
            return point
        else:
            print("Not Find", pic)
            time.sleep(2)

def autoLogin():
    # 输入网站
    point = locatePic(freshPic, 0.9)
    pyautogui.moveTo(point.x *2, point.y, 2)
    pyautogui.click()
    pyautogui.click()
    pyautogui.write('coinlist.co/login', interval=0.01)
    pyautogui.press('enter')
    pyautogui.press('enter')
    time.sleep(4)
    pyautogui.moveTo(point.x, point.y *4)
    pyautogui.click()

    locatePic(loginpagePic, 0.9)

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
                break
        if find == 1:
            break
        print("Not find Email")
        time.sleep(2)

    #点击登陆
    locatePic(loginPic, 0.9)
    pyautogui.click()
    time.sleep(3)

    #输入验证码
    locatePic(authcodePic, 0.9)
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
        if i["Username"] == sorted_eamillist[0][0] and "CoinList" in i["Issuer"]:
            totp = pyotp.TOTP(i["Secret"])
            print(Email, i["Username"], totp.now())
            pyautogui.write(totp.now())
            break
    
    locatePic(loginPic, 0.9)
    pyautogui.click()
    time.sleep(3)
    locatePic(dashboardPic, 0.9)

def register(saleOption):
    point = locatePic(freshPic, 0.9)
    print("Find fresh, goto sale page")
    pyautogui.click(point.x *2, point.y)
    pyautogui.press('delete')
    pyautogui.write(saleOption, interval=0.01)
    pyautogui.press('enter')
    pyautogui.press('enter')

    time.sleep(3)
    locatePic(continuewithPic, 0.8)
    pyautogui.click()
    time.sleep(3)
    locatePic(freshPic, 0.9)
    if pyautogui.locateOnScreen(registration_completePic, confidence=0.85, grayscale=True):
        return True
    locatePic(selectcountryPic, 0.9)
    pyautogui.click()
    time.sleep(1)
    locatePic(manycountryPic, 0.9)
    pyautogui.press("pagedown")
    pyautogui.press("pagedown")
    pyautogui.press("pagedown")
    pyautogui.press("pagedown")
    pyautogui.press("pagedown")
    pyautogui.press("pagedown")
    locatePic(japanPic, 0.9)
    pyautogui.click()
    locatePic(confirmresidencePic, 0.9)
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
    
    locatePic(continuePic, 0.85)
    pyautogui.click()
    locatePic(freshPic, 0.9)

def quiz(qx, confidence):
    while True:
        location = pyautogui.locateOnScreen(qx, confidence=confidence, grayscale=True)
        if location:
            print("Find", qx)
            point = pyautogui.center(location)
            pyautogui.moveTo(point.x, point.y)
            pyautogui.click()
            time.sleep(0.4)
            break
        else:
            print("Not Find", qx)
            time.sleep(2)

def doQuiz():
    time.sleep(3)
    #pyautogui.press("down")
    quiz(q1, 0.95)
    quiz(q2, 0.85)
    quiz(q3, 0.85)
    pyautogui.press("pagedown")
    time.sleep(1)

    quiz(q4, 0.85)
    quiz(q5, 0.95)
    quiz(q6, 0.85)
    quiz(q7, 0.85)
    pyautogui.press("pagedown")
    time.sleep(1)

    
    quiz(q8, 0.85)
    quiz(q9, 0.85)
    locatePic(continuePic, 0.85)
    pyautogui.click()
    time.sleep(2)
    locatePic(registration_completePic, 0.85)

if __name__ == "__main__":
    time.sleep(2)
    pyautogui.hotkey('win', 'm')
    for pos in pyautogui.locateAllOnScreen(googleico, grayscale=True, confidence=0.85):
        point = pyautogui.center(pos)
        pyautogui.moveTo(point.x, point.y)
        pyautogui.doubleClick()
        locatePic(freshPic, 0.8)
        pyautogui.hotkey('win', 'up')
        autoLogin()

        if True == register(saleOption1):
            winsound.MessageBeep(1)
        else:
            doQuiz()

        # if True == register(saleOption2):
        #     winsound.MessageBeep(1)
        # else:
        #     doQuiz()
      
        pyautogui.hotkey('win', 'm')
