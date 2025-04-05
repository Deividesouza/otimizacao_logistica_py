from typing import List, Tuple
from models import Caminhao

class AlocadorEntregas:
    @staticmethod
    def alocar(grafo, caminhoes: List[Caminhao]):
        for centro in grafo.centros:
            entregas_ordenadas = sorted(centro.entregas, key=lambda e: e.prazo)
            
            for caminhao in centro.caminhoes:
                carga_atual = 0.0
                rota = [centro.localizacao]
                
                for entrega in entregas_ordenadas[:]:
                    if (carga_atual + entrega.peso) <= caminhao.capacidade_max:
                        rota.append(entrega.destino)
                        carga_atual += entrega.peso
                        entregas_ordenadas.remove(entrega)
                
                if len(rota) > 1:
                    rota.append(centro.localizacao)
                    caminhao.rota = rota
                    caminhao.carga_atual = carga_atual

        return caminhoes
    