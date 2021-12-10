import pyperclip
import time
import pyotp
import json

secretjson = json.load(open('secret.json'))

last_string = pyperclip.paste()
while True:
    # 检测频率
    time.sleep(2)
    string = pyperclip.paste()#读取剪切板内容
    if "@" in string:
        for i in secretjson:
            if i["Username"] in string and "CoinList" in i["Issuer"]:
                print(i["Issuer"])
                totp = pyotp.TOTP(i["Secret"])
                print(string, "[", i["Username"], totp.now(), "]")
                pyperclip.copy(totp.now()) #重新写入剪切板
