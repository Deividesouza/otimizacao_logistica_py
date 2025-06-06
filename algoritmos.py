from typing import List, Tuple, Dict
from models import CentroDistribuicao, Entrega, Caminhao
from grafo import calcular_distancia, dijkstra, encontrar_nome_local
import csv

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

def estimar_tempo_rota(rota: List[Tuple[float, float]], velocidade_media: float) -> float:
    """
    Estima o tempo total necessário para percorrer uma rota em horas.
    A distância é calculada em km e a velocidade em km/h.
    
    Args:
        rota: Lista de pontos (latitude, longitude)
        velocidade_media: Velocidade média do caminhão em km/h
        
    Returns:
        Tempo estimado em horas
    """
    if len(rota) <= 1:
        return 0.0
    
    # Calcula a distância total em km
    distancia_total = sum(calcular_distancia(rota[i], rota[i+1]) for i in range(len(rota)-1))
    
    # Tempo = distância / velocidade (em horas)
    tempo_estimado = distancia_total / velocidade_media
    
    return tempo_estimado

def calcular_rota_entrega(grafo: Dict, origem: Tuple[float, float], destino: Tuple[float, float], 
                          centros: List[CentroDistribuicao], todas_entregas: List[Entrega]) -> List[Tuple[float, float]]:
    """Calcula a rota entre origem e destino e retorna o caminho"""
    return dijkstra(grafo, origem, destino)

def verificar_viabilidade_entrega(caminhao: Caminhao, entrega: Entrega, centro: CentroDistribuicao, 
                                 grafo: Dict, centros: List[CentroDistribuicao], todas_entregas: List[Entrega]) -> bool:
    """Verifica se é possível realizar a entrega dentro do prazo e limite de horas do caminhão"""
    # Simula a rota com esta entrega
    origem = centro.localizacao
    destino = entrega.destino_localizacao
    
    # Calcula a rota de ida e volta
    rota_ida = calcular_rota_entrega(grafo, origem, destino, centros, todas_entregas)
    rota_volta = calcular_rota_entrega(grafo, destino, origem, centros, todas_entregas)
    rota_completa = rota_ida + rota_volta[1:]  # Evita duplicar o ponto de destino
    
    # Estima o tempo necessário
    tempo_estimado = estimar_tempo_rota(rota_completa, caminhao.velocidade_media)
    
    # Calcula quantos dias serão necessários baseado no limite de horas por dia
    dias_necessarios = tempo_estimado / caminhao.limite_de_horas
    if dias_necessarios > entrega.prazo:
        return False
    return True

def atribuir_entregas_aos_caminhoes(centros: List[CentroDistribuicao], grafo: Dict, todas_entregas: List[Entrega]) -> None:
    """Atribui entregas aos caminhões considerando capacidade, prazo e limite de horas"""
    for centro in centros:
        # Ordena entregas por prazo (mais urgentes primeiro)
        centro.entregas.sort(key=lambda e: e.prazo)
        
        for caminhao in centro.caminhoes:
            capacidade_restante = caminhao.capacidade_max
            caminhao.entregas = []
            
            # Atribui entregas até encher o caminhão
            for entrega in centro.entregas[:]:
                if (entrega.peso <= capacidade_restante and 
                    verificar_viabilidade_entrega(caminhao, entrega, centro, grafo, centros, todas_entregas)):
                    
                    caminhao.entregas.append(entrega)
                    capacidade_restante -= entrega.peso
                    centro.entregas.remove(entrega)
                    print(f"Entrega {entrega.id} atribuída ao caminhão {caminhao.id} do centro {centro.nome}")
                else:
                    if entrega.peso > capacidade_restante:
                        print(f"Entrega {entrega.id} excede capacidade do caminhão {caminhao.id}")
                    else:
                        print(f"Entrega {entrega.id} não pode ser entregue a tempo pelo caminhão {caminhao.id}")
        
        # Verifica se sobraram entregas não atribuídas
        if centro.entregas:
            print(f"AVISO: {len(centro.entregas)} entregas não puderam ser atribuídas do centro {centro.nome}")

