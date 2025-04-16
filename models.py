from typing import Tuple, List

class CentroDistribuicao:
    def __init__(self, id: int, nome: str, localizacao: Tuple[float, float]):
        self.id = id
        self.nome = nome
        self.localizacao = localizacao
        self.entregas: List['Entrega'] = []
        self.caminhoes: List['Caminhao'] = []

class Entrega:
    def __init__(self, id: int, destino_localizacao: Tuple[float, float], destino_nome: str, peso: float, prazo: int):
        self.id = id
        self.destino_localizacao = destino_localizacao
        self.destino_nome = destino_nome
        self.peso = peso
        self.prazo = prazo  # Em dias

class Caminhao:
    def __init__(self, id: int, capacidade_max: float):
        self.id = id
        self.capacidade_max = capacidade_max
        self.rota: List[Tuple[float, float]] = []
        self.entregas = []