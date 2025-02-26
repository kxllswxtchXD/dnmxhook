import yaml
import os

def load_config():
    try:
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        path = os.path.join(root, 'config.yml')
        
        with open(path, 'r') as file:
            config_dict = yaml.safe_load(file)
            return config_dict
    except FileNotFoundError:
        print("Arquivo config.yml não encontrado!")
        return None
    except yaml.YAMLError as e:
        print(f"Erro ao ler o arquivo YAML: {e}")
        return None