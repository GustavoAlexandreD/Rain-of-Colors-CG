# Rain of Colors ☔🎨

## Visão Geral

**Rain of Colors** é um jogo arcade 2D frenético desenvolvido como avaliação para a disciplina de Computação Gráfica. O jogador controla um balde e deve capturar gotas de chuva correspondentes à cor indicada na interface, desviando de bombas e utilizando itens especiais para sobreviver ao aumento progressivo de dificuldade.

O grande diferencial deste projeto é a **construção do motor gráfico do zero**. Seguindo as restrições acadêmicas da disciplina, nenhuma biblioteca gráfica de alto nível foi utilizada para a renderização das formas. O Pygame atua apenas como um *buffer* de pixels, gerenciador de janelas e reprodutor de áudio. Todos os algoritmos de rasterização, preenchimento, transformações, recorte e mapeamento de textura foram implementados manualmente utilizando cálculos matemáticos e manipulação direta de matrizes de pixels.

---

## 🎮 Mecânicas do Jogo

- **Objetivo:** Coletar as gotas da cor correta (mostrada no painel direito) e acumular pontos.
- **Sistema de Combo:** Coletar gotas corretas consecutivamente aumenta o multiplicador de pontos. Coletar uma gota errada zera o combo e retira uma vida.
- **Dificuldade Progressiva:** A velocidade da chuva de objetos aumenta dinamicamente conforme a pontuação sobe.
- **Itens Especiais:**
  - 🌟 **Estrela:** Concede invencibilidade (menos bombas) e poder de pegar gotas de quaquer cor.
  - 🧊 **Gelo:** Congela o balde por alguns segundos.
  - 💖 **Coração:** Restaura uma vida perdida.
  - 💣 **Bomba:** Causa *Game Over* instantâneo se coletada.

---

## ⚙️ Conceitos de Computação Gráfica Implementados

Para demonstrar o domínio sobre o pipeline gráfico, a arquitetura do projeto foi dividida em um núcleo de sistema (`src/system/`) e na lógica do jogo (`src/game/`). Os seguintes algoritmos foram implementados na unha:

### 1. Rasterização de Primitivas (`system/primitivas/`)
- **Algoritmo de Bresenham (`Linha.py`, `Circulo.py`):** Utilizado para o desenho otimizado de Linhas e Círculos geométricos pixel a pixel.
- **Algoritmo de Bezier (`Curva.py`)**: Utiliza para o desenho de curvas.

### 2. Preenchimento de Regiões (`system/preenchimento_e_textura/`)
- **Scanline Fill (`Preenchimento.py`):** Algoritmo de varredura horizontal utilizado para preencher polígonos complexos (como a Gota, a Estrela e o Balde).
- **Flood Fill (`Preenchimento.py`):** Algoritmo de preenchimento 4-conectado.

### 3. Mapeamento de Textura e Máscaras (`system/preenchimento_e_textura/`)
- **Scanline com Coordenadas UV (`Texture_Mapping.py`):** Implementação de um rasterizador capaz de ler coordenadas `(u, v)` de uma imagem original e aplicá-las a um polígono na tela (usado para renderizar o fundo e criar a máscara 3D do "teto" de onde a chuva cai).

### 4. Recorte (Clipping) (`system/clipping/`)
- **Cohen-Sutherland (`Cohen_Sutherland.py`):** Algoritmo analítico de recorte de linhas que divide a tela em regiões (Outcodes) para impedir que as formas do jogo invadam a área reservada à interface de usuário.

### 5. Pipeline de Visualização (`system/transformacoes_geometricas/`)
- **Window to Viewport (`Janela_Viewport.py`):** Mapeamento matemático do universo do jogo (*World Coordinates*) para a tela do monitor (*Device Coordinates*). Utilizado para criar o **Radar/Mini-mapa** dinâmico no painel direito.

