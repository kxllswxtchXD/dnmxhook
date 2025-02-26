from PIL import Image

def solver(image_path):
    try:
        image = Image.open(image_path).convert('L')
        image = image.point(lambda x: 0 if x < 140 else 255)
        return image
    except Exception as e:
        print(f"Erro ao processar o captcha: {e}")
        return None