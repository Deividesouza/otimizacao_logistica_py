from dataclasses import dataclass, field
from typing import Tuple, List

@dataclass
class CentroDistribuicao:
    id: int
    nome: str
    localizacao: Tuple[float, float]
    entregas: List['Entrega'] = field(default_factory=list)
    caminhoes: List['Caminhao'] = field(default_factory=list)

    def __hash__(self):
        return hash(self.id)

@dataclass(frozen=True)  # Classe congelada para ser hashable
class Entrega:
    destino: Tuple[float, float]
    peso: float
    prazo: int

@dataclass
class Caminhao:
    id: int
    capacidade_max: float
    carga_atual: float = 0.0
    rota: List[Tuple[float, float]] = field(default_factory=list)

    @property
    def capacidade_restante(self) -> float:
        return self.capacidade_max - self.carga_atual