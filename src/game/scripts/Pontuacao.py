import os

ARQUIVO_PONTUACOES = "recordes.txt"

def carregar_pontuacoes():
    """Lê o arquivo de recordes. Se não existir, cria uma lista zerada."""
    if os.path.exists(ARQUIVO_PONTUACOES):
        with open(ARQUIVO_PONTUACOES, "r") as f:
            # Lê as linhas e tira os espaços/quebras de linha
            linhas = [linha.strip() for linha in f.readlines() if linha.strip()]
            
            # Garante que sempre teremos 10 posições, mesmo se o arquivo estiver incompleto
            while len(linhas) < 10:
                linhas.append("000000")
            return linhas[:10]
    else:
        # Se for a primeira vez rodando o jogo, retorna 10 zeros
        return ["000000"] * 10

def salvar_pontuacoes(pontuacoes):
    """Escreve a lista atualizada no arquivo txt."""
    with open(ARQUIVO_PONTUACOES, "w") as f:
        for p in pontuacoes:
            f.write(f"{p}\n")