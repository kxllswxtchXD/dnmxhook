import os
import shutil

def captcha():
    if os.path.exists('temp/captcha'):
        shutil.rmtree('temp/captcha')