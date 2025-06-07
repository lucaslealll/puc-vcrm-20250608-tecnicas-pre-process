import sys
from components import *


def path_imagem(prompt, default_path="./src/02.jpeg"):
    """
    Solicita ao usuário um caminho de imagem e retorna-o.
    Se o usuário não fornecer um caminho, um caminho padrão é usado.

    Args:
        prompt (str): A mensagem a ser exibida para o usuário.
        default_path (str): O caminho padrão da imagem a ser usado se nenhum for fornecido.

    Returns:
        str: O caminho da imagem escolhido ou padrão.
    """
    caminho = input(prompt).strip()  # Pede ao usuário para digitar o caminho da imagem e remove espaços em branco.
    if caminho == "":  # Verifica se o usuário não digitou nada.
        print(f"  ⤷ Nenhum caminho fornecido. Usando caminho padrão: {default_path}")
        return default_path  # Retorna o caminho padrão.
    return caminho  # Retorna o caminho fornecido pelo usuário.


def menu():
    """
    Exibe um menu de opções para o usuário e executa a função correspondente à escolha.
    Continua exibindo o menu até que o usuário escolha sair.
    """
    while True:
        clear_t()  # Limpa o terminal a cada exibição do menu.

        print("=" * 31)
        print("🖼️  PROCESSAMENTO DE IMAGENS  🖼️")
        print("=" * 31)
        print("📤  [0] Sair\n")

        print("🎨 PRÉ-PROCESSAMENTO")
        print("   [1] Clusterização de Tons de Cinza")
        print("   [2] Subtração e Delineamento")

        print("🔍 FILTROS")
        print("   [3.1] Filtro High-Boost")
        print("   [3.2] Filtro Passa-Alta")
        print("   [3]   Comparar Resultados de 3.1 e 3.2")

        print("📊 ANÁLISE DE DESEMPENHO")
        print("   [4] Comparar Convolução Espacial vs Frequencial")
        print("=" * 31)

        opcao = input("👉 Escolha uma opção: ").strip()

        if opcao == "1":
            img_path = path_imagem("  ⤷ Caminho da imagem (pressione Enter para padrão): ")
            resultado = _01_clusterizacao_tons_cinza(img_path)
            mostrar_imagem("./out/01_clusterizada.jpg")

        elif opcao == "2":
            bg_path = input("  ⤷ Caminho da imagem de fundo (pressione Enter para padrão): ").strip()
            bg_path = "./src/01.jpeg" if bg_path == "" else bg_path

            fg_path = input("  ⤷ Caminho da imagem com pessoa (pressione Enter para padrão): ").strip()
            fg_path = "./src/02.jpeg" if fg_path == "" else fg_path

            try:
                limiar = int(input("  ⤷ Digite o limiar (ex: 30): "))
            except ValueError:
                print("  ⤷ Limiar inválido. Usando valor padrão 30.")
                limiar = 30

            _, img_contorno = _02_subtrai_e_delineia(bg_path, fg_path, limiar)
            mostrar_imagem("./out/02_com_contorno.jpg")
            mostrar_imagem("./out/02_subtracao_binaria.jpg")

        elif opcao == "3":
            relatorio = _03_comparar_imagens(
                "./out/03_high_boost.jpg",
                "./out/03_passa_alta.jpg",
            )
            for k, v in relatorio.items():
                print(f"{k}: {v}")
            input("\nPressione Enter para voltar ao menu...")

        elif opcao == "3.1":
            img_path = path_imagem("  ⤷ Caminho da imagem (pressione Enter para padrão): ")
            try:
                A = float(input("  ⤷ Digite o valor de A (ex: 1.5): "))
            except ValueError:
                print("  ⤷ Valor inválido para A. Usando valor padrão 1.5.")
                A = 1.5
            resultado = _03_1_filtro_high_boost(img_path, A)
            mostrar_imagem("./out/03_high_boost.jpg")

        elif opcao == "3.2":
            img_path = path_imagem("  ⤷ Caminho da imagem (pressione Enter para padrão): ")
            resultado = _03_2_filtro_passa_alta(img_path)
            mostrar_imagem("./out/03_passa_alta.jpg")

        elif opcao == "4":
            img_path = path_imagem("  ⤷ Caminho da imagem (pressione Enter para padrão): ")
            _04_comparar_tempos_convolucao(img_path)

        elif opcao == "0":
            print("👋 Saindo...")
            sys.exit()

        else:
            print("🚫 Opção inválida!")
            input("Pressione Enter para tentar novamente...")

# Este bloco de código é executado apenas quando o script é executado diretamente (não quando importado como módulo).
if __name__ == "__main__":
    menu()  # Chama a função do menu para iniciar a aplicação.
    # clear_t()
