from models import CentroDistribuicao, Entrega, Caminhao
from grafo import construir_grafo
from algoritmos import (
    atribuir_entregas_aos_centros,
    atribuir_entregas_aos_caminhoes,
    calcular_rota_caminhao,
    desenhar_mapa
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
    entregas = [
        Entrega(1, (-3.10, -60.02), "Manaus", 800.0, 5),
        Entrega(2, (-19.92, -43.94), "Belo Horizonte", 500.0, 3),
        Entrega(3, (-30.03, -51.23), "Porto Alegre", 700.0, 4),
        Entrega(4, (-12.97, -38.51), "Salvador", 600.0, 2),
        Entrega(5, (-22.90, -43.17), "Rio de Janeiro", 900.0, 1),
        Entrega(6, (-16.68, -49.25), "Goiânia", 400.0, 2),
        Entrega(7, (-9.65, -35.73), "Maceió", 300.0, 3),
        Entrega(8, (-25.42, -49.27), "Curitiba", 500.0, 2),
        Entrega(9, (-3.73, -38.52), "Fortaleza", 600.0, 4),
        Entrega(10, (-15.12, -34.86), "João Pessoa", 200.0, 1)
    ]

    # 3. Criar caminhões para cada centro
    for i, centro in enumerate(centros):
        caminhao1 = Caminhao(i*2+1, 1500.0)
        caminhao2 = Caminhao(i*2+2, 1000.0)
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

    # 6. Atribuir entregas aos caminhões
    print("\nAtribuindo entregas aos caminhões...")
    atribuir_entregas_aos_caminhoes(centros)

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