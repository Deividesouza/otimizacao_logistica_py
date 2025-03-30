from dataclasses import dataclass, field
from typing import Tuple, List

@dataclass(frozen=True)  # Adicione frozen=True
class CentroDistribuicao:
    nome: str
    localizacao: Tuple[float, float]
    entregas: List['Entrega'] = field(default_factory=list)
    caminhoes: List['Caminhao'] = field(default_factory=list)

@dataclass
class Entrega:
    destino: Tuple[float, float]
    peso: float  # em quilogramas
    prazo: int   # em horas

@dataclass
class Caminhao:
    capacidade_max: float = 3000.0  # em quilogramas
    rota: List[Tuple[float, float]] = field(default_factory=list)
    carga_atual: float = 0.0

    @property
    def capacidade_restante(self) -> float:
        return self.capacidade_max - self.carga_atual