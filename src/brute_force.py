from __future__ import annotations
from typing import List, Tuple, Set
from .base import Point, ClosestPairBase, ClosestPairResult

class ClosestPairBruteForce(ClosestPairBase):
    name = "Brute O(n^2)"

    def run(self, points: List[Point]) -> ClosestPairResult:
        n = len(points)
        if n < 2:
            return (float("inf"), (None, None))
        best_d2 = float("inf")
        best_pair = (points[0], points[1])
        for i in range(n):
            pi = points[i]
            for j in range(i+1, n):
                pj = points[j]
                d2 = self.dist2(pi, pj)
                if d2 < best_d2:
                    best_d2 = d2
                    best_pair = (pi, pj)
        return (best_d2 ** 0.5, best_pair)