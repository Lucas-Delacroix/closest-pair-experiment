from __future__ import annotations
from typing import List, Tuple, Set
from .base import Point, ClosestPairBase, ClosestPairResult

class ClosestPairDivideConquer(ClosestPairBase):
    name = "D&C O(n log n)"

    def run(self, points: List[Point]) -> ClosestPairResult:
        n = len(points)
        if n < 2:
            return (float("inf"), (None, None))
        Px = sorted(points, key=lambda p: (p.x, p.y))
        Py = sorted(points, key=lambda p: (p.y, p.x))
        d2, pair = self._rec(Px, Py)
        return (d2 ** 0.5, pair)

    def _rec(self, Px: List[Point], Py: List[Point]) -> Tuple[float, Tuple[Point, Point]]:
        n = len(Px)
        if n <= 3:
            return self._brute_small(Px)

        mid = n // 2
        Qx, Rx = Px[:mid], Px[mid:]
        mid_x = Px[mid].x

        qset: Set[Point] = set(Qx)
        Qy, Ry = [], []
        for p in Py:
            (Qy if p in qset else Ry).append(p)

        #T(n) = 2T(n/2) + O(n)
        dl2, pair_l = self._rec(Qx, Qy)
        dr2, pair_r = self._rec(Rx, Ry)
        d2, best = (dl2, pair_l) if dl2 < dr2 else (dr2, pair_r)

        strip = [p for p in Py if (p.x - mid_x) * (p.x - mid_x) < d2]
        m = len(strip)
        for i in range(m):
            pi = strip[i]
            for j in range(i+1, min(i+8, m)):
                pj = strip[j]
                dy = pj.y - pi.y
                if dy*dy >= d2:
                    break
                dij2 = self.dist2(pi, pj)
                if dij2 < d2:
                    d2 = dij2
                    best = (pi, pj)
        return d2, best

    def _brute_small(self, pts: List[Point]) -> Tuple[float, Tuple[Point, Point]]:
        best_d2 = float("inf")
        best_pair = (pts[0], pts[1]) if len(pts) >= 2 else (None, None)
        n = len(pts)
        for i in range(n):
            for j in range(i+1, n):
                d2 = self.dist2(pts[i], pts[j])
                if d2 < best_d2:
                    best_d2 = d2
                    best_pair = (pts[i], pts[j])
        return best_d2, best_pair