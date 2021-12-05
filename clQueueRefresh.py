import pyautogui
import datetime
import time

freshPic = 'detectpic/fresh.png'
queueUrl = 'https://www.baidu.com'
option1_Endtime = datetime.datetime(2021, 12, 5, 23, 50, 0).replace(microsecond=0)
option2_Endtime = datetime.datetime(2022, 12, 5, 23, 55, 0).replace(microsecond=0)

def openQueueUrl():
    print("Open Queue URL")
    for pos in pyautogui.locateAllOnScreen(freshPic):
        point = pyautogui.center(pos)
        pyautogui.moveTo(point.x + 200, point.y, 2)
        pyautogui.click()
        pyautogui.write(queueUrl, interval=0.01)
        pyautogui.press('enter')

if __name__ == "__main__":
    now = datetime.datetime.now().replace(microsecond=0)

    while option1_Endtime > now:
        diff = option1_Endtime - now
        print(diff, end = '\r')
        now = datetime.datetime.now().replace(microsecond=0)
        time.sleep(1)
    openQueueUrl()

    while option2_Endtime > now:
        diff = option2_Endtime - now
        print(diff, end = '\r')
        now = datetime.datetime.now().replace(microsecond=0)
        time.sleep(1)
    openQueueUrl()
