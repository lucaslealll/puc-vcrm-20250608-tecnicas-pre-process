import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from PIL import Image, ImageChops
import os


# 1) Em relação a técnica de transformação de tons de cinza baseado em clusterização, converta uma
# imagem colorida para tons de cinza e agrupe os tons de cinza a cada 4 grupos. Para exemplificar,
# dada uma imagem com 256 tons de cinza, aplicando agrupamento a cada 4 tons de cinza, a imagem
# resultante terá no máximo 64 tons de cinza.
def _01_clusterizacao_tons_cinza(img_path, qtd_grupo=4):
    """
    Converte uma imagem colorida para tons de cinza e agrupa os tons de cinza
    em clusters, reduzindo o número total de tons possíveis.

    Esta técnica é baseada na quantização de cores, onde os 256 tons de cinza
    originais são mapeados para um número menor de grupos.

    Args:
        img_path (str): O caminho para a imagem colorida de entrada.
        grupo (int, optional): O tamanho de cada grupo de tons de cinza.
                               Por exemplo, se 'grupo' for 4, os tons de cinza
                               serão agrupados a cada 4 valores (0-3, 4-7, etc.),
                               resultando em no máximo 256/4 = 64 tons diferentes.
                               Padrão é 4.

    Returns:
        numpy.ndarray: A imagem resultante em tons de cinza com o histograma clusterizado.
                       Os valores dos pixels estarão dentro da faixa [0, 255].
    """
    img = cv2.imread(img_path)

    # Verifica se a imagem foi carregada corretamente
    if img is None:
        raise FileNotFoundError(f"Não foi possível carregar a imagem em: {img_path}")

    # Converte a imagem para tons de cinza
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Calcula o fator de agrupamento
    # Por exemplo, se grupo=4, fator = 256 // 4 = 64
    # Isso significa que cada 64 tons de cinza originais serão mapeados para um único valor.
    fator = 256 // qtd_grupo

    # Realiza a clusterização dos tons de cinza
    # Primeiro, divide o valor do pixel pelo fator (ex: 100 // 64 = 1)
    # Depois, multiplica pelo fator novamente (ex: 1 * 64 = 64)
    # Isso mapeia todos os pixels dentro de um grupo para o valor inicial desse grupo.
    img_cluster = (img_gray // fator) * fator

    # Garante que os valores dos pixels estejam dentro do intervalo [0, 255] e sejam do tipo uint8
    img_cluster = np.clip(img_cluster, 0, 255).astype(np.uint8)

    output_path = "out/01_clusterizada.jpg"
    # Salva a imagem clusterizada
    cv2.imwrite(output_path, img_cluster)
    print(f"  ⤷ Imagem clusterizada salva em {output_path}")

    return img_cluster


def _02_subtrai_e_delineia(bg_path, fg_path, limiar=50):
    """
    Realiza a subtração de fundo para realçar a área de um objeto (corpo humano)
    em uma imagem, binariza o resultado e plota um retângulo delimitador vermelho
    em torno da área detectada.

    Args:
        bg_path (str): O caminho para a imagem de fundo (apenas o cenário/parede).
        fg_path (str): O caminho para a imagem de primeiro plano (com o objeto/corpo).
        limiar (int, optional): O valor de limiar a ser usado na binarização do
                                resultado da subtração. Pixels com diferença de intensidade
                                acima deste limiar serão considerados parte do objeto.
                                Valores típicos variam de 30 a 80. Padrão é 50.

    Returns:
        tuple: Uma tupla contendo:
            - numpy.ndarray: A imagem binarizada resultante da subtração, onde o objeto
                             é branco (255) e o fundo é preto (0).
            - numpy.ndarray: A imagem de primeiro plano original com um retângulo vermelho
                             desenhado ao redor da área detectada do objeto.

    Raises:
        FileNotFoundError: Se alguma das imagens de entrada não puder ser carregada.

    Pré-requisitos:
        - As duas imagens devem ser capturadas com a câmera em uma posição fixa,
          focando no mesmo cenário.
        - A imagem de fundo deve conter apenas o cenário, sem o objeto.
        - A imagem de primeiro plano deve conter o objeto no mesmo cenário.
        - Ambas as imagens são convertidas para tons de cinza antes da subtração.
    """
    # Carrega as imagens de fundo e primeiro plano
    img_bg = cv2.imread(bg_path)
    img_fg = cv2.imread(fg_path)

    # Verifica se as imagens foram carregadas corretamente
    if img_bg is None:
        raise FileNotFoundError(f"  ⤷ Não foi possível carregar a imagem de fundo em: {bg_path}")
    if img_fg is None:
        raise FileNotFoundError(f"  ⤷ Não foi possível carregar a imagem de primeiro plano em: {fg_path}")

    # Converte ambas as imagens para tons de cinza
    bg_gray = cv2.cvtColor(img_bg, cv2.COLOR_BGR2GRAY)
    fg_gray = cv2.cvtColor(img_fg, cv2.COLOR_BGR2GRAY)

    # Calcula a diferença absoluta entre as imagens em tons de cinza
    # Isso realça as áreas onde houve mudança (onde o corpo está)
    subtracao = cv2.absdiff(fg_gray, bg_gray)

    # Binariza a imagem de diferença usando o limiar especificado.
    # Pixels com diferença > limiar se tornam 255 (branco), outros 0 (preto).
    _, binaria = cv2.threshold(subtracao, limiar, 255, cv2.THRESH_BINARY)

    # Encontra os contornos na imagem binarizada.
    # cv2.RETR_EXTERNAL: Recupera apenas os contornos externos.
    # cv2.CHAIN_APPROX_SIMPLE: Compacta segmentos horizontais, verticais e diagonais,
    #                         deixando apenas os pontos finais.
    contours, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Cria uma cópia da imagem de primeiro plano para desenhar os contornos
    img_fg_contorno = img_fg.copy()

    # Itera sobre os contornos encontrados
    for cnt in contours:
        # Calcula o retângulo delimitador (bounding box) para cada contorno
        x, y, w, h = cv2.boundingRect(cnt)
        # Desenha um retângulo vermelho (0, 0, 255) com espessura 2 na imagem de primeiro plano
        cv2.rectangle(img_fg_contorno, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Salva as imagens resultantes
    output_binaria_path = "out/02_subtracao_binaria.jpg"
    output_contorno_path = "out/02_com_contorno.jpg"
    cv2.imwrite(output_binaria_path, binaria)
    cv2.imwrite(output_contorno_path, img_fg_contorno)
    print(f"  ⤷ Imagem binarizada salva em {output_binaria_path}")
    print(f"  ⤷ Imagem com contorno salva em {output_contorno_path}")

    return binaria, img_fg_contorno


def convolucao_espacial(img, kernel):
    """
    Aplica uma operação de convolução espacial a uma imagem usando um kernel (filtro).

    A convolução espacial é uma operação fundamental no processamento de imagens
    usada para diversas finalidades, como suavização, realce de bordas, nitidez,
    e detecção de características, aplicando um filtro (kernel) sobre cada pixel
    da imagem.

    Args:
        img (numpy.ndarray): A imagem de entrada à qual o kernel será aplicado.
                             Pode ser uma imagem em tons de cinza ou colorida.
        kernel (numpy.ndarray): A matriz (kernel) que define o filtro a ser aplicado.
                                O kernel é geralmente uma matriz pequena (ex: 3x3, 5x5)
                                de números que multiplicam os valores dos pixels vizinhos.

    Returns:
        numpy.ndarray: A imagem resultante após a aplicação da convolução.
                       Terá o mesmo tipo e número de canais da imagem de entrada.

    Exemplos de kernels:
        - Kernel de média (suavização): np.ones((3,3), np.float32)/9
        - Kernel de detecção de bordas (Laplaciano): np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
        - Kernel de nitidez: np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    """
    # cv2.filter2D é a função do OpenCV para aplicar filtros convolucionais.
    # img: A imagem de entrada.
    # ddepth: Profundidade de bits da imagem de saída. -1 significa que a saída terá a mesma profundidade
    #         da imagem de origem. É comum usar -1 para manter o tipo de dados original (ex: uint8 para imagens de 0-255).
    # kernel: A matriz do filtro (kernel) a ser aplicada.
    return cv2.filter2D(img, -1, kernel)


def convolucao_frequencia(img, kernel):
    """
    Aplica uma operação de convolução a uma imagem no domínio da frequência
    usando a Transformada Rápida de Fourier (FFT).

    Esta técnica é uma alternativa à convolução espacial, sendo computacionalmente
    mais eficiente para kernels maiores ou em certas aplicações. A convolução no
    domínio espacial é equivalente à multiplicação no domínio da frequência.

    Args:
        img (numpy.ndarray): A imagem de entrada (preferencialmente em tons de cinza)
                             para a qual o filtro será aplicado. Os valores devem ser
                             do tipo float32 para a FFT.
        kernel (numpy.ndarray): O kernel (filtro) a ser aplicado. Deve ser uma matriz
                                numpy.ndarray.

    Returns:
        numpy.ndarray: A imagem resultante após a convolução no domínio da frequência.
                       A imagem resultante terá o mesmo formato e tipo de dados da imagem
                       original (se ajustado após a recuperação).

    Passos da Convolução no Domínio da Frequência:
    1.  **Padding Otimizado:** A imagem e o kernel são expandidos (padded) para um tamanho
        ótimo para a DFT (Discrete Fourier Transform), que geralmente são potências de 2
        e garantem eficiência computacional. Isso também ajuda a evitar efeitos de
        "wrap-around" na convolução.
    2.  **DFT da Imagem:** A Transformada Discreta de Fourier é aplicada à imagem padded
        para convertê-la para o domínio da frequência.
    3.  **DFT do Kernel:** O kernel também é expandido para o mesmo tamanho da imagem padded
        e sua DFT é calculada. É importante que o kernel esteja centralizado no padding.
    4.  **Multiplicação no Domínio da Frequência:** As Transformadas de Fourier da imagem
        e do kernel são multiplicadas elemento a elemento. Esta é a operação equivalente
        à convolução no domínio espacial.
    5.  **IDFT Inversa:** A Transformada Discreta de Fourier Inversa (IDFT) é aplicada ao
        resultado da multiplicação para converter a imagem de volta para o domínio espacial.
    6.  **Corte e Normalização:** A parte relevante da imagem (sem o padding) é extraída,
        e os valores podem ser normalizados ou convertidos para o tipo de dados desejado
        (ex: `uint8` para exibição de imagem).
    """
    # 1. Obter o tamanho ótimo para a DFT e aplicar padding à imagem
    # getOptimalDFTSize retorna o tamanho de array que é o mais eficiente para DFT
    dft_size = (cv2.getOptimalDFTSize(img.shape[0]), cv2.getOptimalDFTSize(img.shape[1]))

    # Cria uma nova matriz de zeros com o tamanho ótimo para padding
    img_padded = np.zeros(dft_size, dtype=np.float32)
    # Copia a imagem original para o canto superior esquerdo da matriz padded
    img_padded[: img.shape[0], : img.shape[1]] = img

    # 2. Aplicar padding ao kernel para que tenha o mesmo tamanho que a imagem padded
    kernel_padded = np.zeros_like(img_padded)
    k_h, k_w = kernel.shape
    # Centraliza o kernel no canto superior esquerdo do padding (ou pode ser centralizado na imagem, mas aqui é simples)
    kernel_padded[:k_h, :k_w] = kernel

    # 3. Calcular a DFT (Transformada de Fourier) da imagem e do kernel
    img_dft = np.fft.fft2(img_padded)
    kernel_dft = np.fft.fft2(kernel_padded)

    # 4. Multiplicação no domínio da frequência
    result_dft = img_dft * kernel_dft

    # 5. Calcular a IDFT (Transformada de Fourier Inversa) e pegar a parte real
    # A IDFT pode retornar valores complexos, mas a parte real é a imagem de interesse.
    result = np.fft.ifft2(result_dft).real

    # 6. Remover o padding extra para retornar a imagem ao seu tamanho original
    return result[: img.shape[0], : img.shape[1]]


# 4) Implemente um programa que demonstre o ganho computacional obtido à partir da aplicação do
# conceito que envolve o Teorema da Convolução. O programa deverá exibir o tempo que a operação
# levou para ser aplicada à imagem usando o operador de convolução e exibir o tempo que aplicação
# do filtro levou para ser aplicada no contexto do domínio da frequência. Analise e teça comentários
# sobre os tempos obtidos.
def _04_comparar_tempos_convolucao(img_path):
    """
    Demonstra e compara o desempenho computacional da convolução espacial
    versus a convolução no domínio da frequência (usando FFT) para um filtro.

    O Teorema da Convolução estabelece que a convolução no domínio espacial
    é equivalente à multiplicação no domínio da frequência. Para kernels grandes,
    a convolução no domínio da frequência (que envolve FFT, multiplicação e IFFT)
    pode ser significativamente mais rápida do que a convolução direta no domínio espacial.

    Args:
        img_path (str): O caminho para a imagem de entrada (será convertida para tons de cinza).

    Returns:
        None: A função imprime os tempos de execução no console e tece comentários.

    Raises:
        FileNotFoundError: Se a imagem de entrada não puder ser carregada.
    """
    # Carrega a imagem em tons de cinza
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # Verifica se a imagem foi carregada corretamente
    if img is None:
        raise FileNotFoundError(f"  ⤷ Não foi possível carregar a imagem em: {img_path}")

    # Define um kernel de exemplo (filtro de média 5x5)
    # Um kernel maior geralmente mostra melhor o ganho da frequência
    kernel = np.ones((5, 5), np.float32) / 25

    # --- Medição de Tempo para Convolução Espacial ---
    start = time.time()
    # Chama a função de convolução espacial (internamente usa cv2.filter2D)
    _ = convolucao_espacial(img, kernel)
    tempo_espacial = time.time() - start

    # --- Medição de Tempo para Convolução no Domínio da Frequência ---
    # Para a convolução de frequência, é importante que a imagem esteja em float32
    # e que o kernel seja passado corretamente (já tratado dentro da função convolucao_frequencia)
    start = time.time()
    _ = convolucao_frequencia(img, kernel)
    tempo_freq = time.time() - start

    print(f"  ⤷ Tempo Convolução Espacial: {tempo_espacial:.6f} segundos")
    print(f"  ⤷ Tempo Convolução Frequencial: {tempo_freq:.6f} segundos")
    input("*press enter")


def _03_comparar_imagens(img_path1, img_path2):
    """
    Compara duas imagens e gera um relatório técnico detalhado sobre as diferenças.

    Parâmetros:
    - img_path1: caminho da primeira imagem
    - img_path2: caminho da segunda imagem
    - salvar_diff: caminho para salvar a imagem de diferenças

    Retorna:
    - Um dicionário com métricas técnicas da comparação.
    """
    # Carregar imagens e garantir RGB
    img1 = Image.open(img_path1).convert("RGB")
    img2 = Image.open(img_path2).convert("RGB")

    # Verificar tamanho
    if img1.size != img2.size:
        return {
            "iguais": False,
            "mensagem": "As imagens têm tamanhos diferentes.",
            "tamanho_img1": img1.size,
            "tamanho_img2": img2.size,
        }

    # Calcular diferença
    diff = ImageChops.difference(img1, img2)

    # Obter bounding box da diferença
    bbox = diff.getbbox()

    # Converter para numpy para análise de pixel
    diff_np = np.array(diff)
    total_pixels = diff_np.shape[0] * diff_np.shape[1]

    # Pixel é diferente se houver qualquer canal (R, G, B) não nulo
    mask = np.any(diff_np != 0, axis=-1)
    num_pixels_diferentes = np.count_nonzero(mask)
    percentual_diferenca = (num_pixels_diferentes / total_pixels) * 100

    # if bbox:
    #     diff.save(salvar_diff)

    return {
        " ⤷ iguais": num_pixels_diferentes == 0,
        " ⤷ mensagem": "Imagens idênticas." if num_pixels_diferentes == 0 else "Diferenças detectadas.",
        " ⤷ pixels_totais": total_pixels,
        " ⤷ pixels_diferentes": num_pixels_diferentes,
        " ⤷ percentual_diferenca": round(percentual_diferenca, 4),
        " ⤷ bounding_box_diferenca": bbox,
        # " ⤷ imagem_diferenca": salvar_diff if bbox else None,
    }
