import os

def temp():
    os.makedirs('temp/captcha', exist_ok=True)
    os.makedirs('temp/messages', exist_ok=True)
