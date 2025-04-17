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
        # Região Norte (prazos entre 20-30 dias)
        Entrega(1, (-3.10, -60.02), "Manaus", 800.0, 25),  # Área remota
        Entrega(11, (-3.47, -62.21), "Novo Airão", 450.0, 28),  # Acesso fluvial
        Entrega(12, (-2.63, -56.74), "Itacoatiara", 600.0, 22),
        Entrega(13, (-5.53, -63.36), "Manacapuru", 550.0, 26),
        Entrega(14, (-1.53, -61.87), "Presidente Figueiredo", 300.0, 20),
        Entrega(2, (-19.92, -43.94), "Belo Horizonte", 500.0, 16),
        Entrega(15, (-19.77, -42.87), "Ipatinga", 400.0, 18),
        Entrega(16, (-21.76, -43.35), "Juiz de Fora", 350.0, 15),
        Entrega(17, (-20.38, -43.51), "Ouro Preto", 250.0, 17),
        Entrega(5, (-22.90, -43.17), "Rio de Janeiro", 900.0, 15),
        Entrega(18, (-22.42, -42.97), "Teresópolis", 300.0, 18),
        Entrega(19, (-22.52, -43.73), "Petrópolis", 350.0, 17),
        Entrega(20, (-23.18, -44.95), "Angra dos Reis", 400.0, 20),  # Acesso por ferry
        Entrega(21, (-22.12, -43.21), "Volta Redonda", 450.0, 16),
        Entrega(3, (-30.03, -51.23), "Porto Alegre", 700.0, 20),
        Entrega(22, (-29.68, -51.13), "Canoas", 500.0, 18),
        Entrega(23, (-32.03, -52.08), "Rio Grande", 600.0, 25),  # Porto
        Entrega(24, (-29.17, -51.18), "Caxias do Sul", 550.0, 22),
        Entrega(8, (-25.42, -49.27), "Curitiba", 500.0, 18),
        Entrega(25, (-25.09, -50.16), "Ponta Grossa", 400.0, 20),
        Entrega(26, (-23.55, -46.63), "São Paulo", 1000.0, 15),  # Capital
        Entrega(27, (-23.96, -46.33), "Santos", 800.0, 25),  # Porto principal
        Entrega(28, (-22.12, -47.89), "Campinas", 700.0, 16),
        Entrega(4, (-12.97, -38.51), "Salvador", 600.0, 22),
        Entrega(29, (-12.25, -38.95), "Candeias", 350.0, 23),
        Entrega(30, (-13.01, -38.52), "Lauro de Freitas", 300.0, 21),
        Entrega(7, (-9.65, -35.73), "Maceió", 300.0, 24),
        Entrega(31, (-9.66, -35.74), "Marechal Deodoro", 250.0, 25),
        Entrega(32, (-10.91, -37.07), "Aracaju", 400.0, 23),
        Entrega(9, (-3.73, -38.52), "Fortaleza", 600.0, 28),
        Entrega(33, (-3.72, -38.60), "Caucaia", 450.0, 27),
        Entrega(34, (-4.18, -38.88), "Pacatuba", 350.0, 26),
        Entrega(10, (-15.12, -34.86), "João Pessoa", 200.0, 25),
        Entrega(35, (-7.12, -34.88), "Recife", 500.0, 24),
        Entrega(36, (-8.05, -34.90), "Olinda", 300.0, 23),
        Entrega(37, (-5.79, -35.21), "Natal", 400.0, 24),
        Entrega(6, (-16.68, -49.25), "Goiânia", 400.0, 18),
        Entrega(38, (-16.42, -49.25), "Aparecida de Goiânia", 350.0, 18),
        Entrega(39, (-15.60, -56.10), "Cuiabá", 500.0, 25),
        Entrega(40, (-20.44, -54.65), "Campo Grande", 450.0, 22),
        Entrega(41, (-18.92, -48.28), "Uberlândia", 550.0, 19),
        Entrega(42, (-12.98, -38.52), "Feira de Santana", 400.0, 20),
        Entrega(43, (-1.45, -48.50), "Belém", 700.0, 28),
        Entrega(44, (-2.53, -44.30), "São Luís", 600.0, 27),
        Entrega(45, (-5.09, -42.80), "Teresina", 500.0, 24),
        Entrega(46, (-7.22, -39.32), "Juazeiro do Norte", 350.0, 22),
        Entrega(47, (-8.76, -63.90), "Porto Velho", 550.0, 30),  # Máximo prazo
        Entrega(48, (-10.91, -37.07), "Aracaju", 400.0, 23),
        Entrega(49, (-27.59, -48.55), "Florianópolis", 600.0, 22),
        Entrega(50, (-22.22, -54.80), "Dourados", 450.0, 25)
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