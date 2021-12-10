import pyautogui
import datetime
import time

freshPic = 'detectpic/fresh.png'
queueUrl_1 = 'https://coinlist.co/queue/enter_queue/pstake'
option1_Endtime = datetime.datetime(2021, 12, 16, 1, 0, 0).replace(microsecond=0)

queueUrl_2 = 'https://www.baidu.com'
option2_Endtime = datetime.datetime(2022, 12, 5, 23, 55, 0).replace(microsecond=0)

def openQueueUrl(URL):
    print(URL)
    for pos in pyautogui.locateAllOnScreen(freshPic):
        point = pyautogui.center(pos)
        pyautogui.moveTo(point.x + 200, point.y, 2)
        pyautogui.click()
        pyautogui.write(URL, interval=0.01)
        pyautogui.press('enter')

if __name__ == "__main__":
    now = datetime.datetime.now().replace(microsecond=0)

    while option1_Endtime > now:
        diff = option1_Endtime - now
        print(queueUrl_1, "( Time Left:", diff, ")", end = '\r')
        now = datetime.datetime.now().replace(microsecond=0)
        time.sleep(1)
    openQueueUrl(queueUrl_1)

    while option2_Endtime > now:
        diff = option2_Endtime - now
        print(queueUrl_2, diff, end = '\r')
        now = datetime.datetime.now().replace(microsecond=0)
        time.sleep(1)
    openQueueUrl(queueUrl_2)
