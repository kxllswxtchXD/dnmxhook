import colorama
import time
import sys
import re
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.functions.content import content
from modules.functions.discord import discord

def messages(page):
    page.reload()
    page.wait_for_timeout(3000)
    page.wait_for_selector('tbody', timeout=10000)
    page_html = page.content()
    existing_message_links = re.findall(r'href="read_body\.php\?mailbox=INBOX&amp;passed_id=(\d+)', page_html)
    last_message_ids = set(existing_message_links)

    while True:
        try:
            page.reload()
            page.wait_for_timeout(3000)
            page.wait_for_selector('tbody', timeout=10000)
            
            page_html = page.content()
            message_links = re.findall(r'href="read_body\.php\?mailbox=INBOX&amp;passed_id=(\d+)', page_html)
            
            if message_links:
                new_message_ids = set(message_links)
                current_new_ids = new_message_ids - last_message_ids

                if current_new_ids:
                    for message_id in current_new_ids:
                        message_url = f'https://dnmx.su/webmail/src/printer_friendly_bottom.php?passed_ent_id=0&mailbox=INBOX&passed_id={message_id}&view_unsafe_images='
                        page.goto(message_url)
                        subject, date, to, pre_content = content(page)
                        if pre_content:
                            subject_display = subject if subject else "Sem Título"
                            print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.WHITE}] Nova mensagem recebida: {subject_display}")
                            discord(subject, date, to, pre_content, message_id)
                            print(f"[{colorama.Fore.GREEN}✓{colorama.Fore.WHITE}] Mensagem enviada no Discord\n")
                    last_message_ids = new_message_ids
                    print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.WHITE}] Aguardando novas mensagens...\n")
                else:
                    pass
            else:
                pass

        except Exception as e:
            print(f"Erro ao verificar mensagens: {e}")
            continue

        time.sleep(3)
