import pytesseract
import colorama
import time
import uuid
import sys
import os

from playwright.sync_api import sync_playwright

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.functions.config import load_config
from modules.functions.messages import messages
from modules.functions.captcha import captcha
from modules.functions.solver import solver
from modules.functions.date import date

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

config = load_config()

if config:
    username = config['username']
    password = config['password']
else:
    print("Não foi possível carregar as credenciais!")
    time.sleep(3)
    exit()

def login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        page.goto('https://dnmx.su/')

        page.fill('input[name="login_username"]', username)
        page.fill('input[name="secretkey"]', password)

        try:
            captcha_image_element = page.query_selector('img[src*="captcha.php"]')
            if captcha_image_element:
                captcha_image_bytes = captcha_image_element.screenshot()
                captcha_filename = f"temp/captcha/{uuid.uuid4()}.png"
                with open(captcha_filename, 'wb') as f:
                    f.write(captcha_image_bytes)

                captcha_image = solver(captcha_filename)
                if captcha_image:
                    captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 6').strip()
                    page.fill('input[name="captcha"]', captcha_text)
        except Exception as e:
            print(f"Erro ao processar o captcha: {e}")

        page.wait_for_timeout(1000)
        page.click('button[name="action"][value="login"]')
        page.wait_for_load_state("domcontentloaded")

        if "login" in page.url:
            print("Login falhou! Verifique suas credenciais.")
            browser.close()
            return

        print(f"[{colorama.Fore.GREEN}✓{colorama.Fore.WHITE}] Sessão iniciada: {date()}")
        print(f"[{colorama.Fore.GREEN}✓{colorama.Fore.WHITE}] Usuário: {username}\n\n")

        print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.WHITE}] Aguardando novas mensagens...\n")    

        captcha()

        page.goto('https://dnmx.su/webmail/src/right_main.php')
        messages(page)
        browser.close()