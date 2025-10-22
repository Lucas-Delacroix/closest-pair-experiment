import os, numpy as np
from src.divide_conquer import ClosestPairDivideConquer
from src.brute_force import ClosestPairBruteForce
from src.datasets import make_dataset
from src.base import ClosestPairBase
from src.plot import plot_comparison, plot_single

def linspace_int(a,b,k): return np.linspace(a,b,k,dtype=int).tolist()

if __name__ == "__main__":
    os.makedirs("results/csv", exist_ok=True)
    os.makedirs("results/figures", exist_ok=True)

    # sizes_all = linspace_int(10, 2000, 5)
    sizes_all = linspace_int(100, 10_000, 20)
    # sizes_all = linspace_int(100, 1_000_000, 100)
    sizes_small = [n for n in sizes_all if n <= 30_000]

    dataset = make_dataset(mode="mixed")

    bf = ClosestPairBruteForce()
    dc = ClosestPairDivideConquer()

    bf_rows = bf.benchmark(sizes_small, dataset, trials=10, warmup=True, max_time_per_trial=10.0)
    dc_rows_small = dc.benchmark(sizes_small, dataset, trials=10, warmup=True)
    dc_rows_large = dc.benchmark(sizes_all,  dataset, trials=10, warmup=True)

    ClosestPairBase.export_csv("results/csv/benchmark_bf.csv", bf_rows)
    ClosestPairBase.export_csv("results/csv/benchmark_dc_small.csv", dc_rows_small)
    ClosestPairBase.export_csv("results/csv/benchmark_dc_large.csv", dc_rows_large)

    plot_comparison(bf_rows, dc_rows_small, out_path="results/figures/closest_pair_small.png")
    plot_single(dc_rows_large, out_path="results/figures/closest_pair_large.png",
                title="D&C")