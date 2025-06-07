import cv2
import numpy as np
import matplotlib.pyplot as plt


def _03_1_filtro_high_boost(img_path, A=1.5):
    """
    Aplica o filtro high-boost a uma imagem.

    O filtro high-boost realça as bordas e os detalhes de uma imagem,
    sendo uma generalização do filtro passa-alta. Ele é calculado subtraindo
    uma versão borrada da imagem original (máscara de nitidez) e, em seguida,
    adicionando essa máscara de volta à imagem original com um peso 'A' para
    controlar a intensidade do realce.

    Args:
        img_path (str): O caminho para a imagem de entrada.
        A (float, optional): O fator de amplificação para a máscara de nitidez.
                             Valores maiores que 1 aumentam o realce. O padrão é 1.5.

    Returns:
        numpy.ndarray: A imagem resultante com o filtro high-boost aplicado.
    """
    img = cv2.imread(img_path)  # Carrega a imagem do caminho especificado
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converte a imagem para tons de cinza

    # Aplica um desfoque Gaussiano à imagem em tons de cinza.
    # Isso cria uma versão "borrada" da imagem, que será usada para criar a máscara.
    # O tamanho do kernel (5, 5) define o nível de desfoque.
    blur = cv2.GaussianBlur(img_gray, (5, 5), 0)

    # Calcula a máscara de nitidez subtraindo a imagem borrada da imagem original em tons de cinza.
    # Essa máscara contém as informações de alta frequência (bordas e detalhes).
    mask = cv2.subtract(img_gray, blur)

    # Aplica o filtro high-boost.
    # cv2.addWeighted combina duas imagens linearmente:
    # img_gray * A + mask * 1 + 0
    # O parâmetro 'A' controla a intensidade do realce da máscara.
    high_boost = cv2.addWeighted(img_gray, A, mask, 1, 0)

    output_path = "out/03_high_boost.jpg"  # Define o caminho de saída para a imagem processada
    cv2.imwrite(output_path, high_boost)  # Salva a imagem high-boost no caminho especificado
    print(f"    Imagem High-Boost salva em {output_path}")  # Imprime uma mensagem de confirmação
    return high_boost  # Retorna a imagem com o filtro high-boost aplicado


def _03_2_filtro_passa_alta(img_path):
    """
    Aplica o filtro passa-alta a uma imagem usando um kernel Laplaciano.

    O filtro passa-alta é usado para realçar as bordas e os detalhes de uma imagem,
    tornando as transições de intensidade mais pronunciadas. Ele funciona detectando
    mudanças rápidas nos valores de pixel.

    Args:
        img_path (str): O caminho para a imagem de entrada.

    Returns:
        numpy.ndarray: A imagem resultante com o filtro passa-alta aplicado.
    """
    img = cv2.imread(img_path)  # Carrega a imagem do caminho especificado
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converte a imagem para tons de cinza

    # Define um kernel Laplaciano.
    # Este kernel é comumente usado para detecção de bordas e realce de detalhes.
    # O valor central positivo e os valores negativos ao redor realçam as mudanças de intensidade.
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])

    # Aplica o filtro 2D (convolução) à imagem em tons de cinza usando o kernel Laplaciano.
    # O parâmetro -1 indica que a profundidade da imagem de saída será a mesma da imagem de entrada.
    passa_alta = cv2.filter2D(img_gray, -1, kernel)

    output_path = "out/03_passa_alta.jpg"  # Define o caminho de saída para a imagem processada
    cv2.imwrite(output_path, passa_alta)  # Salva a imagem passa-alta no caminho especificado
    print(f"    Imagem Passa-Alta salva em {output_path}")  # Imprime uma mensagem de confirmação
    return passa_alta  # Retorna a imagem com o filtro passa-alta aplicado
