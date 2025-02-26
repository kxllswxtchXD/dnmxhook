import requests

def upload(file_path):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post('https://oshi.at', files=files, data={'expire': '30d'})
            if response.status_code == 200:
                return {
                    'download_url': response.text.split('\n')[0].strip(),
                    'management_url': response.text.split('\n')[1].strip()
                }
            else:
                print(f"Erro ao fazer upload no oshi.at: {response.status_code} - {response.text}")
                return None
    except Exception as e:
        print(f"Erro ao fazer upload no oshi.at: {e}")
        return None
