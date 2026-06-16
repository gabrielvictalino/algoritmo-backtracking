#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <time.h>


int posicao_segura(int linha, int coluna, int * pos)
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



void resolver_n_rainhas(int linha, int * pos, int * total_solucoes, int n)
{
    if (linha == n)
    {
        (*total_solucoes)= (*total_solucoes) +1;
        return;
    }

    for (int coluna = 0; coluna < n; coluna++)
    {
        if (posicao_segura(linha, coluna,pos))
        {
            pos[linha] = coluna;
            resolver_n_rainhas(linha + 1,pos,total_solucoes,n);
        }
    }
}

int main()
{
    long long total_solucoes = 0;
    struct timespec inicio, fim;
    int n;
    int *pos;
    
    scanf("%d",&n);

    pos = (int *)malloc(n * sizeof(int));


    clock_gettime(CLOCK_MONOTONIC, &inicio);

    total_solucoes = 0;
    resolver_n_rainhas(0,pos,&total_solucoes,n);

    clock_gettime(CLOCK_MONOTONIC, &fim);

    double tempo = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;

    printf("n = %d, solucoes = %lld, tempo = %.6f segundos\n",
           n, total_solucoes, tempo);

    free(pos);
    return 0;
}
