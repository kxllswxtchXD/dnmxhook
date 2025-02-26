import os
import shutil

def cleanup():
    if os.path.exists('temp/captcha'):
        shutil.rmtree('temp/captcha')
    if os.path.exists('temp/messages'):
        shutil.rmtree('temp/messages')