from typing import List, Dict, Any, Tuple
import matplotlib.pyplot as plt
import os, csv

def _align_by_n(rows_a: List[Dict[str,Any]], rows_b: List[Dict[str,Any]]):
    byn_a = {r["n"]: r for r in rows_a}
    byn_b = {r["n"]: r for r in rows_b}
    common = sorted(set(byn_a.keys()) & set(byn_b.keys()))
    A = [byn_a[n] for n in common]
    B = [byn_b[n] for n in common]
    return common, A, B

def plot_comparison(
    brute_rows: List[Dict[str,Any]],
    dc_rows: List[Dict[str,Any]],
    out_path: str = "results/figures/closest_pair_small.png",
    title: str = "Comparação direta"
):
    ns, A, B = _align_by_n(brute_rows, dc_rows)
    if not ns:
        print("Nada a plotar (sem n em comum).")
        return
    bf_m = [r["mean"] for r in A]; bf_s = [r["std"] for r in A]
    dc_m = [r["mean"] for r in B]; dc_s = [r["std"] for r in B]

    plt.figure(figsize=(8,5))
    plt.errorbar(ns, bf_m, yerr=bf_s, fmt="o-", label=A[0]["algo"])
    plt.errorbar(ns, dc_m, yerr=dc_s, fmt="o-", label=B[0]["algo"])
    plt.xlabel("n (número de incidentes)")
    plt.ylabel("tempo médio (s)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    print("Figura salva:", out_path)

def plot_single(
    rows: List[Dict[str,Any]],
    out_path: str = "results/figures/closest_pair_large.png",
    title: str = "Escala grande "
):
    rows = sorted(rows, key=lambda r: r["n"])
    ns = [r["n"] for r in rows]
    ms = [r["mean"] for r in rows]
    ss = [r["std"] for r in rows]

    plt.figure(figsize=(8,5))
    plt.errorbar(ns, ms, yerr=ss, fmt="o-", label=rows[0]["algo"] if rows else "algo")
    plt.xlabel("n (número de incidentes)")
    plt.ylabel("tempo médio (s)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    print("Figura salva:", out_path)



def save_points_csv(path: str, points):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x","y"])
        for p in points:
            w.writerow([p.x, p.y])