### 6. Transformações Geométricas 2D (`system/transformacoes_geometricas/Transformacoes_Geometricas.py`)
- Operações matriciais de **Translação, Rotação e Escala** aplicadas aos vértices dos objetos (como a animação de pulsação da Estrela e a rotação do floco de Gelo).

---

## 📁 Arquitetura do Projeto

O projeto segue uma arquitetura modularizada, separando claramente o que é o "Motor Gráfico" construído para a disciplina e o que é a lógica e interface do jogo.

```text
Rain-of-Colors-CG/
│
├── assets/                     # Recursos visuais e sonoros
│   ├── audio/                  # Músicas (LofiRain) e efeitos sonoros (Botões)
│   ├── fonts/                  # Fontes em pixel-art (ThaleahFat)
│   └── images/                 # Texturas e fundos (Menu, Jogo e Viewport)
│
├── src/                        # Código-fonte principal
│   ├── main.py                 # Ponto de entrada, Loop Principal e transição de telas
│   │
│   ├── system/                 # ⚙️ MOTOR GRÁFICO (CG Engine)
│   │   ├── primitivas/         # Algoritmos base: SetPixel, Linha (Bresenham), Círculo, etc.
│   │   ├── preenchimento_e_textura/ # Scanline Fill, Mapeamento UV e Máscaras
│   │   ├── transformacoes_geometricas/ # Matrizes 2D, Window e Viewport (Minimapa)
│   │   └── clipping/           # Algoritmo de Cohen-Sutherland
│   │
│   └── game/                   # 🎮 LÓGICA DO JOGO E INTERFACE
│       ├── front_end/          # Telas, HUD e renderização de textos
│       │   ├── TelasPrincipais/# Jogo, Menu, Tutorial, Estatísticas e Pause
│       │   ├── Componentes/    # Elementos visuais (Background com textura, Corações)
│       │   └── helper/         # Sistema de responsividade e proporção de tela
│       │
│       └── scripts/            # Mecânicas, entidades e regras de negócio
│           ├── ObjetosdaChuva/ # Factory e entidades (Gota, Bomba, Estrela, Gelo)
│           ├── player/         # Controle e física do Balde
│           ├── GameState.py    # Controle de Score, Combos e estados de Poderes
│           └── Pontuacao.py    # Leitura e gravação do ranking (recordes.txt)
│
├── recordes.txt                # Armazenamento local das pontuações (Highscores)
├── pyproject.toml / poetry.lock # Gerenciamento de dependências via Poetry
└── venv/                       # Ambiente virtual Python
```
---

## 🚀 Como Executar o Projeto
Este projeto foi desenvolvido e testado em ambiente Linux, utilizando Python 3.12. O gerenciamento de dependências foi feito através do Poetry, mas também pode ser executado via ambiente virtual padrão.

### Pré-requisitos
- Python 3.x instalado
- Pygame (utilizado apenas para display e áudio)

### Passo a passo (Usando VENV e PIP)
1. Clone o repositório ou extraia a pasta do projeto.
2. Acesse o diretório do projeto:

Bash
```code
cd Rain-of-Colors-CG
```
3. Ative o ambiente virtual (já incluso na estrutura ou crie um novo):

Bash
```code
source venv/bin/activate
```
4. Instale as dependências (caso não estejam no venv):

Bash
```code
pip install pygame
```
5. Execute o jogo:

Bash
```code
python src/main.py
```
### Passo a passo (Usando Poetry)
Se você tiver o gerenciador Poetry instalado em sua máquina:

Bash
```code
poetry install
poetry run python src/main.py
```
---

## ⌨️ Controles
- **Setas**: Interação com os menus (Jogar, Tutorial, Estatísticas) / Movimentação do balde.
- **ESC**: Retorna ao Menu Principal.
- **P**: Pausa o jogo.

---

## Equipe
- **Ramon Venâncio** - ramon.venancio@aluno.uece.br
- **Helen Braga** - helen.alves@aluno.uece.br
- **Gustavo Alexandre** - gustavo.alexandre@aluno.uece.br