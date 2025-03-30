from models import CentroDistribuicao, Entrega, Caminhao
from grafo import GrafoLogistica
from algoritimos import AlocadorEntregas

def main():
    # 1. Criar centros
    centros = [
        CentroDistribuicao(
        nome="Belém",
        localizacao=(-1.4557, -48.4902)  # Praça da República, Belém
    ),
    CentroDistribuicao(
        nome="Recife",
        localizacao=(-8.05428, -34.8813)  # Marco Zero, Recife
    ),
    CentroDistribuicao(
        nome="Brasília",
        localizacao=(-15.7975, -47.8919)  # Praça dos Três Poderes
    ),
    CentroDistribuicao(
        nome="São Paulo",
        localizacao=(-23.5505, -46.6333)  # Centro Histórico de SP
    ),
    CentroDistribuicao(
        nome="Florianópolis",
        localizacao=(-27.5969, -48.5495)  # Centro da Cidade
    )
    ]
    
    # 2. Criar caminhões
    for centro in centros:
        centro.caminhoes = [Caminhao(1000) for _ in range(2)]  # 2 caminhões por centro
    
    # 3. Criar entregas
    entregas = [
        Entrega(destino=(-23.5505, -46.6333), peso=300.5,prazo=24)]
    
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