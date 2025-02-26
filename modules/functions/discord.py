import requests
import shutil
import time
import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.functions.config import load_config
from modules.functions.upload import upload

config = load_config()

if config:
    webhook = config['webhook']
else:
    print("Não foi possível carregar as credenciais!")
    time.sleep(3)
    exit()

def discord(subject, date, to, pre_content, message_id):
    try:
        if len(pre_content) > 512:
            message_folder = f"temp/messages/message_{message_id}"
            os.makedirs(message_folder, exist_ok=True)

            txt_filename = f"{message_folder}/{uuid.uuid4()}.txt"
            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write(pre_content)

            upload_response = upload(txt_filename)
            if upload_response:
                download_url = upload_response['download_url']
                management_url = upload_response['management_url']

                message = {
                    "username": "dnmx.su",
                    "avatar_url": "https://i.imgur.com/7ngnBBB.png",
                    "embeds": [
                        {
                            "title": subject[:256],
                            "description": f"O conteúdo da mensagem é muito grande, acesse os links abaixo para visualizar e gerenciar a mensagem.\n\nLink da mensagem: \n{management_url}\n\nLink de gerenciamento: {management_url}",
                            "fields": [
                                {"name": "Data", "value": date[:1024], "inline": True},
                                {"name": "Para", "value": to[:1024], "inline": True}
                            ]
                        }
                    ]
                }
            else:
                print("Erro ao fazer upload do arquivo no oshi.at.")
                return
        else:
            message = {
                "username": "dnmx.su",
                "avatar_url": "https://i.imgur.com/7ngnBBB.png",
                "embeds": [
                    {
                        "title": subject[:256],
                        "description": pre_content[:512],
                        "fields": [
                            {"name": "Data", "value": date[:1024], "inline": True},
                            {"name": "Para", "value": to[:1024], "inline": True}
                        ]
                    }
                ]
            }

        response = requests.post(webhook, json=message)
        if response.status_code != 200 and response.status_code != 204:
            print(f"Erro ao enviar para o Discord: {response.status_code} - {response.text}")

        message_folder = f"temp/messages/message_{message_id}"
        if os.path.exists(message_folder):
            shutil.rmtree(message_folder)
    except Exception as e:
        print(f"Erro ao enviar para o Discord: {e}")
