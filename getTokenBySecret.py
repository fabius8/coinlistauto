import pyperclip
import time
import pyotp
import json

last_string = pyperclip.paste()
while True:
    # 检测频率
    time.sleep(1)
    string = pyperclip.paste()#读取剪切板内容
    time.sleep(1)
    try:
        totp = pyotp.TOTP(string)
        print(string, "[", totp.now(), "]")
        pyperclip.copy(totp.now()) #重新写入剪切板
    except:
        pass