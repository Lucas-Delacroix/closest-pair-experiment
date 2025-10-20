from __future__ import annotations
import math
from typing import List, NamedTuple

class Point(NamedTuple):
    x: float
    y: float

ClosestPairResult = Tuple[float, Tuple[Point, Point]]  # (distância, (pontoA, pontoB))


class ClosestPairBase:
    """
    Classe base que padroniza o comportamento dos algoritmos de busca
    do par de pontos mais próximo. Fornece utilidades compartilhadas,
    como a função de distância euclidiana.
    """

    @staticmethod
    def dist(p: Point, q: Point) -> float:
        """
        Calcula a distância euclidiana entre dois pontos 2D usando math.hypot() (com sqrt).
        """
        return math.hypot(p[0] - q[0], p[1] - q[1])

    def dist2(p: Point, q: Point) -> float:
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
