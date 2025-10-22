from typing import List, Tuple, NamedTuple, Callable, Iterable, Optional, Dict, Any, TypeAlias
import math, time, csv, statistics


class Point(NamedTuple):
    x: float
    y: float

Distance: TypeAlias = float
Seconds: TypeAlias  = float
ClosestPairResult = Tuple[float, Tuple[Point, Point]]
DatasetFn = Callable[[int, int], List[Point]]


class ClosestPairBase:
    """
    Classe base que padroniza o comportamento dos algoritmos de busca
    do par de pontos mais próximo. Fornece utilidades compartilhadas,
    como a função de distância euclidiana.
    """

    @staticmethod
    def dist(p: Point, q: Point) -> Distance:
        """
        Calcula a distância euclidiana entre dois pontos 2D usando math.hypot() (com sqrt).
        """
        return math.hypot(p.x - q.x, p.y - q.y)

    @staticmethod
    def dist2(p: Point, q: Point) -> Distance:
        """
        Distância ao quadrado (sem sqrt)
        """
        dx = p.x - q.x
        dy = p.y - q.y
        return dx*dx + dy*dy
    
    def run(self, points: List[Point]) -> ClosestPairResult:
        """
        Deve ser implementado por cada subclasse.
        Retorna uma tupla (distância, (pontoA, pontoB)).
        """
        raise NotImplementedError

    def time_once(self, points: List[Point]) -> Tuple[Seconds, ClosestPairResult]:
        """
        Mede o tempo do algoritmo e retorna (tempo_em_segundos, (dist, (p,q))).
        """
        t0 = time.perf_counter()
        res = self.run(points)
        t1 = time.perf_counter()
        return (t1 - t0), res

    def benchmark(
            self,
            sizes: Iterable[int],
            dataset: DatasetFn,
            trials: int = 10,
            warmup: bool = True,
            max_time_per_trial: Optional[Seconds] = None,
            verify_with: Optional["ClosestPairBase"] = None,
            verify_tolerance: float = 1e-9,
    ):
        """
        Retorna: list[(n, mean, std, trials_done, mismatches)]
        - dataset(n, seed) deve gerar SEMPRE os mesmos dados para mesma (n, seed).
        - Se max_time_per_trial for definido, aborta trials do n atual ao exceder.
        """
        rows = []
        for n in sizes:
            times: List[Seconds] = []
            mismatches = 0
            reps = trials + (1 if warmup else 0)
            aborted = False

            for seed in range(reps):
                pts = dataset(n, seed)
                t, (d, pair) = self.time_once(pts)

                if seed or not warmup:
                    times.append(t)

                    if verify_with is not None:
                        dv, _ = verify_with.run(pts)

                        if not math.isclose(d, dv, rel_tol=0.0, abs_tol=verify_tolerance):
                            mismatches += 1

                if max_time_per_trial is not None and t > max_time_per_trial:
                    aborted = True
                    break

            if times:
                rows.append({
                    "algo": self.name,
                    "n": int(n),
                    "mean": statistics.mean(times),
                    "std": statistics.pstdev(times),
                    "trials": len(times),
                    "mismatches": mismatches
                })
            if aborted:
                continue
        return rows


    def export_csv(self, path: str, rows: List[Dict[str, Any]]) -> None:
        if not rows:
            return
        for r in rows:
            r.setdefault("algo", self.name)
        keys = ["algo", "n", "mean", "std", "trials", "mismatches"]
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k) for k in keys})