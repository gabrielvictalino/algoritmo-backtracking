"""
Descrição: Encontra todas as soluções válidas para problema das N-Rainhas usando backtracking.

 Análise de Complexidade:
   - Melhor Caso:  Ω(N)    — 1ª solução encontrada cedo
   - Caso Médio:   Θ(N!)   — comportamento típico
   - Pior Caso:    O(N!)   — exploração máxima da árvore
"""


import time
import math
import statistics

N_RAINHAS = 8
RODADAS = 30


def tempo_atual_ns() -> int:
    # Retorna o tempo atual em nanosegundos para medir a duração de uma execução.
    return time.perf_counter_ns()


def imprimir_tabuleiro(tabuleiro: list[int], n: int) -> None:
    # Imprime o tabuleiro em formato visual com linhas e colunas numeradas.
    print()
    print("    " + "  ".join(f"{c:2}" for c in range(n)))
    print("    " + "───" * n)
    for linha in range(n):
        # Para cada linha, imprime um símbolo de rainha ou ponto vazio.
        celulas = " ".join("♛" if tabuleiro[col] == linha else "·" for col in range(n))
        print(f" {linha:2}│ {celulas} │")
    print("    " + "───" * n)


def tem_conflito(tabuleiro: list[int], col: int, linha: int) -> bool:
    """
    Verifica se a rainha em (col, linha) conflita com
    alguma das rainhas já posicionadas nas colunas 0..col-1.
    Checa mesma linha e diagonais.
    """
    for c in range(col):
        l = tabuleiro[c]
        if l == linha:
            # Conflito quando existe outra rainha na mesma linha.
            return True
        if abs(l - linha) == abs(c - col):
            # Conflito quando existe outra rainha na mesma diagonal.
            return True
    return False


def backtracking(
    tabuleiro: list[int],
    n: int,
    col: int,
    contadores: dict,
    apenas_primeira: bool = False
) -> None:
    """
    Função recursiva para tentar colocar rainhas coluna a coluna.
    Se col == n, significa que uma solução completa foi encontrada.
    """
    contadores["nos"] += 1

    if col == n:
        # Caso base: todas as rainhas foram posicionadas sem conflito.
        contadores["solucoes"] += 1
        return

    for linha in range(n):
        # Tenta cada linha possível na coluna atual.
        if not tem_conflito(tabuleiro, col, linha):
            tabuleiro[col] = linha
            backtracking(tabuleiro, n, col + 1, contadores, apenas_primeira)

            # Se apenas a primeira solução é necessária, para após achá-la.
            if apenas_primeira and contadores["solucoes"] > 0:
                return
        else:
            # Conta como poda quando a posição é descartada por conflito.
            contadores["podas"] += 1

    # Retrocede para tentar outras possibilidades em colunas anteriores.
    tabuleiro[col] = -1


def executar_cenario(n: int, apenas_primeira: bool = False) -> dict:
    """
    Executa o algoritmo de backtracking uma vez e retorna métricas.
    """
    tabuleiro  = [-1] * n
    contadores = {"nos": 0, "solucoes": 0, "podas": 0}

    inicio = tempo_atual_ns()
    backtracking(tabuleiro, n, 0, contadores, apenas_primeira)
    fim = tempo_atual_ns()

    return {
        "tempo_ns": fim - inicio,
        "nos":      contadores["nos"],
        "solucoes": contadores["solucoes"],
        "podas":    contadores["podas"],
    }


# Estatísticas
def calcular_estatisticas(resultados: list[dict]) -> dict:
    """Calcula média, desvio-padrão, mínimo e máximo dos tempos."""
    tempos = [r["tempo_ns"] for r in resultados]
    nos    = [r["nos"]      for r in resultados]
    return {
        "media_ns":  statistics.mean(tempos),
        "desvio_ns": statistics.stdev(tempos) if len(tempos) > 1 else 0.0,
        "min_ns":    min(tempos),
        "max_ns":    max(tempos),
        "media_nos": int(statistics.mean(nos)),
        "solucoes":  resultados[0]["solucoes"],
    }


# ─── Impressão de Tabelas ─────────────────────────────────
SEP  = "├────────────────┼─────────────┼──────────────┼──────────────┼─────────────┤"
TOPO = "┌────────────────┬─────────────┬──────────────┬──────────────┬─────────────┐"
ROD  = "└────────────────┴─────────────┴──────────────┴──────────────┴─────────────┘"
CAB  = "│    Cenário     │  Média (µs) │  Desvio (µs) │  Mín (µs)   │  Nós/Média  │"

def imprimir_linha_tabela(nome: str, est: dict) -> None:
    print(f"│ {nome:<14} │ {est['media_ns']/1000:11.3f} │ "
          f"{est['desvio_ns']/1000:12.3f} │ {est['min_ns']/1000:12.3f} │ "
          f"{est['media_nos']:11d} │")


