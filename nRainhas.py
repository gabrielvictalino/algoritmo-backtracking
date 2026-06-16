import time


def posicao_segura(linha, coluna, pos):
    for i in range(linha):
        # mesma coluna
        if pos[i] == coluna:
            return 0

        # mesma diagonal
        if abs(pos[i] - coluna) == abs(i - linha):
            return 0

    return 1


def resolver_n_rainhas(linha, pos, total_solucoes, n):
    if linha == n:
        total_solucoes[0] = total_solucoes[0] + 1
        return

    for coluna in range(n):
        if posicao_segura(linha, coluna, pos):
            pos[linha] = coluna
            resolver_n_rainhas(linha + 1, pos, total_solucoes, n)


def main():
    total_solucoes = [0]

    n = int(input())

    pos = [0] * n

    inicio = time.monotonic()

    total_solucoes[0] = 0
    resolver_n_rainhas(0, pos, total_solucoes, n)

    fim = time.monotonic()

    tempo = fim - inicio

    print(f"n = {n}, solucoes = {total_solucoes[0]}, tempo = {tempo:.6f} segundos")


if name == "main":
    main()