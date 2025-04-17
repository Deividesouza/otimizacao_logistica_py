from models import CentroDistribuicao, Entrega, Caminhao
from grafo import construir_grafo
from algoritmos import (
    atribuir_entregas_aos_centros,
    atribuir_entregas_aos_caminhoes,
    calcular_rota_caminhao,
    desenhar_mapa,
    carregar_entregas_csv
)

def criar_dados_teste():
    """Criar dados para testar o sistema"""
    # 1. Criar os centros de distribuição
    centros = [
        CentroDistribuicao(1, "Belém", (-1.45, -48.48)),
        CentroDistribuicao(2, "Recife", (-8.05, -34.88)),
        CentroDistribuicao(3, "Brasília", (-15.78, -47.93)),
        CentroDistribuicao(4, "São Paulo", (-23.55, -46.63)),
        CentroDistribuicao(5, "Florianópolis", (-27.59, -48.55))
    ]

    # 2. Criar entregas
    entregas = carregar_entregas_csv("entregas.csv")
    
    # Se não houver entregas carregadas (arquivo não encontrado ou vazio), 
    # use dados de exemplo pré-definidos como fallback
    if not entregas:
        print("Usando dados de entrega de exemplo pré-definidos...")
        entregas = [
            # Região Norte (Manaus e proximidades)
            Entrega(1, (-3.10, -60.02), "Manaus", 800.0, 5),
            Entrega(11, (-3.47, -62.21), "Novo Airão", 450.0, 3),
            # Adicione algumas entregas padrão como fallback
            # ...
            Entrega(60, (-7.50, -73.91), "Mâncio Lima", 300.0, 1),
        ]

    # 3. Criar caminhões para cada centro com velocidades e limites diferentes
    for i, centro in enumerate(centros):
        # Caminhão 1: mais rápido, mas com menos horas disponíveis
        caminhao1 = Caminhao(i*2+1, 2000.0, velocidade_media=80.0, limite_de_horas=8.0)
        
        # Caminhão 2: mais lento, mas com mais horas disponíveis
        caminhao2 = Caminhao(i*2+2, 10000.0, velocidade_media=60.0, limite_de_horas=6.0)
        
        centro.caminhoes = [caminhao1, caminhao2]
    
    return centros, entregas

def resolver_problema():
    """Função principal que resolve o problema de distribuição"""
    print("Iniciando solução do problema de distribuição...")
    
    # Criar os dados de teste
    centros, entregas = criar_dados_teste()

    # 4. Construir o grafo
    print("\nConstruindo grafo com todas as localizações...")
    grafo = construir_grafo(centros, entregas)

    # 5. Atribuir entregas aos centros mais próximos
    print("\nAtribuindo entregas aos centros mais próximos...")
    atribuir_entregas_aos_centros(centros, entregas)

    # 6. Atribuir entregas aos caminhões considerando prazo e limite de horas
    print("\nAtribuindo entregas aos caminhões...")
    atribuir_entregas_aos_caminhoes(centros, grafo, entregas)

    # 7. Calcular rotas para cada caminhão com exibição detalhada
    print("\nCalculando rotas ótimas para cada caminhão...")
    for centro in centros:
        for caminhao in centro.caminhoes:
            if hasattr(caminhao, 'entregas') and caminhao.entregas:
                caminhao.rota = calcular_rota_caminhao(grafo, caminhao, centro, centros, entregas)

    print("\nOtimização de rotas concluída!")

    # 8. Mostrar visualização com pygame
    print("\nExibindo visualização gráfica...")
    desenhar_mapa(centros, entregas, mostrar_rotas=True)

if __name__ == "__main__":
    resolver_problema()