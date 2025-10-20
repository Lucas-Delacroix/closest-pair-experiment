from __future__ import annotations
import math
from typing import List, Tuple

Point = Tuple[float, float]  # Representa um ponto 2D.
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
        Calcula a distância euclidiana entre dois pontos 2D usando math.hypot().
        """
        return math.hypot(p[0] - q[0], p[1] - q[1])

    def run(self, points: List[Point]) -> ClosestPairResult:
        """
        Deve ser implementado por cada subclasse.
        Retorna uma tupla (distância, (pontoA, pontoB)).
        """
        raise NotImplementedError
