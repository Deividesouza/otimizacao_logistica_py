from typing import Dict, Tuple, List
import math
import heapq
from models import CentroDistribuicao, Entrega

def calcular_distancia(ponto1: Tuple[float, float], ponto2: Tuple[float, float]) -> float:
    """Calcula a distância euclidiana entre dois pontos"""
    return math.sqrt((ponto1[0] - ponto2[0])**2 + (ponto1[1] - ponto2[1])**2)

def construir_grafo(centros: List[CentroDistribuicao], entregas: List[Entrega]) -> Dict:
    """Constrói um grafo simples onde cada nó é conectado com todos os outros"""
    grafo = {}
    # Coleta todos os pontos (centros e destinos)
    pontos = [centro.localizacao for centro in centros] + [entrega.destino_localizacao for entrega in entregas]
    
    # Inicializa o grafo
    for ponto in pontos:
        grafo[ponto] = {}
    
    # Conecta todos os pontos entre si
    for i, origem in enumerate(pontos):
        for destino in pontos:
            if origem != destino:
                grafo[origem][destino] = calcular_distancia(origem, destino)
    
    return grafo

def dijkstra(grafo: Dict, origem: Tuple[float, float], destino: Tuple[float, float]) -> List[Tuple[float, float]]:
    """Implementação do algoritmo de Dijkstra para encontrar o caminho mais curto"""
    # Inicialização
    distancias = {ponto: float('infinity') for ponto in grafo}
    distancias[origem] = 0
    fila_prioridade = [(0, origem)]
    anterior = {ponto: None for ponto in grafo}
    visitados = set()
    
    while fila_prioridade:
        # Pega o vértice com menor distância
        dist_atual, atual = heapq.heappop(fila_prioridade)
        
        # Se já processamos este vértice, pula
        if atual in visitados:
            continue
        
        # Se chegamos ao destino, terminamos
        if atual == destino:
            break
            
        visitados.add(atual)
        
        # Verifica os vizinhos
        for vizinho, peso in grafo[atual].items():
            if vizinho in visitados:
                continue
            
            distancia = dist_atual + peso
            
            # Se encontramos um caminho mais curto para o vizinho
            if distancia < distancias[vizinho]:
                distancias[vizinho] = distancia
                anterior[vizinho] = atual
                heapq.heappush(fila_prioridade, (distancia, vizinho))
    
    # Reconstrói o caminho
    caminho = []
    atual = destino
    while atual:
        caminho.append(atual)
        atual = anterior[atual]
    
    # Inverte o caminho para ter origem -> destino
    return list(reversed(caminho))

def encontrar_nome_local(localizacao: Tuple[float, float], centros: List[CentroDistribuicao], entregas: List[Entrega]) -> str:
    """Encontra o nome de um local com base nas coordenadas"""
    # Primeiro verifica se é um centro de distribuição
    for centro in centros:
        if centro.localizacao == localizacao:
            return centro.nome
    
    # Depois verifica se é um destino de entrega
    for entrega in entregas:
        if entrega.destino_localizacao == localizacao:
            return entrega.destino_nome
    
    # Se não encontrar, retorna as coordenadas
    return f"Ponto ({localizacao[0]:.2f}, {localizacao[1]:.2f})"