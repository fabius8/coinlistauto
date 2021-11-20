# coinlistauto
coinlist 自动登录器

https://github.com/git-for-windows/git/releases/download/v2.33.0.windows.2/Git-2.33.0.2-64-bit.exe

安装python和tesseract

https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe

安装python时添加PATH勾上

https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20210811.exe

安装完，添加系统环境变量。
`C:\Program Files\Tesseract-OCR`

`py -m pip install -r requirements.txt`

使用方法：
1. OTP json文件准备好
2. 打开chrome
3. 运行clauto.py


题外话：
```
关闭windows更新
sconfig, 选择5，选择m，关闭windows server自动更新

关闭windows defender
1. gpedit.msc，
2. 打开组策略 依次展开“计算机配置->管理模板->Windows组件”
3. 在“Windows Defender”右侧找到“关闭Windows Defender”
4. 改成“启用”
```
