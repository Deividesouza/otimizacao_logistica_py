from dataclasses import dataclass, field
from typing import Tuple, List

@dataclass
class CentroDistribuicao:
    nome: str
    localizacao: Tuple[float, float] # no futuro irei usar latitude e longitude
    entregas: List['Entrega'] = field(default_factory=list)
    caminhoes: List['Caminhao'] = field(default_factory=list)

@dataclass
class Entrega:
    destino: Tuple[float, float]
    peso: float  # em quilogramas
    prazo: int   # em horas

@dataclass
class Caminhao:
    capacidade_max: float  # em quilogramas
    rota: List[Tuple[float, float]] = field(default_factory=list)
    carga_atual: float = 0.0

    @property
    def capacidade_restante(self) -> float:
        return self.capacidade_max - self.carga_atual