def calcular_rota_caminhao(grafo: Dict, caminhao: Caminhao, centro: CentroDistribuicao, centros: List[CentroDistribuicao], todas_entregas: List[Entrega]) -> List[Tuple[float, float]]:
    """Calcula a rota para um caminhão fazer todas as suas entregas"""
    if not hasattr(caminhao, 'entregas') or not caminhao.entregas:
        return []
    
    print(f"\n=== DETALHAMENTO DA ROTA PARA O CAMINHÃO {caminhao.id} DO CENTRO {centro.nome} ===")
    print(f"Velocidade média: {caminhao.velocidade_media} km/h, Limite de horas por dia: {caminhao.limite_de_horas} horas")
    
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
            
            print(f"  {nome_atual} → {nome_proximo} ({distancia_trecho:.2f} km)")
            
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
        
        print(f"  {nome_atual} → {nome_proximo} ({distancia_trecho:.2f} km)")
        
        # Adiciona ponto à rota (exceto o primeiro que já está)
        if i > 0:
            rota.append(ponto_atual)
    
    # Adiciona o último ponto (centro de distribuição)
    rota.append(centro.localizacao)
    
    # Calcula e exibe o tempo estimado
    tempo_estimado = estimar_tempo_rota(rota, caminhao.velocidade_media)
    dias_necessarios = tempo_estimado / caminhao.limite_de_horas
    
    print(f"\nDistância total percorrida: {distancia_total:.2f} km")
    print(f"Tempo estimado: {tempo_estimado:.2f} horas")
    print(f"Dias necessários: {dias_necessarios:.2f} dias (considerando {caminhao.limite_de_horas} horas/dia)")
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
    pygame.display.set_caption("Mapa Logístico - Centros e Entregas (Distâncias em km)")

    font = pygame.font.SysFont("Arial", 16)
    clock = pygame.time.Clock()

    # Cores
    branco = (255, 255, 255)
    preto = (0, 0, 0)
    azul = (70, 130, 180)  # Azul para centros de distribuição e caminhões ímpares
    verde = (34, 139, 34)  # Verde para caminhões pares
    vermelho = (220, 20, 60)  # Vermelho para entregas
    
    # Tons mais claros para as rotas
    azul_rota = (100, 149, 237)  # Azul mais claro para rotas de caminhões ímpares
    verde_rota = (60, 179, 113)  # Verde mais claro para rotas de caminhões pares

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

    # Adiciona algumas informações sobre a escala
    centro_coords = transformar_coords((min_lat + max_lat) / 2, (min_lon + max_lon) / 2)
    
    # Tenta calcular uma escala aproximada
    try:
        escala_100km_pixels = int(100 / (calcular_distancia((min_lat, min_lon), (min_lat, min_lon + 1)) * lon_range / screen_width))
    except:
        escala_100km_pixels = 100  # Valor padrão se o cálculo falhar
    
    # Criar uma legenda para os caminhões
    def desenhar_legenda():
        # Configurações da legenda
        largura_legenda = 200
        altura_legenda = 100
        margem = 20  # Margem das bordas da tela

        #Posição no canto inferior esquerdo
        pos_x = margem
        pos_y = screen_height - altura_legenda - margem

        #Retângulo de fundo para a legenda
        pygame.draw.rect(screen, (240, 240, 240), (pos_x, pos_y, largura_legenda, altura_legenda), 0)
        pygame.draw.rect(screen, preto, (pos_x, pos_y, largura_legenda, altura_legenda), 1)

        # Título da legenda
        titulo = font.render("Legenda", True, preto)
        screen.blit(titulo, (pos_x + 10, pos_y + 10))

        # Linha para caminhões ímpares
        pygame.draw.line(screen, azul_rota, (pos_x + 10, pos_y + 35), (pos_x + 50, pos_y + 35), 3)
        texto_impar = font.render("Caminhão ID ímpar", True, preto)
        screen.blit(texto_impar, (pos_x + 60, pos_y + 30))

        # Linha para caminhões pares
        pygame.draw.line(screen, verde_rota, (pos_x + 10, pos_y + 60), (pos_x + 50, pos_y + 60), 3)
        texto_par = font.render("Caminhão ID par", True, preto)
        screen.blit(texto_par, (pos_x + 60, pos_y + 55))
        
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
                    if hasattr(caminhao, 'rota') and caminhao.rota:
                        pontos = [transformar_coords(lat, lon) for lat, lon in caminhao.rota]
                        if len(pontos) > 1:
                            # Determina cor da rota baseada no ID do caminhão
                            cor_rota = azul_rota if caminhao.id % 2 != 0 else verde_rota
                            pygame.draw.lines(screen, cor_rota, False, pontos, 3)  # Aumentei a espessura para 3

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

        # Desenhar escala
        pygame.draw.line(screen, preto, (50, screen_height - 50), (50 + escala_100km_pixels, screen_height - 50), 2)
        escala_text = font.render("100 km", True, preto)
        screen.blit(escala_text, (50, screen_height - 70))
        
        # Desenhar legenda
        desenhar_legenda()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def carregar_entregas_csv(caminho_arquivo: str) -> List[Entrega]:
    """
    Carrega dados de entregas a partir de um arquivo CSV.
    
    O arquivo CSV deve ter o seguinte formato:
    id,latitude,longitude,destino_nome,peso,prazo
    
    Args:
        caminho_arquivo: Caminho para o arquivo CSV
        
    Returns:
        Lista de objetos Entrega
    """
    entregas = []
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            
            for linha in leitor_csv:
                # Converter valores para os tipos corretos
                id_entrega = int(linha['id'])
                latitude = float(linha['latitude'])
                longitude = float(linha['longitude'])
                destino_nome = linha['destino_nome']
                peso = float(linha['peso'])
                prazo = int(linha['prazo'])
                
                # Criar objeto Entrega
                entrega = Entrega(
                    id=id_entrega,
                    destino_localizacao=(latitude, longitude),
                    destino_nome=destino_nome,
                    peso=peso,
                    prazo=prazo
                )
                
                entregas.append(entrega)
                
        print(f"Carregadas {len(entregas)} entregas do arquivo {caminho_arquivo}")
        return entregas
    
    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho_arquivo} não encontrado.")
        return []
    except KeyError as e:
        print(f"Erro: Coluna obrigatória ausente no CSV: {e}")
        return []
    except ValueError as e:
        print(f"Erro: Problema ao converter valor no CSV: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado ao carregar o arquivo CSV: {e}")
        return []