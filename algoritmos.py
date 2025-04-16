from typing import List, Tuple, Dict
from models import CentroDistribuicao, Entrega, Caminhao
from grafo import calcular_distancia, dijkstra, encontrar_nome_local

def encontrar_centro_mais_proximo(centros: List[CentroDistribuicao], entrega: Entrega) -> CentroDistribuicao:
    """Encontra o centro de distribuição mais próximo para uma entrega"""
    centro_mais_proximo = None
    menor_distancia = float('inf')
    
    for centro in centros:
        distancia = calcular_distancia(centro.localizacao, entrega.destino_localizacao)
        if distancia < menor_distancia:
            menor_distancia = distancia
            centro_mais_proximo = centro
    
    return centro_mais_proximo

def atribuir_entregas_aos_centros(centros: List[CentroDistribuicao], entregas: List[Entrega]) -> None:
    """Atribui cada entrega ao centro de distribuição mais próximo"""
    for entrega in entregas:
        centro = encontrar_centro_mais_proximo(centros, entrega)
        centro.entregas.append(entrega)
        print(f"Entrega {entrega.id} para {entrega.destino_nome} atribuída ao centro {centro.nome}")

def atribuir_entregas_aos_caminhoes(centros: List[CentroDistribuicao]) -> None:
    """Atribui entregas aos caminhões considerando capacidade"""
    for centro in centros:
        # Ordena entregas por prazo (mais urgentes primeiro)
        centro.entregas.sort(key=lambda e: e.prazo)
        
        for caminhao in centro.caminhoes:
            capacidade_restante = caminhao.capacidade_max
            caminhao.entregas = []
            
            # Atribui entregas até encher o caminhão
            for entrega in centro.entregas[:]:
                if entrega.peso <= capacidade_restante:
                    caminhao.entregas.append(entrega)
                    capacidade_restante -= entrega.peso
                    centro.entregas.remove(entrega)
                    print(f"Entrega {entrega.id} atribuída ao caminhão {caminhao.id} do centro {centro.nome}")
        
        # Verifica se sobraram entregas não atribuídas
        if centro.entregas:
            print(f"AVISO: {len(centro.entregas)} entregas não puderam ser atribuídas do centro {centro.nome}")

def calcular_rota_caminhao(grafo: Dict, caminhao: Caminhao, centro: CentroDistribuicao, centros: List[CentroDistribuicao], todas_entregas: List[Entrega]) -> List[Tuple[float, float]]:
    """Calcula a rota para um caminhão fazer todas as suas entregas"""
    if not hasattr(caminhao, 'entregas') or not caminhao.entregas:
        return []
    
    print(f"\n=== DETALHAMENTO DA ROTA PARA O CAMINHÃO {caminhao.id} DO CENTRO {centro.nome} ===")
    
    # Começa no centro de distribuição
    posicao_atual = centro.localizacao
    rota = [posicao_atual]
    destinos = [(entrega.destino_localizacao, entrega) for entrega in caminhao.entregas]
    distancia_total = 0
    
    print(f"Partida: {centro.nome} {posicao_atual}")
    
    # Enquanto houver destinos para visitar
    while destinos:
        # Encontra o destino mais próximo da posição atual
        destino_mais_proximo = None
        entrega_mais_proxima = None
        menor_distancia = float('inf')
        melhor_caminho = None
        
        for destino, entrega in destinos:
            caminho = dijkstra(grafo, posicao_atual, destino)
            distancia = sum(calcular_distancia(caminho[i], caminho[i+1]) for i in range(len(caminho)-1))
            if distancia < menor_distancia:
                menor_distancia = distancia
                destino_mais_proximo = destino
                entrega_mais_proxima = entrega
                melhor_caminho = caminho
        
        # Adiciona o destino à rota
        print(f"\nTrajeto para entrega {entrega_mais_proxima.id} ({entrega_mais_proxima.destino_nome}):")
        
        # Mostrar o caminho percorrido detalhadamente
        for i in range(len(melhor_caminho) - 1):
            ponto_atual = melhor_caminho[i]
            proximo_ponto = melhor_caminho[i + 1]
            distancia_trecho = calcular_distancia(ponto_atual, proximo_ponto)
            distancia_total += distancia_trecho
            
            nome_atual = encontrar_nome_local(ponto_atual, centros, todas_entregas)
            nome_proximo = encontrar_nome_local(proximo_ponto, centros, todas_entregas)
            
            print(f"  {nome_atual} → {nome_proximo} ({distancia_trecho:.2f} unidades)")
            
            # Adiciona ponto à rota
            if i > 0:  # O primeiro ponto já está na rota
                rota.append(ponto_atual)
        
        # Adiciona o destino final à rota
        rota.append(destino_mais_proximo)
        
        # Remove o destino da lista
        destinos = [(d, e) for d, e in destinos if d != destino_mais_proximo]
        posicao_atual = destino_mais_proximo
    
    # Calcular e exibir o caminho de volta ao centro
    caminho_volta = dijkstra(grafo, posicao_atual, centro.localizacao)
    print(f"\nRetorno para o centro {centro.nome}:")
    
    for i in range(len(caminho_volta) - 1):
        ponto_atual = caminho_volta[i]
        proximo_ponto = caminho_volta[i + 1]
        distancia_trecho = calcular_distancia(ponto_atual, proximo_ponto)
        distancia_total += distancia_trecho
        
        nome_atual = encontrar_nome_local(ponto_atual, centros, todas_entregas)
        nome_proximo = encontrar_nome_local(proximo_ponto, centros, todas_entregas)
        
        print(f"  {nome_atual} → {nome_proximo} ({distancia_trecho:.2f} unidades)")
        
        # Adiciona ponto à rota (exceto o primeiro que já está)
        if i > 0:
            rota.append(ponto_atual)
    
    # Adiciona o último ponto (centro de distribuição)
    rota.append(centro.localizacao)
    
    print(f"\nDistância total percorrida: {distancia_total:.2f} unidades")
    print(f"Total de entregas realizadas: {len(caminhao.entregas)}")
    print("=" * 70)
    
    return rota

