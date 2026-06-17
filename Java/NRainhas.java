import java.util.Scanner;

public class NRainhas {

    public static boolean posicaoSegura(int linha, int coluna, int[] pos) {
        for (int i = 0; i < linha; i++) {

            // mesma coluna
            if (pos[i] == coluna) {
                return false;
            }

            // mesma diagonal
            if (Math.abs(pos[i] - coluna) == Math.abs(i - linha)) {
                return false;
            }
        }
        return true;
    }

    public static void resolverNRainhas(
            int linha,
            int[] pos,
            int n,
            int[] totalSolucoes,
            int[] totalChamadasRNR) {

        totalChamadasRNR[0]++;

        if (linha == n) {
            totalSolucoes[0]++;
            return;
        }

        for (int coluna = 0; coluna < n; coluna++) {
            if (posicaoSegura(linha, coluna, pos)) {
                pos[linha] = coluna;
                resolverNRainhas(
                        linha + 1,
                        pos,
                        n,
                        totalSolucoes,
                        totalChamadasRNR);
            }
        }
    }

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();

        int[] pos = new int[n];

        int[] totalSolucoes = {0};
        int[] totalChamadasRNR = {0};

        long inicio = System.nanoTime();

        resolverNRainhas(
                0,
                pos,
                n,
                totalSolucoes,
                totalChamadasRNR);

        long fim = System.nanoTime();

        double tempo = (fim - inicio) / 1_000_000_000.0;

        System.out.printf(
                "n = %d, solucoes = %d, tempo = %.6f segundos, chamadasRNR = %d%n",
                n,
                totalSolucoes[0],
                tempo,
                totalChamadasRNR[0]);

        scanner.close();
    }
}
