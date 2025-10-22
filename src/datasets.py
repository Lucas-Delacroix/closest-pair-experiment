import random
from typing import List, Literal
from .base import Point, DatasetFn

Mode = Literal["uniform", "clusters", "mixed", "line"]

SPACE_SIZE = 1_000_000 # tamanho do espaço em X e Y
DEFAULT_SEED = 123456789 # semente base para RNG

# clusters
DEFAULT_NUM_CLUSTERS = 5 # número de clusters
DEFAULT_CLUSTER_SIGMA = 10_000 # espalhamento dos clusters

# linha
LINE_SPACING = 100.0 # distância fixa no eixo X
LINE_SIGMA = 5.0  # ruído no eixo Y


def _generate_clusters(rng, n: int, k: int = DEFAULT_NUM_CLUSTERS, sigma: float = DEFAULT_CLUSTER_SIGMA) -> List[Point]:
    centers = [(rng.uniform(0, SPACE_SIZE), rng.uniform(0, SPACE_SIZE)) for _ in range(k)]
    return [Point(rng.gauss(cx, sigma), rng.gauss(cy, sigma))
            for _ in range(n) for (cx, cy) in [centers[rng.randrange(k)]]]

def _generate_uniform(rng, n: int) -> List[Point]:
    return [Point(rng.uniform(0,SPACE_SIZE), rng.uniform(0,SPACE_SIZE)) for _ in range(n)]

def _generate_line(rng, n: int) -> List[Point]:
    return [Point(i*LINE_SPACING, rng.gauss(0.0, LINE_SIGMA)) for i in range(n)]


def make_dataset(mode: Mode = "mixed", seed_base: int = 123456789) -> DatasetFn:
    def gen(n: int, seed: int) -> List[Point]:
        rng = random.Random(seed_base + seed + n)

        if mode == "uniform":
            return _generate_uniform(rng, n)

        elif mode == "clusters":
            return _generate_clusters(rng, n)

        elif mode == "line":
            return _generate_line(rng, n)

        else:
            half = n // 2
            pts = _generate_uniform(rng, half)
            pts += _generate_clusters(rng, n - half)
            return pts
    return gen