# Função que implementa a visualização com pygame
def desenhar_mapa(centros, entregas, mostrar_rotas=True):
    import pygame
    
    pygame.init()

    # Aumenta a largura e altura da janela
    screen_width, screen_height = 1400, 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mapa Logístico - Centros e Entregas")

    font = pygame.font.SysFont("Arial", 16)
    clock = pygame.time.Clock()

    # Cores
    branco = (255, 255, 255)
    preto = (0, 0, 0)
    azul = (70, 130, 180)
    vermelho = (220, 20, 60)
    verde = (34, 139, 34)
    cinza = (169, 169, 169)

    # Coleta das latitudes e longitudes
    latitudes = [loc.localizacao[0] for loc in centros] + [ent.destino_localizacao[0] for ent in entregas]
    longitudes = [loc.localizacao[1] for loc in centros] + [ent.destino_localizacao[1] for ent in entregas]
    min_lat, max_lat = min(latitudes), max(latitudes)
    min_lon, max_lon = min(longitudes), max(longitudes)

    # Aumenta o padding para "afastar" os pontos das bordas
    padding_lat = 1.0
    padding_lon = 1.5

    lat_range = (max_lat - min_lat) + 2 * padding_lat
    lon_range = (max_lon - min_lon) + 2 * padding_lon

    def transformar_coords(lat, lon):
        x = int(((lon - (min_lon - padding_lon)) / lon_range) * screen_width)
        y = int(((max_lat + padding_lat - lat) / lat_range) * screen_height)
        return x, y

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        screen.fill(branco)

        # Desenhar as rotas dos caminhões
        if mostrar_rotas:
            for centro in centros:
                for caminhao in centro.caminhoes:
                    if caminhao.rota:
                        pontos = [transformar_coords(lat, lon) for lat, lon in caminhao.rota]
                        if len(pontos) > 1:
                            pygame.draw.lines(screen, cinza, False, pontos, 2)

        # Desenhar centros
        for centro in centros:
            lat, lon = centro.localizacao
            x, y = transformar_coords(lat, lon)
            pygame.draw.circle(screen, azul, (x, y), 8)
            text = font.render(centro.nome, True, preto)

            text_rect = text.get_rect(center=(x, y - 12))  # Nome centralizado acima
            screen.blit(text, text_rect)

        # Desenhar entregas
        for entrega in entregas:
            lat, lon = entrega.destino_localizacao
            x, y = transformar_coords(lat, lon)
            pygame.draw.circle(screen, vermelho, (x, y), 6)
            text = font.render(entrega.destino_nome, True, preto)

            text_rect = text.get_rect(center=(x, y - 12))  # Nome centralizado acima
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()