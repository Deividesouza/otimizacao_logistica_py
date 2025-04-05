from models import CentroDistribuicao, Entrega, Caminhao
from grafo import GrafoLogistica
from geolocalizador import retornar_endereco
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
            Caminhao(id=caminhao_id + i, capacidade_max=4000.0)
            for i in range(2)
        ]
        caminhao_id += 2
    
    # 3. Criar entregas
    entregas = [
    Entrega(destino=(-15.163366003799249, -48.288148331074936), peso=1000.0, prazo=36),
    Entrega(destino=(-15.5417414, -47.3384334), peso=1200.0, prazo=60),
    Entrega(destino=(-15.5417414, -47.3384334), peso=1200.0, prazo=80),
    Entrega(destino=(-15.5417414, -47.3384334), peso=1200.0, prazo=24),
    Entrega(destino=(-16.767394363667858, -47.613630775677635), peso=350.5, prazo=12)
    ]
    
    # 4. Construir grafo
    grafo = GrafoLogistica() # Inicializa o grafo de logística
    for centro in centros:
        grafo.adicionar_centro(centro) # Adiciona centros ao grafo
        grafo.construir_grafo(entregas) # Constrói o grafo com as entregas associadas aos centros 
    
    # 5. Associar entregas
    for entrega in entregas:
        centro = grafo.centro_mais_proximo(entrega.destino) # Encontra o centro mais próximo da entrega
        centro.entregas.append(entrega) # Adiciona a entrega ao centro mais próximo
    
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
            print(f"  - Paradas: {len(caminhao.rota)}")
            #print(f"  - Rota: {' → '.join(map(str, caminhao.rota))}")
            for i, rota in enumerate(caminhao.rota):
                
                resultado = retornar_endereco(rota[0], rota[1])
                if i == len(caminhao.rota) - 1:
                    print(f"  - Retorno: {resultado.get('address', {}).get('suburb')}")
                elif resultado:
                    print(f"  - Rota: {resultado.get('address', {}).get('suburb')}")
                else:
                    print(f"  - Rota: Não foi possível obter o endereço.")

if __name__ == "__main__":
    main()
    