import math

class GrafoLogistica:
    def __init__(self):
        self.centros = [] # Lista de centros de distribuição
        self.distancias = {}  # Dicionário para armazenar distâncias entre centros e entregas
    
    def adicionar_centro(self, centro):
        self.centros.append(centro) # Adiciona um centro de distribuição ao grafo
        self.distancias[centro.id] = {} # Inicializa o dicionário de distâncias para o novo centro
    
    def calcular_distancia(self, ponto1, ponto2): 
        return math.sqrt((ponto1[0]-ponto2[0])**2 + (ponto1[1]-ponto2[1])**2) # Calcula a distância euclidiana entre dois pontos (coordenadas)
    
    def centro_mais_proximo(self, destino):
        return min(self.centros, key=lambda c: self.calcular_distancia(c.localizacao, destino)) # Retorna o centro de distribuição mais próximo de um destino específico
    
    def construir_grafo(self, entregas): 
        for centro in self.centros: # Para cada centro de distribuição
            for entrega in entregas:
                distancia = self.calcular_distancia(centro.localizacao, entrega.destino) # Calcula a distância entre o centro e a entrega
                self.distancias[centro.id][id(entrega)] = distancia  # Usando ID único