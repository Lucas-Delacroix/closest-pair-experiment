from __future__ import annotations
import random
from typing import List, Literal
from .base import Point, DatasetFn

Mode = Literal["uniform", "clusters", "mixed", "line"]

def make_dataset(mode: Mode = "mixed", seed_base: int = 123456789) -> DatasetFn:
    def gen(n: int, seed: int) -> List[Point]:
        rng = random.Random(seed_base + seed + n)
        if mode == "uniform":
            return [Point(rng.uniform(0,1_000_000), rng.uniform(0,1_000_000)) for _ in range(n)]
        if mode == "clusters":
            k = 5
            centers = [(rng.uniform(0,1_000_000), rng.uniform(0,1_000_000)) for _ in range(k)]
            sigma = 10_000.0
            return [Point(rng.gauss(cx, sigma), rng.gauss(cy, sigma))
                    for _ in range(n) for (cx,cy) in [centers[rng.randrange(k)]]]
        if mode == "line":
            return [Point(i*100.0, rng.gauss(0.0, 5.0)) for i in range(n)]
        half = n // 2
        pts = [Point(rng.uniform(0,1_000_000), rng.uniform(0,1_000_000)) for _ in range(half)]
        k = 5
        centers = [(rng.uniform(0,1_000_000), rng.uniform(0,1_000_000)) for _ in range(k)]
        sigma = 10_000.0
        pts += [Point(rng.gauss(cx, sigma), rng.gauss(cy, sigma))
                for _ in range(n - half) for (cx,cy) in [centers[rng.randrange(k)]]]
        return pts
    return gen