from models import CentroDistribuicao, Entrega, Caminhao
from grafo import GrafoLogistica
from algoritmos import AlocadorEntregas

def main():
    # 1. Criar centros
    centros = [
        CentroDistribuicao(
            id=1,
            nome="Belém",
            localizacao=(-1.4557, -48.4902)
        ),
        CentroDistribuicao(
            id=2,
            nome="Recife",
            localizacao=(-8.05428, -34.8813)
        ),
        CentroDistribuicao(
            id=3,
            nome="Brasília",
            localizacao=(-15.7975, -47.8919)
        ),
        CentroDistribuicao(
            id=4,
            nome="São Paulo",
            localizacao=(-23.5505, -46.6333)
        ),
        CentroDistribuicao(
            id=5,
            nome="Florianópolis",
            localizacao=(-27.5969, -48.5495)
        )
    ]
    
    # 2. Criar caminhões com IDs únicos
    caminhao_id = 1
    for centro in centros:
        centro.caminhoes = [
            Caminhao(id=caminhao_id + i, capacidade_max=3500)
            for i in range(2)
        ]
        caminhao_id += 2
    
    # 3. Criar entregas
    entregas = [
    Entrega(destino=(-23.812, -47.192), peso=845.3, prazo=36),
    Entrega(destino=(-8.123, -34.456), peso=1200.0, prazo=24),
    Entrega(destino=(-15.345, -47.891), peso=350.5, prazo=12),
    Entrega(destino=(-1.789, -48.123), peso=1800.7, prazo=48),
    Entrega(destino=(-27.234, -48.789), peso=950.0, prazo=60),
    Entrega(destino=(-23.987, -46.345), peso=420.8, prazo=6),
    Entrega(destino=(-8.456, -34.789), peso=1500.5, prazo=18),
    Entrega(destino=(-15.678, -47.345), peso=670.3, prazo=36),
    Entrega(destino=(-1.234, -48.456), peso=2000.0, prazo=72),
    Entrega(destino=(-27.567, -48.123), peso=1300.2, prazo=24)
    ]
    
    # 4. Construir grafo
    grafo = GrafoLogistica()
    for centro in centros:
        grafo.adicionar_centro(centro)
        grafo.construir_grafo(entregas)
    
    # 5. Associar entregas
    for entrega in entregas:
        centro = grafo.centro_mais_proximo(entrega.destino)
        centro.entregas.append(entrega)
    
    # 6. Alocar entregas
    AlocadorEntregas.alocar(grafo, [c for centro in centros for c in centro.caminhoes])
    
    # 7. Resultados
    print("Relatório Final")
    for centro in centros:
        print(f"\n{centro.nome}:")
        print(f"Entregas pendentes: {len(centro.entregas)}")
        for caminhao in centro.caminhoes:
            print(f"  Caminhão {caminhao.id}:")
            print(f"  - Capacidade: {caminhao.carga_atual}/{caminhao.capacidade_max}kg")
            print(f"  - Paradas: {len(caminhao.rota)-2}")
            print(f"  - Rota: {' → '.join(map(str, caminhao.rota))}")

if __name__ == "__main__":
    main()