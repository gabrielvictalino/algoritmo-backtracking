#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

    struct timespec inicio,
    fim;
int n;
int *pos; // pos[linha] = coluna

int posicao_segura(int linha, int coluna)
{
    for (int i = 0; i < linha; i++)
    {
        // mesma coluna
        if (pos[i] == coluna)
        {
            return 0;
        }
        // mesma diagonal
        if (abs(pos[i] - coluna) == abs(i - linha))
        {
            return 0;
        }
    }
    return 1;
}

long long total_solucoes = 0;

void resolver_n_rainhas(int linha)
{
    if (linha == n)
    {
        total_solucoes++;
        return;
    }

    for (int coluna = 0; coluna < n; coluna++)
    {
        if (posicao_segura(linha, coluna))
        {
            pos[linha] = coluna;
            resolver_n_rainhas(linha + 1);
        }
    }
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("Uso: %s n\n", argv[0]);
        return 1;
    }

    n = atoi(argv[1]);
    pos = (int *)malloc(n * sizeof(int));
    if (pos == NULL)
    {
        printf("Erro ao alocar memória\n");
        return 1;
    }

    clock_gettime(CLOCK_MONOTONIC, &inicio);

    total_solucoes = 0;
    resolver_n_rainhas(0);

    clock_gettime(CLOCK_MONOTONIC, &fim);

    double tempo = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;

    printf("n = %d, solucoes = %lld, tempo = %.6f segundos\n",
           n, total_solucoes, tempo);

    free(pos);
    return 0;
}