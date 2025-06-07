import os
from PIL import Image

def mostrar_imagem(path):
    img = Image.open(path)
    img.show()


def clear_t():
    # Verifica o sistema operacional
    if os.name == 'nt':  # 'nt' é para Windows
        _ = os.system('cls')
    else:  # 'posix' é para Linux e macOS
        _ = os.system('clear')
