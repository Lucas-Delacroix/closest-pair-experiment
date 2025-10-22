import os, numpy as np
from src.divide_conquer import ClosestPairDivideConquer
from src.brute_force import ClosestPairBruteForce
from src.datasets import make_dataset
from src.plot import plot_comparison, plot_single
from functools import lru_cache

gen = make_dataset(mode="mixed")

@lru_cache(maxsize=None)
def _cached_points(n: int, seed: int):
    return tuple(gen(n, seed))

def dataset(n: int, seed: int):
    return list(_cached_points(n, seed))

def linspace_int(a,b,k): return np.linspace(a,b,k,dtype=int).tolist()

if __name__ == "__main__":
    os.makedirs("results/csv", exist_ok=True)
    os.makedirs("results/figures", exist_ok=True)

    # Entrada completa algoritmo D&C
    sizes_all = linspace_int(100, 1_000_000, 100)

    # Entrada para o algoritmo BF adaptada devido a entrada grande
    sizes_small = [n for n in sizes_all if n <= 30_000]

    # Entrada pequena para fins de teste
    # sizes_all = linspace_int(100, 2_000, 10)
    # sizes_small = sizes_all

    bf = ClosestPairBruteForce()
    dc = ClosestPairDivideConquer()

    bf_rows = bf.benchmark(sizes_small, dataset, trials=10, warmup=True, max_time_per_trial=10.0)
    dc_rows_small = dc.benchmark(sizes_small, dataset, trials=10, warmup=True, verify_with=bf)
    dc_rows_large = dc.benchmark(sizes_all, dataset, trials=10, warmup=True)

    bf.export_csv("results/csv/benchmark_bf.csv", bf_rows)
    dc.export_csv("results/csv/benchmark_dc_small.csv", dc_rows_small)
    dc.export_csv("results/csv/benchmark_dc_large.csv", dc_rows_large)

    plot_comparison(bf_rows, dc_rows_small, out_path="results/figures/closest_pair_small.png")

    plot_single(dc_rows_large, out_path="results/figures/closest_pair_large.png", title="D&C")