# ─── Experimento Completo para N ─────────────────────────
def executar_experimento_completo(n: int) -> None:
    """Roda os 3 cenários com 30 rodadas cada para um dado N."""

    print(f"EXPERIMENTO: {n}-RAINHAS (N = {n})")
    print(f"  Rodadas por cenário: {RODADAS}\n")

    cenarios = [
        ("Melhor Caso",  True),
        ("Caso Medio",   False),
        ("Pior Caso",    False),   # Para N-Rainhas, pior ≈ médio completo
    ]

    print(TOPO)
    print(CAB)
    print(SEP)

    for i, (nome, apenas_primeira) in enumerate(cenarios):
        resultados = [executar_cenario(n, apenas_primeira) for _ in range(RODADAS)]
        est = calcular_estatisticas(resultados)
        imprimir_linha_tabela(nome, est)

        if nome == "Caso Medio":
            print(f"│  → Soluções encontradas: {est['solucoes']:<33} │")
            print(SEP)
        elif i < len(cenarios) - 1:
            print(SEP)

    print(ROD)


# Demonstração Visual 
def demonstrar_solucoes(n: int, max_solucoes: int = 3) -> None:
    """Imprime as primeiras `max_solucoes` soluções com tabuleiro visual."""
    print(f"  Primeiras {max_solucoes} soluções para N={n}")

    contagem = [0]

    def buscar(tabuleiro, col):
        if contagem[0] >= max_solucoes:
            return
        if col == n:
            contagem[0] += 1
            print(f"\n  Solução #{contagem[0]}:")
            imprimir_tabuleiro(tabuleiro, n)
            posicoes = "  ".join(f"[{c}→{tabuleiro[c]}]" for c in range(n))
            print(f"  Posições (col→linha): {posicoes}")
            return
        for linha in range(n):
            if not tem_conflito(tabuleiro, col, linha):
                tabuleiro[col] = linha
                buscar(tabuleiro, col + 1)
                if contagem[0] >= max_solucoes:
                    return
                tabuleiro[col] = -1

    buscar([-1] * n, 0)


# Comparação pequeno, médio e grande 
def comparar_tamanhos() -> None:
    """Executa o algoritmo para N=4, N=8 e N=12 e exibe tabela comparativa."""
    tamanhos = [4, 8, 12]
    labels   = ["Pequeno (N=4 )", "Medio   (N=8 )", "Grande  (N=12)"]

    print(f"COMPARAÇÃO: PEQUENO vs MÉDIO vs GRANDE")
    print(f"    Caso considerado: Todas as soluções (Caso Médio/Completo)")
    print(f"    Rodadas por tamanho: {RODADAS}\n")

    SEP2 = "├──────────────────┼─────────────┼──────────────┼──────────────┼─────────────┤"
    print("┌──────────────────┬─────────────┬──────────────┬──────────────┬─────────────┐")
    print("│    Tamanho       │  Média (µs) │  Desvio (µs) │  Soluções   │  Nós/Média  │")
    print(SEP2)

    for i, (n, label) in enumerate(zip(tamanhos, labels)):
        resultados = [executar_cenario(n, False) for _ in range(RODADAS)]
        est = calcular_estatisticas(resultados)
        print(f"│ {label:<16} │ {est['media_ns']/1000:11.3f} │ "
              f"{est['desvio_ns']/1000:12.3f} │ {est['solucoes']:12d} │ "
              f"{est['media_nos']:11d} │")
        if i < len(tamanhos) - 1:
            print(SEP2)

    print("└──────────────────┴─────────────┴──────────────┴──────────────┴─────────────┘")
    print("\n  Nota: Use esses dados para plotar os gráficos do relatório.")
    print("  Eixo X = N (tamanho), Eixo Y = Tempo médio (µs)")
    print("  Sobreposição teórica: curva N! para comparação.")


# Main
def main() -> None:
    print("PROBLEMA DAS N-RAINHAS — BACKTRACKING")
    print("\n   Complexidade: O(N!) — Backtracking com poda")
    print("     Medição: time.perf_counter_ns() [nanosegundos]")
    print("     Executar com: python3 n_rainhas_backtracking.py")

    # 1. Demonstração visual
    demonstrar_solucoes(N_RAINHAS, max_solucoes=3)

    # 2. Experimento completo N=8
    executar_experimento_completo(N_RAINHAS)

    # 3. Comparação de tamanhos
    comparar_tamanhos()

    print("     ANÁLISE ASSINTÓTICA RESUMIDA   ")
    print("-> Big-O  (Pior Caso):   O(N!)  — ~N! chamadas recursivas")
    print("-> Big-Ω  (Melhor Caso): Ω(N)   — 1ª solução em 1 ramo")
    print("->  Big-Θ  (Caso Médio):  Θ(N!)  — média das execuções")
    print()
    print("  • Classe de Complexidade: P")
    print("    → Decidir se ∃ solução para N-Rainhas é O(N!) mas")
    print("      verificar uma solução dada é O(N²) → problema em P.")
    print()
    print("  • Problema NP relacionado: N-Rainhas Generalizado")
    print("    → Contar TODAS as soluções é #P-Completo.")
    print("    → Variante de satisfatibilidade (SAT) é NP-Completo.")


if __name__ == "__main__":
    main()