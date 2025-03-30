from models import CentroDistribuicao, Entrega, Caminhao
from grafo import GrafoLogistica
from algoritimos import AlocadorEntregas

def main():
    # 1. Criar centros
    centros = [
        CentroDistribuicao("Belém", -1.45, -48.49),
        CentroDistribuicao("Recife", -8.04, -34.87),
        CentroDistribuicao("Brasília", -15.79, -47.88),
        CentroDistribuicao("São Paulo", -10.79, 10.25),
        CentroDistribuicao("Florianopolis", -3.12, -57.52)
    ]
    
    # 2. Criar caminhões
    for centro in centros:
        centro.caminhoes = [Caminhao(1000) for _ in range(2)]  # 2 caminhões por centro
    
    # 3. Criar entregas
    entregas = [
        Entrega((-1.44, -48.50), 300, 24),
        Entrega((-8.05, -34.86), 500, 12),
        Entrega((-15.80, -47.90), 700, 48),
        Entrega((-1.46, -48.51), 400, 36)
    ]
    
    # 4. Construir grafo
    grafo = GrafoLogistica()
    for centro in centros:
        grafo.adicionar_centro(centro)
    grafo.construir_grafo(entregas)
    
    # 5. Associar entregas aos centros
    for entrega in entregas:
        centro = grafo.centro_mais_proximo(entrega.destino)
        centro.entregas.append(entrega)
    
    # 6. Alocar entregas
    AlocadorEntregas.alocar(grafo, [c for centro in centros for c in centro.caminhoes])
    
    # 7. Exibir resultados
    print("Relatório de Alocação")
    for centro in centros:
        print(f"\n{centro.nome}:")
        print(f"Entregas não alocadas: {len(centro.entregas)}")
        for i, caminhao in enumerate(centro.caminhoes):
            print(f"  Caminhão {i+1}:")
            print(f"  - Carga: {caminhao.carga}kg")
            print(f"  - Paradas: {len(caminhao.rota)-2}")
            print(f"  - Rota: {' → '.join(map(str, caminhao.rota))}")

if __name__ == "__main__":
    main()