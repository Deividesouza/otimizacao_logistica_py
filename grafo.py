from typing import List, Tuple
from models import CentroDistribuicao, Entrega
import math

class GrafoLogistica:
    def __init__(self):
        self.centros = []
        self.distancias = {}  # Agora usando IDs como chaves
    
    def adicionar_centro(self, centro):
        self.centros.append(centro)
        self.distancias[centro.id] = {}
    
    def calcular_distancia(self, ponto1, ponto2):
        return math.sqrt((ponto1[0]-ponto2[0])**2 + (ponto1[1]-ponto2[1])**2)
    
    def centro_mais_proximo(self, destino):
        return min(self.centros, 
                key=lambda c: self.calcular_distancia(c.localizacao, destino))
    
    def construir_grafo(self, entregas):
        for centro in self.centros:
            for entrega in entregas:
                distancia = self.calcular_distancia(centro.localizacao, entrega.destino)
                self.distancias[centro.id][id(entrega)] = distancia  # Usando ID único