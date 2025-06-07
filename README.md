# **VISÃO COMPUTACIONAL E REALIDADE MISTURADA**
## ATIVIDADE 2 - IMPLEMENTAÇÃO DE TÉCNICAS DE PRÉ-PROCESSAMENTO

Descrição da atividade: [pdf](./2025-s1_%20Tarefa%20Avaliativa%201%20-%20PARTE%202%20-%20Implementação%20de%20técnicas%20de%20pré-processamento.pdf)

## **Funcionalidades**

### **1. Clusterização de Tons de Cinza**

- Converte uma imagem colorida para tons de cinza.
- Agrupa os tons de cinza a cada 4 grupos.
- Por exemplo, uma imagem com 256 tons passa a ter no máximo 64 tons de cinza.

  > **Exemplo de uso:**
  > - No menu, selecione a opção **1**.
  > - Informe o caminho da imagem desejada.

---

### **2. Subtração de Imagens e Delineamento do Corpo**

- A partir de 2 imagens:
  1. **Background**
  2. **Foreground**
- O programa:
  - Converte ambas as imagens para tons de cinza.
  - Aplica subtração entre elas.
  - Binariza com limiar empiricamente escolhido.
  - Identifica contornos e desenha um **retângulo vermelho** onde o corpo foi detectado.

  > **Exemplo de uso:**
  > - No menu, selecione a opção **2**.
  > - Informe o caminho das duas imagens e o valor de limiar sugerido (exemplo: 30 ou 50).

---

### **3.1. Filtro High-Boost**

- Implementação própria do filtro **high-boost**.
- Comparação com o **filtro passa-alta**.
- Salva o resultado da imagem realçada.

  > **Exemplo de uso:**
  > - No menu, selecione a opção **3.1**.
  > - Informe o caminho da imagem.
  > - Digite o valor de A (sugestão: 1.5 ou 2.0).

---

### **3.2. Filtro Passa-Alta**

- Aplica um filtro passa-alta clássico (máscara Laplaciana).
- Realça bordas e detalhes da imagem.

  > **Exemplo de uso:**
  > - No menu, selecione a opção **3.2**.
  > - Informe o caminho da imagem.

---

### **4. Comparação de Desempenho: Convolução Espacial x Frequencial**

- Aplica uma convolução espacial (via máscara 5x5).
- Aplica a mesma operação via domínio da **frequência** (FFT).
- Exibe os **tempos de execução** de cada abordagem.

  > **Exemplo de uso:**
  > - No menu, selecione a opção **4**.
  > - Informe o caminho da imagem.

## **Estrutura do Projeto**

```sh
.
├── components
│   ├── filtros.py          # Filtros de imagem: high-boost, passa-alta
│   ├── __init__.py         # Inicializa o diretório 'components' como um pacote Python e exporta funções
│   ├── processamento.py    # Clusterização, subtração, convolução
│   └── utils.py            # Contém funções utilitárias diversas, como para exibir imagens
├── out             # Pasta para salvar imagens resultantes
├── main.py                 # Script principal para executar as operações de processamento de imagem
├── requirements.txt        # Lista as dependências
└── src                     # Armazenar as imagens de origem (input)
```


## **Como Executar o Projeto**

1. **Pré-requisitos:**
- Python 3.12
- Bibliotecas: `opencv-python`, `numpy`, `matplotlib`

**Instalar dependências:**

```bash
pip install -r requirements
```

2. **Coloque as imagens de entrada na pasta:**
    ```
    src/
    ```


3. **Execute o programa principal:**
    ```bash
    python main.py
    ```


4. **Siga as instruções do menu interativo:**


## **Saída**
- As imagens processadas serão salvas automaticamente na pasta:
    ```
    out/
    ```

## **Demonstração**

O vídeo `demonstracao.mp4` mostra o funcionamento completo do programa, passo a passo.
